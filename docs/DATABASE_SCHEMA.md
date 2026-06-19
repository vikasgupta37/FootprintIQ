# Database Schema & ER Diagram
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Database:** PostgreSQL 15+  
**Status:** Implementation Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Core Tables](#core-tables)
4. [Detailed Schema](#detailed-schema)
5. [Indexes](#indexes)
6. [Relationships](#relationships)
7. [Sample Queries](#sample-queries)
8. [Migration Strategy](#migration-strategy)

---

## Overview

### Database Design Principles

1. **Normalization:** 3NF (Third Normal Form) for data integrity
2. **Performance:** Strategic denormalization where needed
3. **Scalability:** Partitioning strategy for large tables
4. **Auditability:** Timestamps on all tables
5. **Soft Deletes:** Logical deletion with `deleted_at` column

### Key Statistics (Projected)

- **Total Tables:** 25
- **Core Entities:** 15
- **Lookup Tables:** 5
- **Junction Tables:** 5
- **Expected Data Volume:**
  - Users: 200K+ (Year 1)
  - Carbon Footprints: 2.4M+ records
  - Conversations: 500K+
  - Messages: 5M+

---

## Entity Relationship Diagram

### High-Level ER Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USERS DOMAIN                                 │
│                                                                      │
│  ┌──────────────┐         ┌──────────────┐      ┌──────────────┐  │
│  │    users     │◄────────┤user_profiles │      │    roles     │  │
│  └──────┬───────┘         └──────────────┘      └──────┬───────┘  │
│         │                                                │          │
│         │                                                │          │
└─────────┼────────────────────────────────────────────────┼──────────┘
          │                                                │
          │                                                │
┌─────────┼────────────────────────────────────────────────┼──────────┐
│         │            CARBON DOMAIN                       │          │
│         │                                                │          │
│         ↓                                                ↓          │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │carbon_footprints │◄───────┤  carbon_inputs   │                  │
│  └────────┬─────────┘        └──────────────────┘                  │
│           │                                                          │
│           │                  ┌──────────────────┐                  │
│           └──────────────────┤carbon_categories │                  │
│                              └──────────────────┘                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      AI & RECOMMENDATIONS DOMAIN                     │
│                                                                      │
│  ┌──────────────┐         ┌──────────────────┐                     │
│  │conversations │◄────────┤    messages      │                     │
│  └──────┬───────┘         └──────────────────┘                     │
│         │                                                            │
│         │                 ┌──────────────────┐                     │
│         │                 │ recommendations  │                     │
│         │                 └────────┬─────────┘                     │
│         │                          │                                │
│         │                          │                                │
│         │                 ┌────────▼─────────┐                     │
│         │                 │recommendation_   │                     │
│         │                 │  actions         │                     │
│         │                 └──────────────────┘                     │
│         │                                                            │
└─────────┼──────────────────────────────────────────────────────────┘
          │
          │
┌─────────┼──────────────────────────────────────────────────────────┐
│         │           GAMIFICATION DOMAIN                             │
│         │                                                            │
│         ↓                                                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│  │user_points   │    │user_badges   │    │user_challenges│         │
│  └──────────────┘    └──────┬───────┘    └──────┬───────┘         │
│                              │                    │                  │
│                      ┌───────▼────────┐   ┌──────▼───────┐         │
│                      │    badges      │   │  challenges  │         │
│                      └────────────────┘   └──────────────┘         │
│                                                                      │
│  ┌──────────────────┐                                               │
│  │  leaderboards    │                                               │
│  └──────────────────┘                                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      LEARNING & CONTENT DOMAIN                       │
│                                                                      │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │learning_content  │◄───────┤  content_views   │                  │
│  └────────┬─────────┘        └──────────────────┘                  │
│           │                                                          │
│           │                  ┌──────────────────┐                  │
│           └──────────────────┤     quizzes      │                  │
│                              └────────┬─────────┘                  │
│                                       │                              │
│                              ┌────────▼─────────┐                  │
│                              │  quiz_attempts   │                  │
│                              └──────────────────┘                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        ECO TWIN DOMAIN                               │
│                                                                      │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │  eco_twin_states │        │  eco_twin_       │                  │
│  │                  │◄───────┤  simulations     │                  │
│  └──────────────────┘        └──────────────────┘                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      ANALYTICS & AUDIT DOMAIN                        │
│                                                                      │
│  ┌──────────────────┐        ┌──────────────────┐                  │
│  │  user_analytics  │        │   audit_logs     │                  │
│  └──────────────────┘        └──────────────────┘                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Core Tables

### Primary Entities

1. **users** - User accounts and authentication
2. **user_profiles** - Extended user information
3. **carbon_footprints** - Calculated carbon footprints
4. **carbon_inputs** - Raw input data for calculations
5. **recommendations** - AI-generated recommendations
6. **conversations** - AI chat conversations
7. **messages** - Individual chat messages
8. **badges** - Achievement badges
9. **challenges** - Sustainability challenges
10. **learning_content** - Educational content
11. **eco_twin_states** - Eco Twin virtual models
12. **leaderboards** - Community rankings

---

## Detailed Schema

### Table: users

**Purpose:** Core user authentication and account information

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),  -- NULL for OAuth users
    oauth_provider VARCHAR(50),  -- 'google', 'github', etc.
    oauth_id VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    role_id UUID REFERENCES roles(id),
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT users_email_check CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Columns:**
- `id`: Unique identifier (UUID for scalability)
- `email`: User's email (unique, validated)
- `username`: Optional display name
- `password_hash`: BCrypt hashed password
- `oauth_provider`: OAuth provider name
- `oauth_id`: Provider's user ID
- `email_verified`: Email verification status
- `is_active`: Account active status
- `is_superuser`: Admin flag
- `role_id`: Foreign key to roles table
- `last_login_at`: Last login timestamp
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp
- `deleted_at`: Soft delete timestamp

**Sample Data:**
```sql
INSERT INTO users (email, username, oauth_provider, oauth_id, email_verified, role_id)
VALUES 
    ('john.doe@email.com', 'johndoe', 'google', 'google_123456', TRUE, 'role_uuid_here'),
    ('jane.smith@email.com', 'janesmith', 'google', 'google_789012', TRUE, 'role_uuid_here');
```

---

### Table: user_profiles

**Purpose:** Extended user profile information and preferences

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255),
    avatar_url TEXT,
    country_code VARCHAR(3),  -- ISO 3166-1 alpha-3
    timezone VARCHAR(50),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    
    -- Preferences
    preferred_language VARCHAR(10) DEFAULT 'en',
    preferred_units VARCHAR(10) DEFAULT 'metric',  -- 'metric' or 'imperial'
    notification_preferences JSONB DEFAULT '{"email": true, "push": true, "in_app": true}',
    privacy_settings JSONB DEFAULT '{"profile_public": false, "show_on_leaderboard": true}',
    
    -- Sustainability Profile
    sustainability_level VARCHAR(20) DEFAULT 'beginner',  -- 'beginner', 'intermediate', 'advanced'
    goals JSONB,  -- User-defined goals
    interests TEXT[],  -- Array of interest tags
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_country ON user_profiles(country_code);
```

**JSONB Examples:**
```json
// notification_preferences
{
  "email": true,
  "push": true,
  "in_app": true,
  "weekly_summary": true,
  "recommendations": true
}

// privacy_settings
{
  "profile_public": false,
  "show_on_leaderboard": true,
  "share_analytics": false
}

// goals
{
  "annual_reduction_target": 15,  // percentage
  "target_grade": "GOOD",
  "specific_goals": [
    "reduce_transportation_20",
    "zero_waste",
    "plant_based_diet"
  ]
}
```

---

### Table: carbon_footprints

**Purpose:** Stores calculated carbon footprint results

```sql
CREATE TABLE carbon_footprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Calculated Values
    monthly_kg DECIMAL(10, 2) NOT NULL,  -- kg CO2e per month
    annual_tons DECIMAL(10, 2) NOT NULL,  -- tons CO2e per year
    
    -- Grading
    grade VARCHAR(20) NOT NULL,  -- 'EXCELLENT', 'GOOD', 'MODERATE', 'HIGH', 'CRITICAL'
    grade_score INTEGER NOT NULL CHECK (grade_score BETWEEN 0 AND 100),
    
    -- Category Breakdown (kg CO2e annually)
    transportation_kg DECIMAL(10, 2) DEFAULT 0,
    energy_kg DECIMAL(10, 2) DEFAULT 0,
    food_kg DECIMAL(10, 2) DEFAULT 0,
    shopping_kg DECIMAL(10, 2) DEFAULT 0,
    waste_kg DECIMAL(10, 2) DEFAULT 0,
    
    -- Comparisons
    country_average_tons DECIMAL(10, 2),
    global_average_tons DECIMAL(10, 2) DEFAULT 4.5,
    target_2c_tons DECIMAL(10, 2) DEFAULT 2.0,
    
    -- Metadata
    calculation_version VARCHAR(10) DEFAULT '1.0',
    data_completeness INTEGER DEFAULT 100,  -- Percentage
    confidence_score DECIMAL(5, 2) DEFAULT 100.00,
    
    carbon_input_id UUID REFERENCES carbon_inputs(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_carbon_footprints_user_id ON carbon_footprints(user_id);
CREATE INDEX idx_carbon_footprints_created_at ON carbon_footprints(created_at);
CREATE INDEX idx_carbon_footprints_grade ON carbon_footprints(grade);
CREATE INDEX idx_carbon_footprints_user_date ON carbon_footprints(user_id, created_at DESC);

-- Partition by month for scalability
CREATE TABLE carbon_footprints_y2026m06 PARTITION OF carbon_footprints
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

**Sample Data:**
```sql
INSERT INTO carbon_footprints (
    user_id, monthly_kg, annual_tons, grade, grade_score,
    transportation_kg, energy_kg, food_kg, shopping_kg, waste_kg
)
VALUES (
    'user_uuid_here',
    387.00,
    4.64,
    'GOOD',
    72,
    1950.00,
    1300.00,
    840.00,
    370.00,
    180.00
);
```

---

### Table: carbon_inputs

**Purpose:** Raw input data from carbon calculator

```sql
CREATE TABLE carbon_inputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Transportation
    vehicle_type VARCHAR(50),  -- 'car_petrol', 'car_diesel', 'ev', 'motorcycle', 'none'
    vehicle_km_per_month INTEGER,
    public_transport_frequency VARCHAR(20),  -- 'daily', 'weekly', 'monthly', 'rarely', 'never'
    flights_short_haul INTEGER DEFAULT 0,
    flights_long_haul INTEGER DEFAULT 0,
    bicycle_walking_pct INTEGER DEFAULT 0,
    
    -- Energy
    electricity_kwh_per_month INTEGER,
    renewable_energy_pct INTEGER DEFAULT 0,
    ac_usage VARCHAR(20),  -- 'none', 'minimal', 'moderate', 'heavy'
    heating_type VARCHAR(20),  -- 'gas', 'electric', 'solar', 'none'
    household_size INTEGER DEFAULT 1,
    
    -- Food
    diet_type VARCHAR(20),  -- 'vegan', 'vegetarian', 'pescatarian', 'meat_occasional', 'meat_daily'
    dairy_consumption VARCHAR(20),  -- 'none', 'low', 'medium', 'high'
    food_waste VARCHAR(20),  -- 'minimal', 'average', 'above_average'
    local_produce VARCHAR(20),  -- 'always', 'often', 'sometimes', 'rarely'
    
    -- Shopping
    clothing_items_per_month INTEGER DEFAULT 0,
    electronics_per_year INTEGER DEFAULT 0,
    online_deliveries_per_month INTEGER DEFAULT 0,
    second_hand_preference VARCHAR(20),  -- 'always', 'often', 'sometimes', 'never'
    
    -- Waste
    recycling_frequency VARCHAR(20),  -- 'always', 'often', 'sometimes', 'rarely', 'never'
    composting BOOLEAN DEFAULT FALSE,
    plastic_usage VARCHAR(20),  -- 'minimal', 'average', 'above_average'
    water_bottle_type VARCHAR(20),  -- 'reusable', 'disposable'
    
    -- Metadata
    completion_time_seconds INTEGER,
    data_source VARCHAR(50) DEFAULT 'manual_entry',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_carbon_inputs_user_id ON carbon_inputs(user_id);
CREATE INDEX idx_carbon_inputs_created_at ON carbon_inputs(created_at);
```

---

### Table: recommendations

**Purpose:** AI-generated personalized recommendations

```sql
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    carbon_footprint_id UUID REFERENCES carbon_footprints(id),
    
    -- Recommendation Details
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,  -- 'transportation', 'energy', 'food', 'shopping', 'waste'
    
    -- Impact Metrics
    co2_savings_kg_annual DECIMAL(10, 2) NOT NULL,
    co2_savings_percentage DECIMAL(5, 2),
    
    -- Feasibility
    difficulty VARCHAR(20) NOT NULL,  -- 'easy', 'medium', 'hard'
    cost_impact VARCHAR(20) NOT NULL,  -- 'saves_money', 'neutral', 'costs_money'
    estimated_cost_annual DECIMAL(10, 2),  -- Can be negative (savings)
    time_to_implement VARCHAR(20),  -- 'immediate', 'days', 'weeks', 'months'
    
    -- Implementation
    implementation_steps JSONB,  -- Array of steps
    tracking_metrics JSONB,  -- How to measure success
    
    -- Prioritization
    priority_score INTEGER NOT NULL CHECK (priority_score BETWEEN 0 AND 100),
    relevance_score DECIMAL(5, 2) DEFAULT 100.00,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'accepted', 'rejected', 'completed'
    accepted_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    -- AI Metadata
    ai_model VARCHAR(50) DEFAULT 'claude-opus-4.5',
    ai_confidence DECIMAL(5, 2) DEFAULT 95.00,
    generation_context JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX idx_recommendations_status ON recommendations(status);
CREATE INDEX idx_recommendations_category ON recommendations(category);
CREATE INDEX idx_recommendations_priority ON recommendations(priority_score DESC);
CREATE INDEX idx_recommendations_user_status ON recommendations(user_id, status);
```

**JSONB Examples:**
```json
// implementation_steps
[
  "Download your city's public transit app",
  "Plan routes for your two chosen days (suggest Tuesday & Thursday)",
  "Purchase monthly transit pass ($100)",
  "Set calendar reminders the night before",
  "Track your trips in FootprintIQ app"
]

// tracking_metrics
{
  "days_per_week": 2,
  "km_replaced": 60,
  "money_saved_monthly": 150,
  "co2_avoided_monthly": 28.5
}
```

---

### Table: conversations

**Purpose:** AI chat conversation sessions

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    title VARCHAR(255),  -- Auto-generated from first message
    conversation_type VARCHAR(50) DEFAULT 'general',  -- 'general', 'calculator_help', 'eco_twin'
    
    -- Metadata
    message_count INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    ai_model VARCHAR(50) DEFAULT 'claude-opus-4.5',
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'archived', 'deleted'
    last_message_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);
```

---

### Table: messages

**Purpose:** Individual messages within conversations

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    
    role VARCHAR(20) NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    
    -- AI Metadata (for assistant messages)
    token_count INTEGER,
    model VARCHAR(50),
    latency_ms INTEGER,
    cost_usd DECIMAL(10, 6),
    
    -- Context Used
    context_used JSONB,  -- RAG documents, user data used
    tools_called JSONB,  -- Tools/functions called
    
    -- Feedback
    user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 5),
    user_feedback TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

---

### Table: badges

**Purpose:** Achievement badge definitions

```sql
CREATE TABLE badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,  -- 'carbon_reduction', 'engagement', 'learning', 'social'
    
    -- Visual
    icon_url TEXT NOT NULL,
    color VARCHAR(7),  -- Hex color
    
    -- Requirements
    requirements JSONB NOT NULL,
    points_awarded INTEGER DEFAULT 0,
    rarity VARCHAR(20) DEFAULT 'common',  -- 'common', 'rare', 'epic', 'legendary'
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_hidden BOOLEAN DEFAULT FALSE,  -- Hidden until unlocked
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_badges_category ON badges(category);
CREATE INDEX idx_badges_active ON badges(is_active);
```

**Sample Data:**
```sql
INSERT INTO badges (name, display_name, description, category, icon_url, requirements, points_awarded, rarity)
VALUES 
    ('first_calculation', 'Carbon Curious', 'Complete your first carbon footprint calculation', 'engagement', 
     '/badges/curious.svg', '{"action": "complete_calculation", "count": 1}', 50, 'common'),
    ('week_streak', '7-Day Streak', 'Log in for 7 consecutive days', 'engagement',
     '/badges/streak7.svg', '{"action": "login_streak", "days": 7}', 100, 'common'),
    ('co2_reducer', 'Carbon Cutter', 'Reduce your footprint by 10%', 'carbon_reduction',
     '/badges/reducer.svg', '{"action": "reduction", "percentage": 10}', 250, 'rare');
```

---

### Table: user_badges

**Purpose:** Badges earned by users

```sql
CREATE TABLE user_badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id UUID NOT NULL REFERENCES badges(id),
    
    progress INTEGER DEFAULT 0,  -- For multi-step badges
    unlocked BOOLEAN DEFAULT FALSE,
    
    unlocked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, badge_id)
);

CREATE INDEX idx_user_badges_user_id ON user_badges(user_id);
CREATE INDEX idx_user_badges_unlocked ON user_badges(unlocked);
CREATE INDEX idx_user_badges_user_unlocked ON user_badges(user_id, unlocked_at DESC);
```

---

### Table: challenges

**Purpose:** Sustainability challenges

```sql
CREATE TABLE challenges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    
    -- Challenge Details
    challenge_type VARCHAR(50) NOT NULL,  -- 'daily', 'weekly', 'monthly', 'one_time'
    duration_days INTEGER,
    
    -- Requirements
    requirements JSONB NOT NULL,
    success_criteria JSONB NOT NULL,
    
    -- Rewards
    points_reward INTEGER DEFAULT 0,
    badge_id UUID REFERENCES badges(id),
    
    -- Timing
    start_date DATE,
    end_date DATE,
    is_recurring BOOLEAN DEFAULT FALSE,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    participant_count INTEGER DEFAULT 0,
    completion_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_challenges_active ON challenges(is_active);
CREATE INDEX idx_challenges_type ON challenges(challenge_type);
CREATE INDEX idx_challenges_dates ON challenges(start_date, end_date);
```

**Sample Data:**
```sql
INSERT INTO challenges (name, display_name, description, category, challenge_type, duration_days, requirements, success_criteria, points_reward)
VALUES (
    'green_commute_week',
    'Green Commute Challenge',
    'Use public transport or bike to work for 5 days',
    'transportation',
    'weekly',
    7,
    '{"transport_type": ["public", "bicycle"], "min_trips": 5}',
    '{"trips_completed": 5}',
    500
);
```

---

### Table: user_challenges

**Purpose:** User participation in challenges

```sql
CREATE TABLE user_challenges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_id UUID NOT NULL REFERENCES challenges(id),
    
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'completed', 'failed', 'abandoned'
    progress JSONB DEFAULT '{}',
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(user_id, challenge_id, started_at)
);

CREATE INDEX idx_user_challenges_user_id ON user_challenges(user_id);
CREATE INDEX idx_user_challenges_status ON user_challenges(status);
CREATE INDEX idx_user_challenges_challenge_id ON user_challenges(challenge_id);
```

---

### Table: user_points

**Purpose:** Track user gamification points

```sql
CREATE TABLE user_points (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    points INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    level_progress INTEGER DEFAULT 0,  -- Progress to next level (0-100)
    
    -- Point History
    total_points_earned INTEGER DEFAULT 0,
    total_points_spent INTEGER DEFAULT 0,
    
    -- Lifetime Stats
    badges_unlocked INTEGER DEFAULT 0,
    challenges_completed INTEGER DEFAULT 0,
    days_active INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    
    last_activity_date DATE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id)
);

