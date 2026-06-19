# Frontend & Backend Implementation Guide
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Status:** Implementation Ready

---

## Frontend Architecture (Next.js 15)

### Project Structure

```
frontend/
├── src/
│   ├── app/                          # Next.js 15 App Router
│   │   ├── (auth)/                   # Auth route group
│   │   │   ├── login/page.tsx
│   │   │   ├── signup/page.tsx
│   │   │   └── callback/page.tsx
│   │   ├── (dashboard)/              # Dashboard route group
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── calculator/page.tsx
│   │   │   ├── advisor/page.tsx
│   │   │   ├── eco-twin/page.tsx
│   │   │   ├── analytics/page.tsx
│   │   │   ├── challenges/page.tsx
│   │   │   └── learning/page.tsx
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Landing page
│   │   ├── globals.css
│   │   └── api/                      # API routes
│   ├── components/
│   │   ├── ui/                       # ShadCN components
│   │   ├── dashboard/
│   │   │   ├── CarbonScoreCard.tsx
│   │   │   ├── BreakdownChart.tsx
│   │   │   └── RecommendationsList.tsx
│   │   ├── calculator/
│   │   │   ├── MultiStepForm.tsx
│   │   │   └── CategoryStep.tsx
│   │   ├── ai/
│   │   │   ├── ChatInterface.tsx
│   │   │   └── MessageBubble.tsx
│   │   └── shared/
│   ├── lib/
│   │   ├── api-client.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useCarbon.ts
│   │   └── useAI.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   └── carbonStore.ts
│   └── types/
│       └── index.ts
├── public/
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

### Key Components

#### Dashboard Components

**CarbonScoreCard.tsx**
```typescript
'use client';

import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface CarbonScoreCardProps {
  monthlyKg: number;
  annualTons: number;
  grade: string;
  gradeColor: string;
}

export function CarbonScoreCard({ 
  monthlyKg, 
  annualTons, 
  grade, 
  gradeColor 
}: CarbonScoreCardProps) {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Your Carbon Footprint</h2>
      <div className="space-y-4">
        <div>
          <p className="text-sm text-muted-foreground">Monthly</p>
          <p className="text-4xl font-bold">{monthlyKg} kg CO2e</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Annual</p>
          <p className="text-3xl font-semibold">{annualTons} tons CO2e</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Grade</p>
          <div 
            className="inline-block px-4 py-2 rounded-full font-bold"
            style={{ backgroundColor: gradeColor }}
          >
            {grade}
          </div>
        </div>
      </div>
    </Card>
  );
}
```

#### AI Chat Component

**ChatInterface.tsx**
```typescript
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAI } from '@/hooks/useAI';

export function ChatInterface({ conversationId }: { conversationId?: string }) {
  const [message, setMessage] = useState('');
  const { messages, sendMessage, isLoading } = useAI(conversationId);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    await sendMessage(message);
    setMessage('');
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask about sustainability..."
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading}>
            Send
          </Button>
        </div>
      </form>
    </div>
  );
}
```

### State Management (Zustand)

**carbonStore.ts**
```typescript
import { create } from 'zustand';

interface CarbonFootprint {
  id: string;
  monthlyKg: number;
  annualTons: number;
  grade: string;
  breakdown: Record<string, number>;
}

interface CarbonStore {
  footprint: CarbonFootprint | null;
  history: CarbonFootprint[];
  isLoading: boolean;
  error: string | null;
  
  fetchFootprint: () => Promise<void>;
  calculateFootprint: (data: any) => Promise<void>;
  fetchHistory: () => Promise<void>;
}

