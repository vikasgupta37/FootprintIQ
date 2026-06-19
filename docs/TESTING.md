# Testing Strategy
# FootprintIQ

**Version:** 1.0.0  
**Date:** June 17, 2026

---

## Testing Pyramid

```
        /\
       /E2E\       ← 10% (Critical user flows)
      /──────\
     /Integration\ ← 30% (API + DB + Services)
    /────────────\
   /  Unit Tests  \ ← 60% (Functions, components)
  /────────────────\
```

---

## Backend Testing (Python + Pytest)

### Unit Tests

```python
# tests/test_carbon_calculations.py
import pytest
from app.utils.carbon_calculations import calculate_transportation

def test_calculate_transportation_petrol_car():
    result = calculate_transportation({
        "vehicle_type": "car_petrol",
        "km_per_month": 600,
        "flights_short_haul": 0,
        "flights_long_haul": 0
    })
    
    expected = 600 * 0.171 * 12  # 1231.2 kg/year
    assert abs(result - expected) < 0.01

def test_calculate_transportation_with_flights():
    result = calculate_transportation({
        "vehicle_type": "ev",
        "km_per_month": 500,
        "flights_short_haul": 2,
        "flights_long_haul": 1
    })
    
    vehicle_emissions = 500 * 0.053 * 12
    flight_emissions = (2 * 255) + (1 * 1240)
    expected = vehicle_emissions + flight_emissions
    
    assert abs(result - expected) < 0.01
```

### Integration Tests

```python
# tests/test_api_carbon.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers(test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "TestPass123!"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_calculate_footprint(auth_headers):
    response = client.post(
        "/api/v1/carbon/calculate",
        json={
            "transportation": {
                "vehicle_type": "car_petrol",
                "km_per_month": 600
            },
            "energy": {...},
            "food": {...},
            "shopping": {...},
            "waste": {...}
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "carbon_score" in data
    assert data["carbon_score"]["monthly_kg"] > 0
    assert data["carbon_score"]["grade"] in ["EXCELLENT", "GOOD", "MODERATE", "HIGH", "CRITICAL"]
```

---

## Frontend Testing (Jest + React Testing Library)

### Component Tests

```typescript
// components/CarbonScoreCard.test.tsx
import { render, screen } from '@testing-library/react';
import { CarbonScoreCard } from './CarbonScoreCard';

describe('CarbonScoreCard', () => {
  it('renders carbon footprint data correctly', () => {
    render(
      <CarbonScoreCard
        monthlyKg={387}
        annualTons={4.64}
        grade="GOOD"
        gradeColor="#34D399"
      />
    );
    
    expect(screen.getByText('387 kg CO2e')).toBeInTheDocument();
    expect(screen.getByText('4.64 tons CO2e')).toBeInTheDocument();
    expect(screen.getByText('GOOD')).toBeInTheDocument();
  });
});
```

### E2E Tests (Playwright)

```typescript
// e2e/carbon-calculation.spec.ts
import { test, expect } from '@playwright/test';

test('complete carbon footprint calculation flow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'TestPass123!');
  await page.click('button[type="submit"]');
  
  // Navigate to calculator
  await page.goto('/calculator');
  
  // Fill transportation
  await page.selectOption('[name="vehicle_type"]', 'car_petrol');
  await page.fill('[name="km_per_month"]', '600');
  await page.click('button:has-text("Next")');
  
  // Fill energy
  await page.fill('[name="electricity_kwh_per_month"]', '350');
  await page.click('button:has-text("Next")');
  
  // ... fill other categories ...
  
  // Submit and verify results
  await page.click('button:has-text("Calculate")');
  
  await expect(page.locator('text=Your Carbon Footprint')).toBeVisible();
  await expect(page.locator('text=kg CO2e')).toBeVisible();
  await expect(page.locator('[data-testid="carbon-grade"]')).toHaveText(/EXCELLENT|GOOD|MODERATE|HIGH|CRITICAL/);
});
```

---

## Test Coverage Goals

- **Backend:** 80%+ code coverage
- **Frontend:** 70%+ code coverage
- **E2E:** Critical user flows (10 scenarios minimum)

---

**Document Owner:** QA Team  
**Last Updated:** June 17, 2026