CREATE INDEX idx_user_points_user_id ON user_points(user_id);
CREATE INDEX idx_user_points_points ON user_points(points DESC);
CREATE INDEX idx_user_points_level ON user_points(level DESC);
```

---

### Table: point_transactions

**Purpose:** Detailed point transaction history

```sql
CREATE TABLE point_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    points INTEGER NOT NULL,  -- Can be negative for spending
    transaction_type VARCHAR(50) NOT NULL,  -- 'calculation', 'badge_unlock', 'challenge', 'daily_login', 'referral'
    description VARCHAR(255),
    
    -- Reference
    reference_type VARCHAR(50),  -- 'badge', 'challenge', 'recommendation'
    reference_id UUID,
    
    balance_after INTEGER NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_point_transactions_user_id ON point_transactions(user_id);
CREATE INDEX idx_point_transactions_created_at ON point_transactions(created_at);
CREATE INDEX idx_point_transactions_user_date ON point_transactions(user_id, created_at DESC);
```

---

### Table: leaderboards

**Purpose:** Community leaderboard rankings

```sql
CREATE TABLE leaderboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Leaderboard Types
    leaderboard_type VARCHAR(50) NOT NULL,  -- 'global', 'country', 'friends', 'organization'
    period VARCHAR(20) NOT NULL,  -- 'daily', 'weekly', 'monthly', 'all_time'
    
    -- Metrics
    rank INTEGER NOT NULL,
    score DECIMAL(10, 2) NOT NULL,  -- Could be points, reduction %, etc.
    metric_type VARCHAR(50) NOT NULL,  -- 'points', 'reduction_pct', 'co2_saved'
    
    -- Grouping (for country/org leaderboards)
    group_id VARCHAR(100),
    
    -- Period Dates
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Metadata
    total_participants INTEGER,
    percentile DECIMAL(5, 2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, leaderboard_type, period, period_start)
);

