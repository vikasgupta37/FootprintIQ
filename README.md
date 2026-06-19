# FootprintIQ

> AI-Powered Carbon Footprint Awareness Platform

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (frontend development)
- Python 3.11+ (backend development)

### 1. Clone & Setup
```bash
cd FootprintIQ

# Copy env file and fill in API keys
cp backend/.env.example backend/.env
```

### 2. Start with Docker
```bash
docker compose up -d
```

Services:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Run Tests
```bash
cd backend
pytest tests/ -v
```

## Tech Stack

| Layer       | Technology                   |
|-------------|------------------------------|
| Frontend    | Next.js 15, TypeScript, Tailwind CSS |
| Backend     | FastAPI, Python 3.11         |
| Database    | PostgreSQL 15                |
| Cache       | Redis 7                      |
| AI          | Claude (Anthropic)           |
| Vector DB   | Pinecone                     |
| Auth        | JWT + Google OAuth           |
| Deployment  | Docker, AWS ECS Fargate      |

## Project Structure
```
FootprintIQ/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Route handlers
│   │   ├── core/            # Config, DB, cache, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages (App Router)
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/             # API client, utilities
│   │   ├── stores/          # Zustand state management
│   │   └── types/           # TypeScript definitions
│   └── Dockerfile
├── docs/                    # Architecture & planning docs
└── docker-compose.yml
```

## Features
- 🧮 **Carbon Calculator** — 5-category footprint calculation with IPCC emission factors
- 🤖 **AI Advisor** — Conversational sustainability advice powered by Claude
- 🪞 **Eco Twin™** — Simulate lifestyle changes before committing
- 🏆 **Gamification** — Points, badges, challenges, and leaderboards
- 📊 **Analytics** — Trend tracking and future predictions
- 📚 **Learning Center** — Articles and quizzes about sustainability
