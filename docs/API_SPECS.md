# API Specifications
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Base URL:** `https://api.footprintiq.com`  
**API Version:** `/api/v1`  
**Status:** Implementation Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Common Patterns](#common-patterns)
4. [Authentication Endpoints](#authentication-endpoints)
5. [User Management Endpoints](#user-management-endpoints)
6. [Carbon Calculation Endpoints](#carbon-calculation-endpoints)
7. [AI Agent Endpoints](#ai-agent-endpoints)
8. [Recommendation Endpoints](#recommendation-endpoints)
9. [Gamification Endpoints](#gamification-endpoints)
10. [Analytics Endpoints](#analytics-endpoints)
11. [Admin Endpoints](#admin-endpoints)
12. [WebSocket API](#websocket-api)
13. [Error Handling](#error-handling)
14. [Rate Limiting](#rate-limiting)

---

## Overview

### API Design Principles

1. **RESTful:** Follow REST conventions
2. **JSON:** All requests and responses use JSON
3. **Versioned:** API version in URL path
4. **Secure:** HTTPS only, OAuth 2.0 + JWT
5. **Documented:** OpenAPI 3.0 specification
6. **Paginated:** Consistent pagination for lists
7. **Filtered:** Query parameters for filtering
8. **Cached:** ETags and cache headers

### Base URL Structure

```
Production:  https://api.footprintiq.com/api/v1
Staging:     https://api-staging.footprintiq.com/api/v1
Development: http://localhost:8000/api/v1
```

### Content Type

All requests must include:
```
Content-Type: application/json
Accept: application/json
```

---

## Authentication

### OAuth 2.0 + JWT Flow

**Supported Providers:**
- Google OAuth 2.0
- GitHub OAuth (future)
- Email/Password (traditional)

### JWT Token Structure

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900,
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "scope": "read write"
}
```

### Authorization Header

```
Authorization: Bearer <access_token>
```

### Token Expiry

- **Access Token:** 15 minutes
- **Refresh Token:** 7 days

---

## Common Patterns

### Pagination

**Request Parameters:**
```
GET /api/v1/resource?page=1&page_size=20
```

**Response Structure:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8,
    "has_next": true,
    "has_previous": false
  }
}
```

### Filtering

```
GET /api/v1/carbon/footprints?category=transportation&grade=HIGH
```

### Sorting

```
GET /api/v1/recommendations?sort_by=priority_score&order=desc
```

### Field Selection

```
GET /api/v1/users/me?fields=id,username,email
```

---

## Authentication Endpoints

### POST /api/v1/auth/register

Register a new user account.

**Request:**
```json
{
  "email": "john.doe@email.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@email.com",
    "username": "johndoe",
    "email_verified": false,
    "created_at": "2026-06-17T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

**Errors:**
- `400`: Validation error (email format, weak password)
- `409`: Email or username already exists

---

### POST /api/v1/auth/login

Login with email and password.

**Request:**
```json
{
  "email": "john.doe@email.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@email.com",
    "username": "johndoe",
    "role": "user"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

**Errors:**
- `401`: Invalid credentials
- `403`: Account not active

---

### POST /api/v1/auth/oauth/google

Authenticate with Google OAuth.

**Request:**
```json
{
  "code": "4/0AX4XfWh...",
  "redirect_uri": "https://footprintiq.com/auth/callback"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@gmail.com",
    "username": "johndoe",
    "oauth_provider": "google",
    "avatar_url": "https://lh3.googleusercontent.com/..."
  },
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

### POST /api/v1/auth/refresh

Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

### POST /api/v1/auth/logout

Logout and invalidate tokens.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

## User Management Endpoints

### GET /api/v1/users/me

Get current authenticated user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@email.com",
  "username": "johndoe",
  "profile": {
    "full_name": "John Doe",
    "avatar_url": "https://...",
    "country_code": "USA",
    "timezone": "America/New_York",
    "preferred_language": "en",
    "preferred_units": "metric"
  },
  "carbon_footprint": {
    "monthly_kg": 387.00,
    "annual_tons": 4.64,
    "grade": "GOOD",
    "last_updated": "2026-06-15T14:20:00Z"
  },
  "gamification": {
    "points": 1250,
    "level": 5,
    "badges_unlocked": 12,
    "current_streak": 7
  },
  "created_at": "2026-01-15T09:00:00Z"
}
```

---

### PUT /api/v1/users/me

Update current user profile.

**Request:**
```json
{
  "profile": {
    "full_name": "John A. Doe",
    "country_code": "USA",
    "timezone": "America/New_York",
    "preferred_language": "en"
  },
  "preferences": {
    "notifications": {
      "email": true,
      "push": true,
      "weekly_summary": true
    },
    "privacy": {
      "show_on_leaderboard": true,
      "profile_public": false
    }
  }
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "profile": {...},
  "preferences": {...},
  "updated_at": "2026-06-17T11:00:00Z"
}
```

---

### GET /api/v1/users/{user_id}

Get public user profile (if public).

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "avatar_url": "https://...",
  "level": 5,
  "total_co2_saved": 250.5,
  "badges_count": 12,
  "joined_date": "2026-01-15"
}
```

**Errors:**
- `404`: User not found
- `403`: Profile is private

---

## Carbon Calculation Endpoints

### POST /api/v1/carbon/calculate

Calculate carbon footprint.

**Request:**
```json
{
  "transportation": {
    "vehicle_type": "car_petrol",
    "km_per_month": 600,
    "public_transport_frequency": "rarely",
    "flights_short_haul": 2,
    "flights_long_haul": 1,
    "bicycle_walking_pct": 10
  },
  "energy": {
    "electricity_kwh_per_month": 350,
    "renewable_energy_pct": 20,
    "ac_usage": "moderate",
    "heating_type": "gas",
    "household_size": 2
  },
  "food": {
    "diet_type": "meat_occasional",
    "dairy_consumption": "medium",
    "food_waste": "average",
    "local_produce": "sometimes"
  },
  "shopping": {
    "clothing_items_per_month": 2,
    "electronics_per_year": 1,
    "online_deliveries_per_month": 8,
    "second_hand_preference": "sometimes"
  },
  "waste": {
    "recycling_frequency": "often",
    "composting": false,
    "plastic_usage": "average",
    "water_bottle_type": "reusable"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": "footprint_123",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "carbon_score": {
    "monthly_kg": 387.00,
    "annual_tons": 4.64,
    "grade": "GOOD",
    "grade_score": 72,
    "grade_color": "#34D399"
  },
  "breakdown": {
    "transportation": {
      "kg_annual": 1950.00,
      "percentage": 42,
      "grade": "HIGH"
    },
    "energy": {
      "kg_annual": 1300.00,
      "percentage": 28,
      "grade": "MODERATE"
    },
    "food": {
      "kg_annual": 840.00,
      "percentage": 18,
      "grade": "GOOD"
    },
    "shopping": {
      "kg_annual": 370.00,
      "percentage": 8,
      "grade": "GOOD"
    },
    "waste": {
      "kg_annual": 180.00,
      "percentage": 4,
      "grade": "EXCELLENT"
    }
  },
  "comparisons": {
    "country_average": {
      "tons": 5.2,
      "difference_pct": -10.8,
      "status": "below_average"
    },
    "global_average": {
      "tons": 4.5,
      "difference_pct": 3.1,
      "status": "above_average"
    },
    "target_2c": {
      "tons": 2.0,
      "difference_pct": 132.0,
      "status": "above_target"
    }
  },
  "insights": [
    "Transportation is your highest emission category at 42%",
    "Your energy usage is near the national average",
    "Great job on waste management!"
  ],
  "created_at": "2026-06-17T11:30:00Z"
}
```

---

### GET /api/v1/carbon/footprints

Get user's carbon footprint history.

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 12)
- `from_date`: Start date (ISO 8601)
- `to_date`: End date (ISO 8601)

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "footprint_123",
      "monthly_kg": 387.00,
      "annual_tons": 4.64,
      "grade": "GOOD",
      "created_at": "2026-06-17T11:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 12,
    "total_items": 24,
    "total_pages": 2
  }
}
```

---

### GET /api/v1/carbon/footprints/{footprint_id}

Get specific carbon footprint details.

**Response:** `200 OK`
```json
{
  "id": "footprint_123",
  "carbon_score": {...},
  "breakdown": {...},
  "comparisons": {...},
  "input_data": {...},
  "created_at": "2026-06-17T11:30:00Z"
}
```

---

### GET /api/v1/carbon/trends

Get carbon footprint trends.

**Query Parameters:**
- `period`: "week" | "month" | "quarter" | "year"
- `metric`: "monthly_kg" | "annual_tons"

**Response:** `200 OK`
```json
{
  "period": "month",
  "data_points": [
    {
      "date": "2026-01-01",
      "value": 420.5,
      "grade": "MODERATE"
    },
    {
      "date": "2026-02-01",
      "value": 395.2,
      "grade": "GOOD"
    }
  ],
  "trend": {
    "direction": "decreasing",
    "change_pct": -6.0,
    "average": 405.3
  },
  "insights": [
    "You've reduced emissions by 6% over the past 6 months",
    "Transportation improvements driving the reduction"
  ]
}
```

---

## AI Agent Endpoints

### POST /api/v1/ai/chat

Send message to AI advisor.

**Request:**
```json
{
  "message": "How can I reduce my transportation emissions?",
  "conversation_id": "conv_456",
  "context": {
    "page": "dashboard",
    "referencing": "carbon_footprint"
  }
}
```

**Response:** `200 OK`
```json
{
  "message_id": "msg_789",
  "conversation_id": "conv_456",
  "role": "assistant",
  "content": "Based on your 30km daily commute...",
  "suggestions": [
    "Tell me more about public transport",
    "Show me cost comparison",
    "Run Eco Twin simulation"
  ],
  "related_content": [
    {
      "type": "article",
      "title": "Public Transport Benefits",
      "url": "/learning/public-transport"
    }
  ],
  "metadata": {
    "tokens_used": 450,
    "latency_ms": 2100,
    "model": "claude-opus-4.5"
  },
  "created_at": "2026-06-17T11:45:00Z"
}
```

---

### POST /api/v1/ai/chat/stream

Stream AI response (Server-Sent Events).

**Request:**
```json
{
  "message": "Explain carbon offsetting",
  "conversation_id": "conv_456"
}
```

**Response:** `200 OK` (text/event-stream)
```
event: token
data: {"content": "Carbon"}

event: token
data: {"content": " offsetting"}

event: token
data: {"content": " is"}

event: complete
data: {"message_id": "msg_790", "total_tokens": 450}
```

---

### GET /api/v1/ai/conversations

Get user's conversation history.

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "conv_456",
      "title": "Transportation Emissions Help",
      "message_count": 12,
      "last_message_at": "2026-06-17T11:45:00Z",
      "created_at": "2026-06-15T09:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### GET /api/v1/ai/conversations/{conversation_id}/messages

Get conversation messages.

**Response:** `200 OK`
```json
{
  "conversation_id": "conv_456",
  "messages": [
    {
      "id": "msg_788",
      "role": "user",
      "content": "How can I reduce emissions?",
      "created_at": "2026-06-17T11:44:00Z"
    },
    {
      "id": "msg_789",
      "role": "assistant",
      "content": "Based on your profile...",
      "created_at": "2026-06-17T11:45:00Z"
    }
  ]
}
```

---

## Recommendation Endpoints

### GET /api/v1/recommendations

Get personalized recommendations.

**Query Parameters:**
- `status`: "active" | "accepted" | "completed"
- `category`: "transportation" | "energy" | "food" | "shopping" | "waste"
- `difficulty`: "easy" | "medium" | "hard"
- `sort_by`: "priority_score" | "co2_savings" | "created_at"

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "rec_101",
      "title": "Use Public Transport 2 Days per Week",
      "description": "Switch to public transport for your commute...",
      "category": "transportation",
      "impact": {
        "co2_savings_kg_annual": 340.0,
        "co2_savings_percentage": 18.0,
        "financial_savings_annual": 1800.0
      },
      "feasibility": {
        "difficulty": "easy",
        "cost_impact": "saves_money",
        "time_to_implement": "immediate"
      },
      "implementation_steps": [
        "Download transit app",
        "Plan route",
        "Purchase monthly pass",
        "Set reminders"
      ],
      "priority_score": 92,
      "status": "active",
      "created_at": "2026-06-17T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### POST /api/v1/recommendations/{recommendation_id}/actions

Take action on recommendation.

**Request:**
```json
{
  "action": "accept",
  "notes": "Starting with Tuesday/Thursday"
}
```

**Actions:** `accept`, `reject`, `start`, `complete`, `pause`

**Response:** `200 OK`
```json
{
  "recommendation_id": "rec_101",
  "action": "accept",
  "status": "accepted",
  "points_earned": 50,
  "accepted_at": "2026-06-17T12:00:00Z"
}
```

---

### POST /api/v1/recommendations/generate

Request new recommendations.

**Request:**
```json
{
  "category": "transportation",
  "max_difficulty": "medium",
  "focus": "quick_wins"
}
```

**Response:** `200 OK`
```json
{
  "recommendations": [...],
  "generation_time_ms": 1500,
  "personalization_score": 0.92
}
```

---

## Eco Twin Endpoints

### POST /api/v1/eco-twin/simulate

Run Eco Twin scenario simulation.

**Request:**
```json
{
  "scenario_name": "Go Electric",
  "changes": [
    {
      "category": "transportation",
      "change_type": "replace_vehicle",
      "from": "car_petrol",
      "to": "ev"
    },
    {
      "category": "energy",
      "change_type": "add_renewable",
      "details": {
        "solar_panels_kwh": 5
      }
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "simulation_id": "sim_202",
  "scenario_name": "Go Electric",
  "baseline": {
    "annual_tons": 4.64,
    "monthly_kg": 387.0
  },
  "simulated": {
    "annual_tons": 1.85,
    "monthly_kg": 154.2
  },
  "impact": {
    "reduction_tons": 2.79,
    "reduction_percentage": 60.1,
    "equivalent_trees": 127
  },
  "financial": {
    "upfront_cost": 45000,
    "annual_savings": 2400,
    "payback_period_years": 18.75,
    "lifetime_savings_10yr": -21000
  },
  "feasibility": {
    "difficulty_score": 75,
    "timeline_months": 3,
    "ai_recommendation_score": 68
  },
  "created_at": "2026-06-17T12:15:00Z"
}
```

---

### GET /api/v1/eco-twin/simulations

Get user's simulation history.

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "sim_202",
      "scenario_name": "Go Electric",
      "reduction_percentage": 60.1,
      "created_at": "2026-06-17T12:15:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### GET /api/v1/eco-twin/scenarios

Get pre-built scenarios.

**Response:** `200 OK`
```json
{
  "scenarios": [
    {
      "id": "scenario_ev",
      "name": "Go Fully Electric",
      "description": "Switch to EV and install solar panels",
      "expected_reduction_pct": 65,
      "difficulty": "hard",
      "estimated_cost": "$40,000-$60,000"
    },
    {
      "id": "scenario_plant_based",
      "name": "Plant-Based Diet",
      "description": "Switch to vegan diet",
      "expected_reduction_pct": 15,
      "difficulty": "medium",
      "estimated_cost": "Neutral"
    }
  ]
}
```

---

## Gamification Endpoints

### GET /api/v1/gamification/points

Get user's points and level.

**Response:** `200 OK`
```json
{
  "points": 1250,
  "level": 5,
  "level_progress": 45,
  "next_level_points": 1500,
  "total_points_earned": 2100,
  "badges_unlocked": 12,
  "challenges_completed": 8,
  "current_streak": 7,
  "longest_streak": 14
}
```

---

### GET /api/v1/gamification/badges

Get available and earned badges.

**Query Parameters:**
- `status`: "unlocked" | "locked" | "all"

**Response:** `200 OK`
```json
{
  "badges": [
    {
      "id": "badge_001",
      "name": "carbon_curious",
      "display_name": "Carbon Curious",
      "description": "Complete your first calculation",
      "icon_url": "/badges/curious.svg",
      "category": "engagement",
      "rarity": "common",
      "points_awarded": 50,
      "unlocked": true,
      "unlocked_at": "2026-06-15T10:00:00Z",
      "progress": 100
    },
    {
      "id": "badge_002",
      "name": "week_streak",
      "display_name": "7-Day Streak",
      "description": "Log in for 7 consecutive days",
      "icon_url": "/badges/streak7.svg",
      "category": "engagement",
      "rarity": "common",
      "points_awarded": 100,
      "unlocked": true,
      "unlocked_at": "2026-06-17T09:00:00Z",
      "progress": 100
    },
    {
      "id": "badge_003",
      "name": "co2_reducer",
      "display_name": "Carbon Cutter",
      "description": "Reduce footprint by 10%",
      "icon_url": "/badges/reducer.svg",
      "category": "carbon_reduction",
      "rarity": "rare",
      "points_awarded": 250,
      "unlocked": false,
      "progress": 65
    }
  ]
}
```

---

### GET /api/v1/gamification/challenges

Get available challenges.

**Query Parameters:**
- `status`: "available" | "active" | "completed"
- `type`: "daily" | "weekly" | "monthly" | "one_time"

**Response:** `200 OK`
```json
{
  "challenges": [
    {
      "id": "challenge_101",
      "name": "green_commute_week",
      "display_name": "Green Commute Challenge",
      "description": "Use public transport or bike for 5 days",
      "category": "transportation",
      "type": "weekly",
      "duration_days": 7,
      "points_reward": 500,
      "badge_reward": null,
      "start_date": "2026-06-17",
      "end_date": "2026-06-24",
      "participant_count": 1245,
      "user_status": "active",
      "user_progress": {
        "trips_completed": 3,
        "trips_required": 5,
        "progress_pct": 60
      }
    }
  ]
}
```

---

### POST /api/v1/gamification/challenges/{challenge_id}/join

Join a challenge.

**Response:** `200 OK`
```json
{
  "challenge_id": "challenge_101",
  "status": "active",
  "started_at": "2026-06-17T13:00:00Z"
}
```

---

### GET /api/v1/gamification/leaderboard

Get leaderboard rankings.

**Query Parameters:**
- `type`: "global" | "country" | "friends"
- `period`: "daily" | "weekly" | "monthly" | "all_time"
- `metric`: "points" | "reduction_pct" | "co2_saved"

**Response:** `200 OK`
```json
{
  "leaderboard_type": "global",
  "period": "weekly",
  "metric": "points",
  "period_start": "2026-06-10",
  "period_end": "2026-06-17",
  "current_user_rank": 42,
  "rankings": [
    {
      "rank": 1,
      "user": {
        "id": "user_001",
        "username": "eco_warrior",
        "avatar_url": "https://...",
        "level": 12
      },
      "score": 2450,
      "percentile": 99.5
    },
    {
      "rank": 2,
      "user": {
        "id": "user_002",
        "username": "green_hero",
        "avatar_url": "https://...",
        "level": 10
      },
      "score": 2180,
      "percentile": 98.2
    }
  ],
  "total_participants": 10523
}
```

---

## Analytics Endpoints

### GET /api/v1/analytics/dashboard

Get dashboard analytics summary.

**Query Parameters:**
- `period`: "week" | "month" | "quarter" | "year"

**Response:** `200 OK`
```json
{
  "period": "month",
  "carbon_metrics": {
    "current_footprint": 387.0,
    "previous_footprint": 420.5,
    "change_pct": -7.97,
    "trend": "improving",
    "grade": "GOOD"
  },
  "engagement": {
    "login_days": 18,
    "calculations_performed": 4,
    "ai_conversations": 12,
    "articles_read": 8
  },
  "achievements": {
    "points_earned": 450,
    "badges_unlocked": 2,
    "challenges_completed": 1,
    "recommendations_completed": 3
  },
  "impact": {
    "total_co2_saved_kg": 125.5,
    "equivalent_trees": 6,
    "equivalent_car_km": 734
  }
}
```

---

### GET /api/v1/analytics/breakdown

Get detailed category breakdown.

**Query Parameters:**
- `period`: "month" | "quarter" | "year"

**Response:** `200 OK`
```json
{
  "period": "month",
  "categories": [
    {
      "category": "transportation",
      "current_kg": 162.5,
      "previous_kg": 175.0,
      "change_pct": -7.14,
      "percentage_of_total": 42,
      "trend": "decreasing",
      "breakdown": {
        "car": 140.0,
        "public_transport": 15.5,
        "flights": 7.0
      }
    }
  ],
  "total_current": 387.0,
  "total_previous": 420.5
}
```

---

### GET /api/v1/analytics/predictions

Get future emissions predictions.

**Query Parameters:**
- `timeframe`: "30d" | "90d" | "1y"

**Response:** `200 OK`
```json
{
  "timeframe": "90d",
  "predictions": [
    {
      "date": "2026-07-17",
      "predicted_kg": 375.2,
      "confidence_80": [360.1, 390.3],
      "confidence_95": [345.0, 405.4]
    }
  ],
  "trend": "decreasing",
  "projected_reduction_pct": 3.0,
  "confidence_score": 0.85,
  "assumptions": [
    "Current behavior patterns continue",
    "Seasonal factors accounted for",
    "Accepted recommendations implemented"
  ]
}
```

---

### POST /api/v1/analytics/export

Export user data.

**Request:**
```json
{
  "format": "pdf",
  "include": [
    "carbon_footprints",
    "recommendations",
    "analytics"
  ],
  "date_range": {
    "from": "2026-01-01",
    "to": "2026-06-17"
  }
}
```

**Formats:** `pdf`, `csv`, `json`

**Response:** `202 Accepted`
```json
{
  "export_id": "export_303",
  "status": "processing",
  "estimated_completion": "2026-06-17T13:30:00Z"
}
```

---

### GET /api/v1/analytics/exports/{export_id}

Check export status and download.

**Response:** `200 OK`
```json
{
  "export_id": "export_303",
  "status": "completed",
  "download_url": "https://s3.../export_303.pdf",
  "expires_at": "2026-06-18T13:30:00Z",
  "file_size_bytes": 524288,
  "created_at": "2026-06-17T13:25:00Z"
}
```

---

## Learning Content Endpoints

### GET /api/v1/learning/content

Get learning content list.

**Query Parameters:**
- `category`: "basics" | "transportation" | "energy" | "food"
- `difficulty`: "beginner" | "intermediate" | "advanced"
- `content_type`: "article" | "video" | "quiz"

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "content_401",
      "title": "Understanding Your Carbon Footprint",
      "slug": "understanding-carbon-footprint",
      "description": "Learn the basics...",
      "category": "basics",
      "difficulty": "beginner",
      "content_type": "article",
      "thumbnail_url": "https://...",
      "estimated_read_time": 5,
      "tags": ["basics", "carbon", "intro"],
      "view_count": 15234,
      "like_count": 892,
      "is_featured": true
    }
  ],
  "pagination": {...}
}
```

---

### GET /api/v1/learning/content/{content_id}

Get specific content.

**Response:** `200 OK`
```json
{
  "id": "content_401",
  "title": "Understanding Your Carbon Footprint",
  "content": "# Introduction\n\nYour carbon footprint...",
  "metadata": {...},
  "related_content": [...]
}
```

---

### GET /api/v1/learning/quizzes

Get available quizzes.

**Response:** `200 OK`
```json
{
  "quizzes": [
    {
      "id": "quiz_501",
      "title": "Carbon Basics Quiz",
      "category": "basics",
      "difficulty": "beginner",
      "question_count": 10,
      "total_points": 100,
      "passing_score": 70,
      "average_score": 82.5,
      "attempt_count": 3421,
      "user_best_score": 85,
      "user_attempts": 2
    }
  ]
}
```

---

### POST /api/v1/learning/quizzes/{quiz_id}/attempts

Submit quiz attempt.

**Request:**
```json
{
  "answers": [
    {
      "question_id": "q1",
      "answer": "Bicycle"
    }
  ],
  "time_taken_seconds": 180
}
```

**Response:** `200 OK`
```json
{
  "attempt_id": "attempt_601",
  "score": 85,
  "total_possible": 100,
  "percentage": 85.0,
  "passed": true,
  "correct_answers": 8,
  "wrong_answers": 2,
  "points_earned": 50,
  "results": [
    {
      "question_id": "q1",
      "correct": true,
      "user_answer": "Bicycle",
      "explanation": "Bicycles have zero direct emissions..."
    }
  ]
}
```

---

## Admin Endpoints

### GET /api/v1/admin/users

Get all users (admin only).

**Query Parameters:**
- `page`, `page_size`
- `role`: "user" | "premium" | "admin"
- `is_active`: true | false

**Response:** `200 OK`
```json
{
  "data": [...],
  "pagination": {...}
}
```

---

### GET /api/v1/admin/analytics

Get platform-wide analytics.

**Response:** `200 OK`
```json
{
  "users": {
    "total": 52341,
    "active_today": 12453,
    "new_this_week": 834
  },
  "carbon": {
    "total_calculations": 145632,
    "total_co2_saved_tons": 12453.5
  },
  "engagement": {
    "avg_session_duration_minutes": 12.5,
    "avg_calculations_per_user": 2.8
  }
}
```

---

## WebSocket API

### Connection

**URL:** `wss://api.footprintiq.com/ws`

**Authentication:**
```
wss://api.footprintiq.com/ws?token=<access_token>
```

### Message Format

**Client → Server:**
```json
{
  "type": "subscribe",
  "channel": "ai_chat",
  "conversation_id": "conv_456"
}
```

**Server → Client:**
```json
{
  "type": "ai_token",
  "conversation_id": "conv_456",
  "content": "Based on"
}
```

### Channels

- `ai_chat`: Real-time AI responses
- `notifications`: User notifications
- `leaderboard`: Leaderboard updates
- `challenges`: Challenge progress

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_12345",
    "timestamp": "2026-06-17T14:00:00Z"
  }
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `500`: Internal Server Error
- `503`: Service Unavailable

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## Rate Limiting

### Limits

**Tier: Free User**
- 100 requests / hour
- 10 AI chat messages / hour
- 5 carbon calculations / day

**Tier: Premium User**
- 1000 requests / hour
- 100 AI chat messages / hour
- Unlimited calculations

### Headers

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1655478000
```

### Rate Limit Exceeded Response

**Status:** `429 Too Many Requests`
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "retry_after": 3600
  }
}
```

---

**Document Owner:** API Team  
**Last Updated:** June 17, 2026  
**Interactive Docs:** https://api.footprintiq.com/docs  
**Status:** APPROVED FOR IMPLEMENTATION