CREATE INDEX idx_leaderboards_type_period ON leaderboards(leaderboard_type, period);
CREATE INDEX idx_leaderboards_rank ON leaderboards(leaderboard_type, period, rank);
CREATE INDEX idx_leaderboards_user_id ON leaderboards(user_id);
CREATE INDEX idx_leaderboards_period_dates ON leaderboards(period_start, period_end);
```

---

### Table: learning_content

**Purpose:** Educational content and articles

```sql
CREATE TABLE learning_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    content TEXT NOT NULL,  -- Markdown content
    
    -- Classification
    category VARCHAR(50) NOT NULL,  -- 'basics', 'transportation', 'energy', 'food', 'lifestyle'
    difficulty VARCHAR(20) DEFAULT 'beginner',  -- 'beginner', 'intermediate', 'advanced'
    content_type VARCHAR(50) NOT NULL,  -- 'article', 'video', 'infographic', 'quiz'
    
    -- Media
    thumbnail_url TEXT,
    video_url TEXT,
    estimated_read_time INTEGER,  -- Minutes
    
    -- Engagement
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    
    -- SEO
    meta_title VARCHAR(255),
    meta_description TEXT,
    tags TEXT[],
    
    -- Status
    is_published BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE,
    
    author_id UUID REFERENCES users(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_learning_content_slug ON learning_content(slug);
CREATE INDEX idx_learning_content_category ON learning_content(category);
CREATE INDEX idx_learning_content_published ON learning_content(is_published, published_at DESC);
CREATE INDEX idx_learning_content_tags ON learning_content USING GIN(tags);
```

---

### Table: content_views

**Purpose:** Track user engagement with learning content

```sql
CREATE TABLE content_views (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content_id UUID NOT NULL REFERENCES learning_content(id) ON DELETE CASCADE,
    
    -- Engagement Metrics
    view_duration_seconds INTEGER,
    completion_percentage INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    
    -- Feedback
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    liked BOOLEAN DEFAULT FALSE,
    
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_content_views_user_id ON content_views(user_id);
CREATE INDEX idx_content_views_content_id ON content_views(content_id);
CREATE INDEX idx_content_views_completed ON content_views(completed);
```

---

### Table: quizzes

**Purpose:** Interactive sustainability quizzes

```sql
CREATE TABLE quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'beginner',
    
    -- Questions (JSONB array)
    questions JSONB NOT NULL,
    
    -- Scoring
    total_points INTEGER DEFAULT 0,
    passing_score INTEGER,
    
    -- Rewards
    points_reward INTEGER DEFAULT 0,
    badge_id UUID REFERENCES badges(id),
    
    -- Stats
    attempt_count INTEGER DEFAULT 0,
    average_score DECIMAL(5, 2),
    
    is_published BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quizzes_category ON quizzes(category);
CREATE INDEX idx_quizzes_published ON quizzes(is_published);
```

**JSONB Example:**
```json
{
  "questions": [
    {
      "id": "q1",
      "question": "Which transportation mode has the lowest carbon footprint per km?",
      "type": "multiple_choice",
      "options": [
        "Electric car",
        "Train",
        "Bus",
        "Bicycle"
      ],
      "correct_answer": "Bicycle",
      "explanation": "Bicycles have zero direct emissions and minimal manufacturing impact.",
      "points": 10
    }
  ]
}
```

---

### Table: quiz_attempts

**Purpose:** User quiz attempts and results

```sql
CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_id UUID NOT NULL REFERENCES quizzes(id),
    
    -- Results
    score INTEGER NOT NULL,
    total_possible INTEGER NOT NULL,
    percentage DECIMAL(5, 2),
    passed BOOLEAN,
    
    -- Answers
    answers JSONB NOT NULL,
    time_taken_seconds INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX idx_quiz_attempts_quiz_id ON quiz_attempts(quiz_id);
CREATE INDEX idx_quiz_attempts_user_quiz ON quiz_attempts(user_id, quiz_id, created_at DESC);
```

---

### Table: eco_twin_states

**Purpose:** Eco Twin virtual sustainability models

```sql
CREATE TABLE eco_twin_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- State Snapshot
    state_name VARCHAR(100) NOT NULL,  -- 'current', 'optimized', 'custom_1'
    description TEXT,
    
    -- Carbon Profile (snapshot)
    carbon_footprint_snapshot JSONB NOT NULL,
    
    -- Behavioral Model
    transportation_model JSONB,
    energy_model JSONB,
    food_model JSONB,
    shopping_model JSONB,
    waste_model JSONB,
    
    -- Predictions
    projected_annual_tons DECIMAL(10, 2),
    projected_30d_kg DECIMAL(10, 2),
    projected_90d_kg DECIMAL(10, 2),
    projected_365d_kg DECIMAL(10, 2),
    
    is_baseline BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_eco_twin_states_user_id ON eco_twin_states(user_id);
CREATE INDEX idx_eco_twin_states_baseline ON eco_twin_states(user_id, is_baseline);
```

---

### Table: eco_twin_simulations

**Purpose:** What-if scenario simulations

```sql
CREATE TABLE eco_twin_simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    baseline_state_id UUID NOT NULL REFERENCES eco_twin_states(id),
    
    simulation_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Changes Applied
    changes_applied JSONB NOT NULL,
    
    -- Results
    new_annual_tons DECIMAL(10, 2) NOT NULL,
    reduction_tons DECIMAL(10, 2) NOT NULL,
    reduction_percentage DECIMAL(5, 2) NOT NULL,
    
    -- Financial Impact
    estimated_cost_annual DECIMAL(10, 2),
    savings_annual DECIMAL(10, 2),
    payback_period_months INTEGER,
    
    -- Feasibility Analysis
    difficulty_score INTEGER CHECK (difficulty_score BETWEEN 0 AND 100),
    ai_recommendation_score INTEGER CHECK (ai_recommendation_score BETWEEN 0 AND 100),
    
    -- Metadata
    ai_model VARCHAR(50) DEFAULT 'claude-opus-4.5',
    simulation_time_ms INTEGER,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_eco_twin_simulations_user_id ON eco_twin_simulations(user_id);
CREATE INDEX idx_eco_twin_simulations_baseline ON eco_twin_simulations(baseline_state_id);
```

---

### Table: recommendation_actions

**Purpose:** Track user actions on recommendations

```sql
CREATE TABLE recommendation_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recommendation_id UUID NOT NULL REFERENCES recommendations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    action_type VARCHAR(50) NOT NULL,  -- 'accepted', 'rejected', 'started', 'completed', 'paused'
    notes TEXT,
    
    -- Progress Tracking
    progress_percentage INTEGER DEFAULT 0,
    milestones_completed JSONB,
    
    -- Impact Tracking
    actual_co2_saved_kg DECIMAL(10, 2),
    actual_cost_impact DECIMAL(10, 2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recommendation_actions_recommendation_id ON recommendation_actions(recommendation_id);
CREATE INDEX idx_recommendation_actions_user_id ON recommendation_actions(user_id);
CREATE INDEX idx_recommendation_actions_action_type ON recommendation_actions(action_type);
```

---

### Table: user_analytics

**Purpose:** Aggregated user analytics and insights

```sql
CREATE TABLE user_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Time Period
    period_type VARCHAR(20) NOT NULL,  -- 'daily', 'weekly', 'monthly'
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Engagement Metrics
    login_count INTEGER DEFAULT 0,
    session_duration_minutes INTEGER DEFAULT 0,
    pages_viewed INTEGER DEFAULT 0,
    
    -- Carbon Metrics
    calculations_performed INTEGER DEFAULT 0,
    average_carbon_footprint DECIMAL(10, 2),
    carbon_reduction_pct DECIMAL(5, 2),
    
    -- AI Interactions
    ai_conversations INTEGER DEFAULT 0,
    ai_messages_sent INTEGER DEFAULT 0,
    
    -- Gamification
    points_earned INTEGER DEFAULT 0,
    badges_unlocked INTEGER DEFAULT 0,
    challenges_completed INTEGER DEFAULT 0,
    
    -- Content
    articles_read INTEGER DEFAULT 0,
    quizzes_taken INTEGER DEFAULT 0,
    
    -- Recommendations
    recommendations_received INTEGER DEFAULT 0,
    recommendations_accepted INTEGER DEFAULT 0,
    recommendations_completed INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, period_type, period_start)
);

CREATE INDEX idx_user_analytics_user_id ON user_analytics(user_id);
CREATE INDEX idx_user_analytics_period ON user_analytics(period_type, period_start);
```

---

### Table: audit_logs

**Purpose:** System audit trail for security and compliance

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Actor
    user_id UUID REFERENCES users(id),
    actor_type VARCHAR(50) NOT NULL,  -- 'user', 'admin', 'system'
    
    -- Action
    action VARCHAR(100) NOT NULL,  -- 'user.login', 'carbon.calculate', 'recommendation.accept'
    resource_type VARCHAR(50) NOT NULL,  -- 'user', 'carbon_footprint', 'recommendation'
    resource_id UUID,
    
    -- Details
    description TEXT,
    changes JSONB,  -- Before/after for updates
    
    -- Context
    ip_address INET,
    user_agent TEXT,
    request_id UUID,
    
    -- Status
    status VARCHAR(20) NOT NULL,  -- 'success', 'failure', 'error'
    error_message TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
```

---

### Table: roles

**Purpose:** User role definitions for RBAC

```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(50) UNIQUE NOT NULL,  -- 'user', 'premium', 'admin', 'corporate_manager'
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Permissions
    permissions JSONB NOT NULL,
    
    is_system_role BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_roles_name ON roles(name);

-- Seed data
INSERT INTO roles (name, display_name, description, permissions, is_system_role)
VALUES 
    ('user', 'Regular User', 'Standard user with full app access', 
     '{"carbon": ["read", "write"], "ai": ["chat"], "gamification": ["participate"]}', TRUE),
    ('premium', 'Premium User', 'Enhanced features and analytics',
     '{"carbon": ["read", "write", "export"], "ai": ["chat", "priority"], "analytics": ["advanced"]}', TRUE),
    ('admin', 'Administrator', 'Full system access',
     '{"*": ["*"]}', TRUE);
```

---

### Table: organizations

**Purpose:** Corporate/organizational accounts

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    
    -- Contact
    email VARCHAR(255),
    website VARCHAR(255),
    
    -- Settings
    settings JSONB DEFAULT '{}',
    
    -- Stats
    member_count INTEGER DEFAULT 0,
    total_carbon_saved DECIMAL(10, 2) DEFAULT 0,
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organizations_active ON organizations(is_active);
```

---

### Table: organization_members

**Purpose:** Organization membership

```sql
CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    role VARCHAR(50) DEFAULT 'member',  -- 'owner', 'admin', 'manager', 'member'
    
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(organization_id, user_id)
);

