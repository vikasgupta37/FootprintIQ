# Security Architecture & Implementation
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Status:** Implementation Ready

---

## Security Principles

1. **Defense in Depth** - Multiple security layers
2. **Zero Trust Architecture** - Verify everything
3. **Least Privilege** - Minimal access rights
4. **Encryption Everywhere** - Data at rest and in transit
5. **Security by Design** - Built-in from start

---

## Authentication & Authorization

### OAuth 2.0 + JWT Implementation

**Token Structure:**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@email.com",
    "role": "user",
    "exp": 1687104000,
    "iat": 1687103100
  }
}
```

### Password Security

- **Algorithm:** bcrypt with 12 rounds
- **Requirements:** Min 8 chars, uppercase, lowercase, number, special char
- **Storage:** Hashed, never plaintext
- **Reset:** Secure token with 1-hour expiry

### Role-Based Access Control (RBAC)

**Roles:**
- `user`: Standard access
- `premium`: Enhanced features
- `admin`: Full system access
- `corporate_manager`: Organization management

---

## Data Security

### Encryption

**At Rest:**
- Database: AES-256 encryption
- S3: Server-side encryption (SSE-S3)
- Secrets: AWS Secrets Manager

**In Transit:**
- TLS 1.3 minimum
- HTTPS only (HSTS enabled)
- Certificate pinning for mobile apps

### Data Classification

| Level | Description | Examples | Protection |
|-------|-------------|----------|------------|
| Public | Non-sensitive | Blog posts | Standard HTTPS |
| Internal | User-generated | Carbon data | Encryption + Auth |
| Confidential | Personal data | Email, name | Encryption + RBAC |
| Restricted | Credentials | Passwords, tokens | HSM + Encryption |

---

## API Security

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/carbon/calculate")
@limiter.limit("10/hour")
async def calculate_footprint():
    pass
```

### Input Validation

```python
from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://footprintiq.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600
)
```

---

## Infrastructure Security

### AWS Security Groups

**Frontend (ECS):**
```
Inbound:
- Port 443 from ALB only
- Port 80 from ALB only

Outbound:
- All traffic
```

**Backend (ECS):**
```
Inbound:
- Port 8000 from ALB only

Outbound:
- Port 5432 to RDS
- Port 6379 to Redis
- Port 443 to Internet (API calls)
```

**Database (RDS):**
```
Inbound:
- Port 5432 from Backend security group only

Outbound:
- None
```

### WAF Rules

```json
{
  "rules": [
    {
      "name": "RateLimitRule",
      "priority": 1,
      "action": "BLOCK",
      "rateLimit": 2000
    },
    {
      "name": "SQLInjectionProtection",
      "priority": 2,
      "action": "BLOCK",
      "managedRuleGroup": "AWSManagedRulesSQLiRuleSet"
    },
    {
      "name": "XSSProtection",
      "priority": 3,
      "action": "BLOCK",
      "managedRuleGroup": "AWSManagedRulesKnownBadInputsRuleSet"
    }
  ]
}
```

---

## Application Security

### SQL Injection Prevention

```python
# GOOD - Using ORM
users = db.query(User).filter(User.email == email).all()

# BAD - String concatenation (NEVER DO THIS)
# query = f"SELECT * FROM users WHERE email = '{email}'"
```

### XSS Protection

```typescript
// Frontend - Sanitize user input
import DOMPurify from 'dompurify';

const sanitized = DOMPurify.sanitize(userInput);
```

**Content Security Policy:**
```
Content-Security-Policy: 
  default-src 'self'; 
  script-src 'self' 'unsafe-inline' https://trusted-cdn.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.footprintiq.com;
```

### CSRF Protection

```python
from fastapi_csrf_protect import CsrfProtect

@app.post("/api/v1/users/update")
async def update_user(csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    # Process update
```

---

## Monitoring & Incident Response

### Security Monitoring

**CloudWatch Alarms:**
- Failed login attempts > 5
- Unusual API patterns
- Database connection failures
- Unauthorized access attempts

### Audit Logging

```python
async def audit_log(
    user_id: str,
    action: str,
    resource: str,
    status: str
):
    await db.execute(
        """
        INSERT INTO audit_logs 
        (user_id, action, resource, status, ip_address, user_agent)
        VALUES ($1, $2, $3, $4, $5, $6)
        """,
        user_id, action, resource, status, ip, user_agent
    )
```

---

## Compliance

### GDPR Compliance

- **Right to Access:** Data export API
- **Right to Deletion:** Soft delete with 30-day grace
- **Right to Portability:** JSON/CSV export
- **Consent Management:** Explicit opt-in
- **Privacy by Design:** Minimal data collection

### Data Retention

| Data Type | Retention Period | Deletion Method |
|-----------|-----------------|-----------------|
| User data | Until account deletion | Soft delete + hard delete after 30 days |
| Logs | 90 days | Automatic |
| Backups | 30 days | Automatic |
| Analytics | 2 years (anonymized) | Automatic |

---

## Incident Response Plan

### Severity Levels

**P1 - Critical:**
- Data breach
- Service completely down
- Security vulnerability exploited

**P2 - High:**
- Partial service outage
- Performance degradation
- Suspected security issue

**P3 - Medium:**
- Minor bugs
- Feature not working

### Response Procedure

1. **Detection** (0-15 min): Alert triggered
2. **Triage** (15-30 min): Assess severity
3. **Containment** (30-60 min): Stop the breach
4. **Eradication** (1-4 hours): Remove threat
5. **Recovery** (4-24 hours): Restore service
6. **Post-Incident** (1-7 days): Review and improve

---

**Document Owner:** Security Team  
**Last Updated:** June 17, 2026  
**Next Review:** July 17, 2026
