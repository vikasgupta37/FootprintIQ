# System Architecture Document
# FootprintIQ - AI-Powered Carbon Footprint Awareness Platform

**Version:** 1.0.0  
**Date:** June 17, 2026  
**Status:** Implementation Ready  
**Classification:** Technical Architecture Specification

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Architecture](#component-architecture)
4. [Data Flow Architecture](#data-flow-architecture)
5. [AI Agent Architecture](#ai-agent-architecture)
6. [Frontend Architecture](#frontend-architecture)
7. [Backend Architecture](#backend-architecture)
8. [Database Architecture](#database-architecture)
9. [Infrastructure Architecture](#infrastructure-architecture)
10. [Security Architecture](#security-architecture)
11. [Scalability & Performance](#scalability--performance)
12. [Monitoring & Observability](#monitoring--observability)

---

## Architecture Overview

### Design Principles

1. **AI-First Design**
   - AI agent as core intelligence layer
   - RAG architecture for knowledge retrieval
   - Agentic workflow for complex reasoning
   - Multi-agent orchestration capability

2. **Scalability by Design**
   - Microservices-inspired modular architecture
   - Horizontal scaling capability
   - Stateless service design
   - Event-driven communication

3. **Performance Optimized**
   - CDN for static assets
   - Redis caching layer
   - Database query optimization
   - Lazy loading and code splitting
   - Background job processing

4. **Security First**
   - Zero-trust architecture
   - Defense in depth
   - Encryption everywhere
   - Least privilege access

5. **Developer Experience**
   - Clear separation of concerns
   - Well-defined interfaces
   - Comprehensive documentation
   - Easy local development setup

### Technology Stack Summary

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│  Next.js 15 + TypeScript + Tailwind + ShadCN UI        │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTPS
┌─────────────────────────────────────────────────────────┐
│                    CDN LAYER                             │
│         AWS CloudFront + S3 (Static Assets)             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 LOAD BALANCER                            │
│              AWS Application Load Balancer              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                APPLICATION LAYER                         │
│              FastAPI (Python 3.11+)                     │
│    ┌──────────────┐  ┌──────────────┐                  │
│    │  API Gateway │  │  WebSocket   │                  │
│    │   Service    │  │   Service    │                  │
│    └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   AI AGENT LAYER                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │  Carbon    │  │   Advisor  │  │  Eco Twin  │        │
│  │  Engine    │  │   Agent    │  │  Simulator │        │
│  └────────────┘  └────────────┘  └────────────┘        │
│         Claude Opus 4.5 + LangGraph                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  SERVICE LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │   User     │  │  Carbon    │  │   Gamif.   │        │
│  │  Service   │  │  Service   │  │  Service   │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │ PostgreSQL │  │   Redis    │  │  Pinecone  │        │
│  │    (DB)    │  │  (Cache)   │  │  (Vector)  │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 STORAGE LAYER                            │
│              AWS S3 (Object Storage)                    │
└─────────────────────────────────────────────────────────┘
```

---

## High-Level Architecture

### System Context Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    EXTERNAL ACTORS                            │
│                                                               │
│  [End Users]  [Admins]  [Corporate Managers]                 │
│       ↓          ↓              ↓                             │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│                 FOOTPRINTIQ PLATFORM                          │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            Web Application (Next.js)                 │    │
│  │  • Dashboard  • Calculator  • Chat  • Analytics     │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           API Layer (FastAPI)                        │    │
│  │  • REST APIs  • WebSocket  • Authentication         │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         AI Agent Layer (Claude + LangGraph)          │    │
│  │  • Carbon Engine  • Advisor  • Eco Twin             │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Data & Storage Layer                    │    │
│  │  • PostgreSQL  • Redis  • Pinecone  • S3           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                            │
│                                                               │
│  [Anthropic API]  [Google OAuth]  [AWS Services]             │
│  [Email Service]  [Analytics]  [Monitoring]                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Architectural Layers

#### 1. Presentation Layer (Frontend)
**Technology:** Next.js 15 (App Router), TypeScript, Tailwind CSS

**Responsibilities:**
- User interface rendering
- Client-side state management
- Form validation
- Real-time updates
- Responsive design
- Progressive Web App (PWA) features

**Key Components:**
- Dashboard pages
- Carbon calculator forms
- AI chat interface
- Analytics visualizations
- Gamification UI
- User profile management

#### 2. API Gateway Layer
**Technology:** FastAPI, Pydantic, OAuth 2.0

**Responsibilities:**
- Request routing
- Authentication & authorization
- Rate limiting
- Request validation
- Response transformation
- API versioning
- WebSocket management

**Endpoints:**
- `/api/v1/auth/*` - Authentication
- `/api/v1/carbon/*` - Carbon calculations
- `/api/v1/ai/*` - AI agent interactions
- `/api/v1/users/*` - User management
- `/api/v1/analytics/*` - Analytics data
- `/api/v1/gamification/*` - Points, badges, challenges
- `/api/v1/community/*` - Leaderboards, social

#### 3. AI Agent Layer
**Technology:** Claude Opus 4.5, LangGraph, LangChain

**Responsibilities:**
- Carbon footprint calculation
- Behavioral analysis
- Recommendation generation
- Predictive modeling
- Eco Twin simulation
- Natural language understanding
- Context management
- Multi-step reasoning

**Components:**
- **Carbon Assessment Engine**
- **Behavior Analysis Engine**
- **Recommendation Engine**
- **Prediction Engine**
- **Eco Twin Simulator**
- **Response Generator**

#### 4. Business Logic Layer (Services)
**Technology:** Python, Pydantic, SQLAlchemy

**Services:**
- **UserService:** User management, profiles, preferences
- **CarbonService:** Footprint calculations, historical data
- **RecommendationService:** Suggestion generation, prioritization
- **GamificationService:** Points, badges, challenges, leaderboards
- **AnalyticsService:** Data aggregation, trend analysis
- **NotificationService:** Email, push, in-app notifications
- **AdminService:** Platform administration, content management

#### 5. Data Access Layer
**Technology:** SQLAlchemy ORM, Redis Client, Pinecone Client

**Responsibilities:**
- Database operations (CRUD)
- Query optimization
- Transaction management
- Cache management
- Vector operations
- Data validation

**Data Stores:**
- **PostgreSQL:** Primary relational data
- **Redis:** Session cache, rate limiting, job queue
- **Pinecone:** Vector embeddings, semantic search
- **S3:** File storage, backups, exports

#### 6. Infrastructure Layer
**Technology:** AWS, Docker, Terraform

**Components:**
- Load balancers
- Container orchestration
- CDN
- Monitoring
- Logging
- Alerting

---

## Component Architecture

### Frontend Component Hierarchy

```
App (Root)
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── MainNav
│   │   └── QuickActions
│   └── Footer
│
├── Pages
│   ├── Dashboard
│   │   ├── CarbonScoreCard
│   │   ├── BreakdownChart
│   │   ├── RecommendationsList
│   │   ├── ChallengesWidget
│   │   └── ProgressTracker
│   │
│   ├── Calculator
│   │   ├── MultiStepForm
│   │   │   ├── TransportationStep
│   │   │   ├── EnergyStep
│   │   │   ├── FoodStep
│   │   │   ├── ShoppingStep
│   │   │   └── WasteStep
│   │   └── ResultsDisplay
│   │
│   ├── AIAdvisor
│   │   ├── ChatInterface
│   │   │   ├── MessageList
│   │   │   ├── MessageInput
│   │   │   └── SuggestionChips
│   │   └── ContextPanel
│   │
│   ├── EcoTwin
│   │   ├── CurrentStateView
│   │   ├── ScenarioBuilder
│   │   ├── SimulationResults
│   │   └── ComparisonChart
│   │
│   ├── Analytics
│   │   ├── TimeSeriesChart
│   │   ├── CategoryBreakdown
│   │   ├── TrendAnalysis
│   │   └── ExportOptions
│   │
│   ├── Gamification
│   │   ├── PointsDisplay
│   │   ├── BadgeCollection
│   │   ├── ChallengesList
│   │   ├── Leaderboard
│   │   └── AchievementModal
│   │
│   ├── Learning
│   │   ├── ArticleList
│   │   ├── ArticleReader
│   │   ├── Quiz
│   │   └── LearningPath
│   │
│   └── Profile
│       ├── PersonalInfo
│       ├── Preferences
│       ├── DataExport
│       └── Settings
│
└── Shared Components
    ├── UI Components (ShadCN)
    │   ├── Button, Input, Card
    │   ├── Dialog, Sheet, Toast
    │   └── Charts, Tables, Forms
    │
    ├── Custom Components
    │   ├── LoadingSpinner
    │   ├── ErrorBoundary
    │   ├── EmptyState
    │   └── FeatureFlag
    │
    └── Hooks
        ├── useAuth
        ├── useCarbon
        ├── useAI
        └── useGamification
```

### Backend Service Architecture

```
FastAPI Application
├── app/
│   ├── main.py (Application entry point)
│   │
│   ├── api/ (API Routes)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── carbon.py
│   │   │   ├── ai.py
│   │   │   ├── users.py
│   │   │   ├── analytics.py
│   │   │   ├── gamification.py
│   │   │   ├── community.py
│   │   │   └── admin.py
│   │   └── deps.py (Dependencies)
│   │
│   ├── core/ (Core Configuration)
│   │   ├── config.py (Settings)
│   │   ├── security.py (Auth, JWT)
│   │   ├── database.py (DB connection)
│   │   ├── cache.py (Redis)
│   │   └── logging.py
│   │
│   ├── models/ (Database Models)
│   │   ├── user.py
│   │   ├── carbon_footprint.py
│   │   ├── recommendation.py
│   │   ├── gamification.py
│   │   ├── conversation.py
│   │   └── analytics.py
│   │
│   ├── schemas/ (Pydantic Schemas)
│   │   ├── user.py
│   │   ├── carbon.py
│   │   ├── ai.py
│   │   ├── recommendation.py
│   │   └── gamification.py
│   │
│   ├── services/ (Business Logic)
│   │   ├── user_service.py
│   │   ├── carbon_service.py
│   │   ├── recommendation_service.py
│   │   ├── gamification_service.py
│   │   ├── analytics_service.py
│   │   └── notification_service.py
│   │
│   ├── agents/ (AI Agents)
│   │   ├── base_agent.py
│   │   ├── carbon_engine.py
│   │   ├── advisor_agent.py
│   │   ├── recommendation_engine.py
│   │   ├── prediction_engine.py
│   │   ├── eco_twin_simulator.py
│   │   └── tools/
│   │       ├── calculator_tool.py
│   │       ├── knowledge_base_tool.py
│   │       └── analysis_tool.py
│   │
│   ├── utils/ (Utilities)
│   │   ├── carbon_calculations.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   └── helpers.py
│   │
│   └── workers/ (Background Jobs)
│       ├── celery_app.py
│       ├── email_tasks.py
│       ├── analytics_tasks.py
│       └── cleanup_tasks.py
```

---

## Data Flow Architecture

### Request Flow: Carbon Calculation

```
1. User Input
   ↓
2. Frontend Form Validation
   ↓
3. API Request: POST /api/v1/carbon/calculate
   ↓
4. API Gateway (FastAPI)
   - Authentication check
   - Rate limit check
   - Request validation
   ↓
5. CarbonService
   - Parse input data
   - Call Carbon Engine (AI Agent)
   ↓
6. Carbon Assessment Engine (AI)
   - Apply calculation formulas
   - Category analysis
   - Grade assignment
   ↓
7. Database Operations
   - Save carbon footprint record
   - Update user statistics
   - Cache results (Redis)
   ↓
8. Response Generation
   - Format results
   - Add comparisons
   - Include recommendations
   ↓
9. API Response
   ↓
10. Frontend Update
    - Update dashboard
    - Show results
    - Trigger animations
```

### Request Flow: AI Conversation

```
1. User Message
   ↓
2. WebSocket Connection / HTTP POST
   ↓
3. API Gateway
   - Authenticate
   - Validate message
   ↓
4. AI Service
   - Load conversation history (Redis)
   - Load user context (PostgreSQL)
   - Retrieve relevant knowledge (Pinecone)
   ↓
5. Advisor Agent (Claude Opus 4.5)
   - Understand intent
   - Analyze user data
   - Generate response
   - Create recommendations
   ↓
6. Response Processing
   - Format markdown
   - Extract action items
   - Generate follow-ups
   ↓
7. Storage
   - Save conversation (PostgreSQL)
   - Update cache (Redis)
   - Log analytics
   ↓
8. Stream Response
   - Real-time streaming to client
   - Character-by-character display
   ↓
9. Frontend Display
   - Render message
   - Show suggestions
   - Update context
```

### Data Synchronization Flow

```
User Action (Frontend)
   ↓
API Request
   ↓
┌─────────────────────────────────┐
│  Write-Through Cache Pattern     │
│                                  │
│  1. Write to PostgreSQL          │
│  2. Update Redis cache           │
│  3. Invalidate related caches    │
│  4. Return success               │
└─────────────────────────────────┘
   ↓
Response to Frontend
   ↓
Real-time Update (WebSocket)
   - Notify connected clients
   - Update leaderboards
   - Refresh analytics
```

---

## AI Agent Architecture

### Agentic Workflow

```
┌──────────────────────────────────────────────────────────┐
│              USER INPUT / TRIGGER                         │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│           INTENT CLASSIFICATION AGENT                     │
│  • Determine request type                                 │
│  • Route to appropriate agent                             │
│  • Extract key parameters                                 │
└──────────────────────────────────────────────────────────┘
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
┌─────────────────────┐   ┌─────────────────────┐
│  CARBON ASSESSMENT  │   │   ADVISOR AGENT     │
│       ENGINE        │   │                     │
│                     │   │  • Answer questions │
│  • Calculate CO2e   │   │  • Explain concepts │
│  • Analyze patterns │   │  • Educate users    │
│  • Grade footprint  │   │  • Guide actions    │
└─────────────────────┘   └─────────────────────┘
              ↓                       ↓
┌─────────────────────────────────────────────────────────┐
│         BEHAVIOR ANALYSIS ENGINE                         │
│  • Identify high-impact areas                            │
│  • Detect patterns                                       │
│  • Compare to benchmarks                                 │
│  • Extract insights                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│         RECOMMENDATION ENGINE                            │
│  • Generate personalized suggestions                     │
│  • Prioritize by impact                                  │
│  • Consider feasibility                                  │
│  • Calculate savings                                     │
└─────────────────────────────────────────────────────────┘
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
┌─────────────────────┐   ┌─────────────────────┐
│  PREDICTION ENGINE  │   │  ECO TWIN SIMULATOR │
│                     │   │                     │
│  • Forecast future  │   │  • Model scenarios  │
│  • Trend analysis   │   │  • Simulate changes │
│  • Early warnings   │   │  • Compare outcomes │
└─────────────────────┘   └─────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│            RESPONSE GENERATOR                             │
│  • Format output                                          │
│  • Add visualizations                                     │
│  • Include action items                                   │
│  • Generate follow-ups                                    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│            DASHBOARD INSIGHTS UPDATE                      │
└──────────────────────────────────────────────────────────┘
```

### RAG Architecture (Retrieval-Augmented Generation)

```
┌──────────────────────────────────────────────────────────┐
│                   USER QUERY                              │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│              QUERY EMBEDDING                              │
│  OpenAI Ada-002 Embedding Model                          │
│  • Convert query to vector (1536 dimensions)             │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│          VECTOR SIMILARITY SEARCH                         │
│  Pinecone Vector Database                                │
│  • Search knowledge base                                 │
│  • Retrieve top-k relevant documents (k=5)               │
│  • Include metadata (source, date, relevance)            │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│         CONTEXT AUGMENTATION                              │
│  • User profile data                                     │
│  • Current carbon footprint                              │
│  • Historical behavior                                   │
│  • Retrieved knowledge documents                         │
│  • Conversation history                                  │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│          PROMPT CONSTRUCTION                              │
│  System Prompt + Context + User Query                    │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│        CLAUDE OPUS 4.5 GENERATION                         │
│  • Process augmented prompt                              │
│  • Generate contextual response                          │
│  • Include citations                                     │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│         POST-PROCESSING                                   │
│  • Format response                                       │
│  • Add source references                                 │
│  • Extract action items                                  │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│              RETURN TO USER                               │
└──────────────────────────────────────────────────────────┘
```

### Knowledge Base Structure (Pinecone)

**Vector Collections:**

1. **Sustainability Knowledge**
   - Scientific papers
   - Carbon calculation methodologies
   - Environmental impact data
   - Climate science facts

2. **Recommendation Templates**
   - Proven reduction strategies
   - Case studies
   - Best practices
   - Implementation guides

3. **Educational Content**
   - Sustainability concepts
   - Carbon terminology
   - How-to guides
   - FAQs

4. **User Behavior Patterns**
   - Anonymized successful transitions
   - Common challenges
   - Solution patterns

**Metadata Schema:**
```json
{
  "id": "doc_12345",
  "text": "Document content...",
  "embedding": [0.123, -0.456, ...],
  "metadata": {
    "source": "IPCC Report 2023",
    "category": "transportation",
    "topic": "electric_vehicles",
    "relevance_score": 0.95,
    "last_updated": "2026-01-15",
    "verified": true
  }
}
```

### Agent Tool Ecosystem

**Tools Available to Agents:**

1. **calculator_tool**
   - Calculate carbon emissions
   - Apply emission factors
   - Convert units

2. **knowledge_base_tool**
   - Query vector database
   - Retrieve relevant information
   - Cite sources

3. **analysis_tool**
   - Analyze user behavior
   - Identify patterns
   - Generate insights

4. **recommendation_tool**
   - Generate suggestions
   - Prioritize recommendations
   - Calculate impacts

5. **prediction_tool**
   - Forecast emissions
   - Trend analysis
   - Scenario modeling

6. **simulation_tool**
   - Eco Twin simulation
   - What-if analysis
   - Comparative modeling

---

## Frontend Architecture

### Next.js 15 App Router Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx (Root layout)
│   │   ├── page.tsx (Home page)
│   │   ├── globals.css
│   │   │
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   └── callback/
│   │   │
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx (Dashboard layout)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── calculator/
│   │   │   │   └── page.tsx
│   │   │   ├── advisor/
│   │   │   │   └── page.tsx
│   │   │   ├── eco-twin/
│   │   │   │   └── page.tsx
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx
│   │   │   ├── challenges/
│   │   │   │   └── page.tsx
│   │   │   ├── leaderboard/
│   │   │   │   └── page.tsx
│   │   │   ├── learning/
│   │   │   │   └── page.tsx
│   │   │   └── profile/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/
│   │       └── auth/
│   │           └── [...nextauth]/
│   │               └── route.ts
│   │
│   ├── components/
│   │   ├── ui/ (ShadCN components)
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── calculator/
│   │   ├── ai/
│   │   ├── analytics/
│   │   ├── gamification/
│   │   └── shared/
│   │
│   ├── lib/
│   │   ├── api.ts (API client)
│   │   ├── auth.ts (Auth utilities)
│   │   ├── utils.ts (Helpers)
│   │   └── constants.ts
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useCarbon.ts
│   │   ├── useAI.ts
│   │   ├── useGamification.ts
│   │   └── useAnalytics.ts
│   │
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── carbonStore.ts
│   │   ├── uiStore.ts
│   │   └── chatStore.ts
│   │
│   ├── types/
│   │   ├── user.ts
│   │   ├── carbon.ts
│   │   ├── ai.ts
│   │   └── gamification.ts
│   │
│   └── styles/
│       └── themes.css
│
├── public/
│   ├── images/
│   ├── icons/
│   └── fonts/
│
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

### State Management Strategy

**Zustand Stores:**

```typescript
// authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

// carbonStore.ts
interface CarbonState {
  currentFootprint: CarbonFootprint | null;
  history: CarbonFootprint[];
  breakdown: CategoryBreakdown[];
  calculateFootprint: (data: CarbonInput) => Promise<void>;
  fetchHistory: () => Promise<void>;
}

// chatStore.ts
interface ChatState {
  conversations: Conversation[];
  activeConversation: string | null;
  messages: Message[];
  isTyping: boolean;
  sendMessage: (message: string) => Promise<void>;
  loadConversation: (id: string) => Promise<void>;
}
```

### API Client Configuration

```typescript
// lib/api.ts
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
  const token = localStorage.getItem('token');
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
      // Handle token refresh
    }
    return Promise.reject(error);
  }
);
```

---

## Backend Architecture

### FastAPI Application Structure

**Main Application (main.py):**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.core.database import engine
from app.api.v1 import api_router
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Service Layer Pattern

```python
# services/carbon_service.py
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.carbon_footprint import CarbonFootprint
from app.schemas.carbon import CarbonInput, CarbonResult
from app.agents.carbon_engine import CarbonEngine

class CarbonService:
    def __init__(self, db: Session):
        self.db = db
        self.carbon_engine = CarbonEngine()
    
    async def calculate_footprint(
        self,
        user_id: str,
        data: CarbonInput
    ) -> CarbonResult:
        # Calculate using AI engine
        result = await self.carbon_engine.calculate(data)
        
        # Save to database
        footprint = CarbonFootprint(
            user_id=user_id,
            monthly_kg=result.monthly_kg,
            annual_tons=result.annual_tons,
            grade=result.grade,
            breakdown=result.breakdown
        )
        self.db.add(footprint)
        self.db.commit()
        
        # Update cache
        await self._update_cache(user_id, result)
        
        return result
    
    async def get_history(
        self,
        user_id: str,
        limit: int = 12
    ) -> List[CarbonFootprint]:
        return self.db.query(CarbonFootprint)\
            .filter(CarbonFootprint.user_id == user_id)\
            .order_by(CarbonFootprint.created_at.desc())\
            .limit(limit)\
            .all()
```

### Dependency Injection

```python
# api/deps.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

---

(Continued in next sections due to length...)


## Database Architecture

### PostgreSQL Schema Overview

**Core Tables:**
- users
- carbon_footprints
- carbon_categories
- recommendations
- conversations
- messages
- achievements
- challenges
- leaderboards
- learning_content

**Detailed schema available in DATABASE_SCHEMA.md**

### Redis Cache Strategy

**Cache Keys:**
```
user:{user_id}:profile          # TTL: 1 hour
user:{user_id}:carbon:latest    # TTL: 5 minutes
user:{user_id}:recommendations  # TTL: 1 hour
conversation:{conv_id}:messages # TTL: 24 hours
leaderboard:global              # TTL: 5 minutes
leaderboard:weekly              # TTL: 1 minute
```

**Cache Patterns:**
1. **Cache-Aside:** Read-through caching
2. **Write-Through:** Update cache on write
3. **Cache Invalidation:** TTL-based + manual invalidation

---

## Infrastructure Architecture

### AWS Services Used

```
┌─────────────────────────────────────────────────────────┐
│                    Route 53 (DNS)                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              CloudFront (CDN)                            │
│  • Edge caching                                          │
│  • SSL/TLS termination                                   │
│  • DDoS protection                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│         Application Load Balancer (ALB)                  │
│  • Health checks                                         │
│  • SSL termination                                       │
│  • Path-based routing                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                     ↓
┌──────────────────┐               ┌──────────────────┐
│   ECS Cluster    │               │   ECS Cluster    │
│   (Frontend)     │               │   (Backend)      │
│                  │               │                  │
│  Next.js Pods    │               │  FastAPI Pods    │
│  (Auto-scaling)  │               │  (Auto-scaling)  │
└──────────────────┘               └──────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    VPC (Private Subnet)                  │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  RDS          │  │  ElastiCache │  │    S3        │  │
│  │ (PostgreSQL) │  │   (Redis)    │  │  (Storage)   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Container Architecture

**Frontend Container (Dockerfile):**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
```

**Backend Container (Dockerfile):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./app ./app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Auto-Scaling Configuration

**ECS Auto-Scaling Policy:**
```yaml
TargetTrackingScaling:
  Frontend:
    TargetValue: 70.0  # CPU utilization %
    ScaleInCooldown: 300
    ScaleOutCooldown: 60
    MinCapacity: 2
    MaxCapacity: 20
  
  Backend:
    TargetValue: 75.0  # CPU utilization %
    ScaleInCooldown: 300
    ScaleOutCooldown: 60
    MinCapacity: 3
    MaxCapacity: 30
```

---

## Security Architecture

### Authentication Flow

```
1. User clicks "Login with Google"
   ↓
2. Redirect to Google OAuth
   ↓
3. User authorizes
   ↓
4. Google redirects with auth code
   ↓
5. Backend exchanges code for tokens
   ↓
6. Backend creates user session
   ↓
7. Backend generates JWT
   ↓
8. Frontend stores JWT (httpOnly cookie)
   ↓
9. JWT included in subsequent requests
```

### Security Layers

**1. Network Security:**
- VPC with public/private subnets
- Security groups (firewall rules)
- Network ACLs
- WAF (Web Application Firewall)

**2. Application Security:**
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- XSS protection (Content Security Policy)
- CSRF tokens
- Rate limiting

**3. Data Security:**
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Database encryption
- Secrets management (AWS Secrets Manager)

**4. Authentication & Authorization:**
- OAuth 2.0
- JWT with short expiry (15 minutes)
- Refresh tokens (7 days)
- Role-based access control (RBAC)

### Compliance

**GDPR Compliance:**
- Right to access
- Right to deletion
- Right to portability
- Data minimization
- Consent management
- Privacy by design

**Data Retention:**
- User data: Until account deletion
- Logs: 90 days
- Analytics: 2 years (anonymized)
- Backups: 30 days

---

## Scalability & Performance

### Performance Optimization Strategies

**Frontend:**
- Code splitting
- Lazy loading
- Image optimization (Next.js Image)
- Static generation where possible
- CDN for assets
- Service worker caching

**Backend:**
- Database connection pooling
- Query optimization (indexes)
- Async I/O operations
- Response caching
- Database read replicas
- Background job processing

**AI Layer:**
- Response streaming
- Prompt caching
- Batch processing
- Rate limiting
- Fallback mechanisms

### Load Testing Targets

| Metric | Target | Max |
|--------|--------|-----|
| Concurrent Users | 10,000 | 50,000 |
| Requests/second | 1,000 | 5,000 |
| API Response Time (p95) | 200ms | 500ms |
| AI Response Time (p95) | 3s | 5s |
| Database Query Time (p95) | 50ms | 100ms |

---

## Monitoring & Observability

### Monitoring Stack

**Application Monitoring:**
- OpenTelemetry instrumentation
- Distributed tracing
- Metrics collection
- Error tracking (Sentry)

**AI Monitoring:**
- LangSmith for agent tracking
- Token usage monitoring
- Response quality metrics
- Cost tracking

**Infrastructure Monitoring:**
- CloudWatch metrics
- CloudWatch logs
- CloudWatch alarms
- Custom dashboards

### Key Metrics

**Application Metrics:**
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Availability (uptime)

**Business Metrics:**
- User signups
- Carbon calculations
- AI conversations
- Recommendation adoptions
- Active users (DAU/MAU)

**AI Metrics:**
- AI request rate
- Average tokens per request
- AI response time
- Success rate
- Cost per request

### Alerting

**Critical Alerts:**
- API error rate > 5%
- Response time p95 > 1s
- Database connection failures
- AI API failures
- Downtime > 1 minute

**Warning Alerts:**
- API error rate > 2%
- Response time p95 > 500ms
- High CPU usage (> 80%)
- High memory usage (> 85%)
- Slow database queries

---

## Disaster Recovery

### Backup Strategy

**Database Backups:**
- Automated daily snapshots
- Point-in-time recovery (PITR)
- Cross-region replication
- Retention: 30 days

**Application Backups:**
- Infrastructure as Code (Terraform)
- Container images in ECR
- Configuration in Git

### Recovery Objectives

- **RPO (Recovery Point Objective):** 1 hour
- **RTO (Recovery Time Objective):** 4 hours

### Failover Procedures

1. **Database Failover:**
   - Automatic promotion of read replica
   - DNS update to new endpoint
   - Application reconnection

2. **Application Failover:**
   - Multi-AZ deployment
   - Auto-scaling handles failures
   - Health checks trigger replacement

---

## Development Workflow

### Local Development

```bash
# Clone repository
git clone https://github.com/org/footprintiq.git

# Start infrastructure
docker-compose up -d postgres redis

# Frontend development
cd frontend
npm install
npm run dev  # http://localhost:3000

# Backend development
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # http://localhost:8000
```

### Deployment Pipeline

```
┌─────────────┐
│  Developer  │
│  Commits    │
└──────┬──────┘
       ↓
┌─────────────┐
│  Git Push   │
│  to Branch  │
└──────┬──────┘
       ↓
┌──────────────────────┐
│  GitHub Actions      │
│  • Lint              │
│  • Type check        │
│  • Unit tests        │
│  • Build             │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│  Pull Request        │
│  • Code review       │
│  • Integration tests │
│  • Preview deploy    │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│  Merge to Main       │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│  Production Deploy   │
│  • Build containers  │
│  • Push to ECR       │
│  • Update ECS        │
│  • Run migrations    │
│  • Health checks     │
└──────────────────────┘
```

---

## Architecture Decision Records (ADRs)

### ADR-001: Why Next.js 15 for Frontend?

**Decision:** Use Next.js 15 with App Router

**Rationale:**
- Server-side rendering for SEO
- Built-in optimization (images, fonts)
- File-based routing
- TypeScript support
- Large ecosystem

**Alternatives Considered:**
- React SPA (no SSR)
- Vue.js/Nuxt (smaller ecosystem)

### ADR-002: Why FastAPI for Backend?

**Decision:** Use FastAPI with Python

**Rationale:**
- Native async support
- Automatic API documentation
- Pydantic validation
- Great AI library ecosystem
- High performance

**Alternatives Considered:**
- Django (heavier, slower)
- Node.js/Express (different language)
- Go (less AI tooling)

### ADR-003: Why Claude Opus 4.5?

**Decision:** Use Anthropic Claude as primary AI model

**Rationale:**
- Superior reasoning capabilities
- Large context window (200k tokens)
- Strong factual accuracy
- Function calling support
- Reasonable pricing

**Alternatives Considered:**
- GPT-4 (more expensive)
- Open source models (less capable)

### ADR-004: Why PostgreSQL over NoSQL?

**Decision:** Use PostgreSQL as primary database

**Rationale:**
- ACID compliance
- Complex queries support
- Relational data model fits use case
- JSON support for flexibility
- Mature ecosystem

**Alternatives Considered:**
- MongoDB (weaker consistency)
- DynamoDB (vendor lock-in)

---

## Conclusion

This architecture provides:
- **Scalability:** Handle 100,000+ users
- **Performance:** Sub-200ms API responses
- **Reliability:** 99.9% uptime
- **Security:** Enterprise-grade protection
- **Maintainability:** Clean separation of concerns
- **Extensibility:** Easy to add features

The system is designed for hackathon demonstration while being production-ready and enterprise-scalable.

---

**Document Owner:** Technical Architect  
**Last Updated:** June 17, 2026  
**Next Review:** July 17, 2026  
**Status:** APPROVED FOR IMPLEMENTATION