CREATE INDEX idx_organization_members_org_id ON organization_members(organization_id);
CREATE INDEX idx_organization_members_user_id ON organization_members(user_id);
```

---

## Indexes

### Performance-Critical Indexes

```sql
-- User lookups
CREATE INDEX idx_users_email_active ON users(email) WHERE deleted_at IS NULL AND is_active = TRUE;

-- Carbon footprint queries
CREATE INDEX idx_carbon_footprints_user_recent ON carbon_footprints(user_id, created_at DESC) 
    WHERE deleted_at IS NULL;

-- Leaderboard rankings
CREATE INDEX idx_leaderboards_global_weekly ON leaderboards(rank) 
    WHERE leaderboard_type = 'global' AND period = 'weekly';

-- AI conversation history
CREATE INDEX idx_messages_conversation_recent ON messages(conversation_id, created_at DESC);

-- Recommendation filtering
CREATE INDEX idx_recommendations_user_active ON recommendations(user_id, priority_score DESC) 
    WHERE status = 'active';
```

### Full-Text Search Indexes

```sql
-- Content search
CREATE INDEX idx_learning_content_fts ON learning_content 
    USING GIN(to_tsvector('english', title || ' ' || description || ' ' || content));

-- User search
CREATE INDEX idx_users_fts ON users 
    USING GIN(to_tsvector('english', username || ' ' || email));