export const useCarbonStore = create<CarbonStore>((set) => ({
  footprint: null,
  history: [],
  isLoading: false,
  error: null,
  
  fetchFootprint: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/carbon/footprints/latest');
      set({ footprint: response.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  calculateFootprint: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/carbon/calculate', data);
      set({ footprint: response.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchHistory: async () => {
    try {
      const response = await apiClient.get('/carbon/footprints');
      set({ history: response.data.data });
    } catch (error) {
      set({ error: error.message });
    }
  }
}));
```

### API Client

**api-client.ts**
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Attempt token refresh
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {
          refresh_token: refreshToken
        });
        
        localStorage.setItem('access_token', response.data.access_token);
        error.config.headers.Authorization = `Bearer ${response.data.access_token}`;
        return axios(error.config);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## Backend Architecture (FastAPI)

### Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── carbon.py
│   │       ├── ai.py
│   │       ├── users.py
│   │       ├── recommendations.py
│   │       ├── gamification.py
│   │       └── analytics.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── cache.py
│   ├── models/
│   │   ├── user.py
│   │   ├── carbon_footprint.py
│   │   └── recommendation.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── carbon.py
│   │   └── ai.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── carbon_service.py
│   │   ├── ai_service.py
│   │   └── recommendation_service.py
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── carbon_engine.py
│   │   ├── advisor_agent.py
│   │   └── tools/
│   └── utils/
│       ├── carbon_calculations.py
│       └── validators.py
├── tests/
├── alembic/
├── requirements.txt
└── .env
```

### Main Application

**main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}
```

### Service Layer

**carbon_service.py**
```python
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.carbon_footprint import CarbonFootprint
from app.schemas.carbon import CarbonInput, CarbonResult
from app.agents.carbon_engine import CarbonEngine
from app.core.cache import cache

class CarbonService:
    def __init__(self, db: Session):
        self.db = db
        self.carbon_engine = CarbonEngine()
    
    async def calculate_footprint(
        self, 
        user_id: str, 
        data: CarbonInput
    ) -> CarbonResult:
        """Calculate carbon footprint using AI engine"""
        
        # Calculate using AI engine
        result = await self.carbon_engine.calculate(data)
        
        # Save to database
        footprint = CarbonFootprint(
            user_id=user_id,
            monthly_kg=result.monthly_kg,
            annual_tons=result.annual_tons,
            grade=result.grade,
            transportation_kg=result.breakdown.transportation,
            energy_kg=result.breakdown.energy,
            food_kg=result.breakdown.food,
            shopping_kg=result.breakdown.shopping,
            waste_kg=result.breakdown.waste
        )
        
        self.db.add(footprint)
        self.db.commit()
        self.db.refresh(footprint)
        
        # Update cache
        await cache.set(
            f"carbon:{user_id}:latest",
            result.dict(),
            expire=300
        )
        
        # Trigger recommendation generation
        await self._generate_recommendations(user_id, result)
        
        return result
    
    async def _generate_recommendations(
        self, 
        user_id: str, 
        footprint: CarbonResult
    ):
        """Generate recommendations based on footprint"""
        from app.services.recommendation_service import RecommendationService
        
        rec_service = RecommendationService(self.db)
        await rec_service.generate_for_user(user_id, footprint)
```

### API Router

**carbon.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.carbon import CarbonInput, CarbonResult
from app.services.carbon_service import CarbonService
from app.models.user import User

router = APIRouter()

@router.post("/calculate", response_model=CarbonResult, status_code=201)
async def calculate_footprint(
    data: CarbonInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate carbon footprint"""
    service = CarbonService(db)
    try:
        result = await service.calculate_footprint(current_user.id, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/footprints", response_model=List[CarbonResult])
async def get_footprints(
    page: int = 1,
    page_size: int = 12,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's carbon footprint history"""
    service = CarbonService(db)
    return await service.get_history(
        current_user.id, 
        page=page, 
        page_size=page_size
    )
```

### AI Agent Implementation

**carbon_engine.py**
```python
from anthropic import AsyncAnthropic
from app.schemas.carbon import CarbonInput, CarbonResult
from app.utils.carbon_calculations import EmissionFactors

class CarbonEngine:
    def __init__(self):
        self.client = AsyncAnthropic()
        self.model = "claude-opus-4.5"
    
    async def calculate(self, data: CarbonInput) -> CarbonResult:
        """Calculate carbon footprint using AI-enhanced logic"""
        
        # Calculate base emissions
        transportation = self._calculate_transportation(data.transportation)
        energy = self._calculate_energy(data.energy)
        food = self._calculate_food(data.food)
        shopping = self._calculate_shopping(data.shopping)
        waste = self._calculate_waste(data.waste)
        
        # Total annual emissions
        total_kg = transportation + energy + food + shopping + waste
        annual_tons = total_kg / 1000
        monthly_kg = total_kg / 12
        
        # Assign grade
        grade = self._assign_grade(annual_tons)
        
        # Use AI for insights
        insights = await self._generate_insights(data, total_kg)
        
        return CarbonResult(
            monthly_kg=monthly_kg,
            annual_tons=annual_tons,
            grade=grade["grade"],
            grade_score=grade["score"],
            breakdown={
                "transportation": transportation,
                "energy": energy,
                "food": food,
                "shopping": shopping,
                "waste": waste
            },
            insights=insights
        )
    
    def _calculate_transportation(self, data: dict) -> float:
        """Calculate transportation emissions"""
        factors = EmissionFactors.TRANSPORTATION
        
        # Vehicle emissions
        vehicle_kg = 0
        if data.get("vehicle_type") and data.get("km_per_month"):
            factor = factors[data["vehicle_type"]]
            vehicle_kg = data["km_per_month"] * factor * 12
        
        # Flight emissions
        flight_kg = (
            data.get("flights_short_haul", 0) * 255 +
            data.get("flights_long_haul", 0) * 1240
        )
        
        return vehicle_kg + flight_kg
    
    async def _generate_insights(
        self, 
        data: CarbonInput, 
        total_kg: float
    ) -> List[str]:
        """Generate AI-powered insights"""
        
        prompt = f"""
        Analyze this carbon footprint data and provide 3 key insights:
        
        Total emissions: {total_kg} kg CO2e/year
        Data: {data.dict()}
        
        Provide brief, actionable insights.
        """
        
        response = await self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        # Parse insights from response
        return self._parse_insights(response.content[0].text)
```

---

## Security Implementation

### JWT Authentication

**security.py**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

---

**Document Owner:** Engineering Team  
**Last Updated:** June 17, 2026  
**Status:** APPROVED FOR IMPLEMENTATION