```

---

## Relationships

### Primary Relationships

1. **users → carbon_footprints** (1:N)
   - One user has many carbon footprint calculations

2. **users → conversations** (1:N)
   - One user has many AI conversations

3. **conversations → messages** (1:N)
   - One conversation has many messages

4. **users → recommendations** (1:N)
   - One user receives many recommendations

5. **users → user_badges** (1:N)
   - One user can earn many badges

6. **badges → user_badges** (1:N)
   - One badge can be earned by many users

7. **users → user_challenges** (1:N)
   - One user can participate in many challenges

8. **challenges → user_challenges** (1:N)
   - One challenge can have many participants

9. **users → eco_twin_states** (1:N)
   - One user can have multiple eco twin states

10. **eco_twin_states → eco_twin_simulations** (1:N)
    - One state can have many simulations

---

## Sample Queries

### Query 1: Get User Dashboard Data

```sql
SELECT 
    u.id,
    u.username,
    u.email,
    up.full_name,
    up.avatar_url,
    -- Latest carbon footprint
    (SELECT json_build_object(
        'monthly_kg', cf.monthly_kg,
        'annual_tons', cf.annual_tons,
        'grade', cf.grade,
        'created_at', cf.created_at
    )
    FROM carbon_footprints cf
    WHERE cf.user_id = u.id
    ORDER BY cf.created_at DESC
    LIMIT 1) as latest_footprint,
    -- Points and level
    (SELECT json_build_object(
        'points', upnt.points,
        'level', upnt.level,
        'badges_unlocked', upnt.badges_unlocked,
        'current_streak', upnt.current_streak
    )
    FROM user_points upnt
    WHERE upnt.user_id = u.id) as gamification,
    -- Active challenges count
    (SELECT COUNT(*)
    FROM user_challenges uc
    WHERE uc.user_id = u.id AND uc.status = 'active') as active_challenges
FROM users u
LEFT JOIN user_profiles up ON u.id = up.user_id
WHERE u.id = $1;
```

### Query 2: Get Carbon Trend (Last 12 Months)

```sql
SELECT 
    DATE_TRUNC('month', created_at) as month,
    AVG(monthly_kg) as avg_monthly_kg,
    AVG(annual_tons) as avg_annual_tons,
    COUNT(*) as calculation_count
FROM carbon_footprints
WHERE user_id = $1
    AND created_at >= NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;
```

### Query 3: Get Leaderboard

```sql
SELECT 
    l.rank,
    u.username,
    up.avatar_url,
    l.score,
    l.metric_type,
    up.country_code
FROM leaderboards l
JOIN users u ON l.user_id = u.id
LEFT JOIN user_profiles up ON u.id = up.user_id
WHERE l.leaderboard_type = 'global'
    AND l.period = 'weekly'
    AND l.period_start = DATE_TRUNC('week', CURRENT_DATE)
ORDER BY l.rank
LIMIT 100;
```

### Query 4: Get Active Recommendations with Impact

```sql
SELECT 
    r.id,
    r.title,
    r.description,
    r.category,
    r.co2_savings_kg_annual,
    r.difficulty,
    r.cost_impact,
    r.priority_score,
    r.implementation_steps,
    COALESCE(ra.action_type, 'pending') as user_status
FROM recommendations r
LEFT JOIN recommendation_actions ra 
    ON r.id = ra.recommendation_id 
    AND ra.user_id = $1
WHERE r.user_id = $1
    AND r.status = 'active'
ORDER BY r.priority_score DESC
LIMIT 10;
```

### Query 5: Calculate User Impact Summary

```sql
SELECT 
    u.id,
    u.username,
    -- Total CO2 saved
    COALESCE(SUM(
        CASE 
            WHEN cf_first.annual_tons > cf_latest.annual_tons 
            THEN cf_first.annual_tons - cf_latest.annual_tons
            ELSE 0
        END
    ), 0) as total_co2_saved_tons,
    -- Reduction percentage
    CASE 
        WHEN cf_first.annual_tons > 0 THEN
            ((cf_first.annual_tons - cf_latest.annual_tons) / cf_first.annual_tons * 100)
        ELSE 0
    END as reduction_percentage,
    -- Days since joining
    DATE_PART('day', NOW() - u.created_at) as days_since_joining,
    -- Total points
    up.points as total_points,
    -- Recommendations completed
    (SELECT COUNT(*)
     FROM recommendation_actions ra
     WHERE ra.user_id = u.id AND ra.action_type = 'completed') as recommendations_completed
FROM users u
LEFT JOIN user_points up ON u.id = up.user_id
LEFT JOIN LATERAL (
    SELECT annual_tons
    FROM carbon_footprints
    WHERE user_id = u.id
    ORDER BY created_at ASC
    LIMIT 1
) cf_first ON true
LEFT JOIN LATERAL (
    SELECT annual_tons
    FROM carbon_footprints
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 1
) cf_latest ON true
WHERE u.id = $1
GROUP BY u.id, u.username, cf_first.annual_tons, cf_latest.annual_tons, u.created_at, up.points;
```

---

## Migration Strategy

### Initial Migration (v1.0)

```sql
-- migrations/001_initial_schema.sql

BEGIN;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- Create custom types
CREATE TYPE carbon_grade AS ENUM ('EXCELLENT', 'GOOD', 'MODERATE', 'HIGH', 'CRITICAL');
CREATE TYPE recommendation_status AS ENUM ('active', 'accepted', 'rejected', 'completed');

-- Create all tables (as defined above)
-- ... table creation statements ...

-- Create indexes
-- ... index creation statements ...

-- Insert seed data
INSERT INTO roles (name, display_name, permissions, is_system_role) VALUES (...);

COMMIT;
```

### Migration Best Practices

1. **Version Control:** All migrations in Git
2. **Rollback Scripts:** Every migration has a down script
3. **Data Preservation:** Never destructive migrations in production
4. **Testing:** Test migrations on staging first
5. **Backup:** Always backup before major migrations

### Example Migration Tools

```bash
# Using Alembic (Python)
alembic init migrations
alembic revision -m "initial schema"
alembic upgrade head

# Using Flyway (Java)
flyway migrate

# Using golang-migrate
migrate -path ./migrations -database postgres://... up
```

---

## Database Optimization

### Partitioning Strategy

```sql
-- Partition carbon_footprints by month
CREATE TABLE carbon_footprints (
    ...
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE carbon_footprints_y2026m06 PARTITION OF carbon_footprints
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');

-- Automatic partition creation
CREATE OR REPLACE FUNCTION create_partition_if_not_exists()
RETURNS TRIGGER AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    start_date := DATE_TRUNC('month', NEW.created_at);
    end_date := start_date + INTERVAL '1 month';
    partition_name := 'carbon_footprints_y' || TO_CHAR(start_date, 'YYYY') || 
                      'm' || TO_CHAR(start_date, 'MM');
    
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = partition_name) THEN
        EXECUTE format('CREATE TABLE %I PARTITION OF carbon_footprints 
                        FOR VALUES FROM (%L) TO (%L)',
                       partition_name, start_date, end_date);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Query Optimization

1. **Use EXPLAIN ANALYZE** for slow queries
2. **Index covering queries** where possible
3. **Materialized views** for complex analytics
4. **Connection pooling** (PgBouncer)
5. **Read replicas** for analytics queries

---

## Backup & Recovery

### Backup Strategy

```bash
# Daily full backup
pg_dump -U postgres -d footprintiq -F c -f backup_$(date +%Y%m%d).dump

# Point-in-time recovery setup
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://footprintiq-backups/wal/%f'
```

### Recovery

```bash
# Restore from backup
pg_restore -U postgres -d footprintiq backup_20260617.dump

# Point-in-time recovery
# ... PITR commands ...
```

---

## Monitoring Queries

### Active Connections

```sql
SELECT count(*) as active_connections
FROM pg_stat_activity
WHERE state = 'active';
```

### Slow Queries

```sql
SELECT 
    query,
    mean_exec_time,
    calls,
    total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Table Sizes

```sql
SELECT 
    table_name,
    pg_size_pretty(pg_total_relation_size(table_name::regclass)) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(table_name::regclass) DESC;
```

---

## Security Considerations

1. **Row-Level Security (RLS):**
```sql
ALTER TABLE carbon_footprints ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_carbon_policy ON carbon_footprints
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::UUID);
```

2. **Encryption:** All connections use TLS
3. **Credentials:** Stored in AWS Secrets Manager
4. **Least Privilege:** Application uses read/write-only user
5. **Audit Logging:** All DDL operations logged

---

**Document Owner:** Database Architect  
**Last Updated:** June 17, 2026  
**Next Review:** July 17, 2026  
**Status:** APPROVED FOR IMPLEMENTATION
