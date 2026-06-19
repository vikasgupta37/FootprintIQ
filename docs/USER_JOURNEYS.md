# User Journey & Workflow Diagrams
# FootprintIQ

**Version:** 1.0.0  
**Date:** June 17, 2026

---

## User Journey 1: New User Onboarding

```
[Landing Page] → [Sign Up] → [Welcome] → [Calculator] → [Results] → [AI Recommendations] → [Dashboard]
     ↓              ↓           ↓            ↓            ↓               ↓                    ↓
  Learn More    Google OAuth  Profile    Input Data   View Score   Chat with AI        Explore Features
                              Setup
```

**Detailed Flow:**

1. **Landing Page (0-30s)**
   - Hero: "Smarter Choices. Smaller Footprints."
   - Value proposition
   - CTA: "Calculate Your Footprint"
   - Social proof: "200,000+ users, 10,000 tons CO2 saved"

2. **Sign Up (30s-1min)**
   - Google OAuth (1-click)
   - OR Email/password
   - Terms acceptance
   - → Confirmation email sent

3. **Welcome & Profile (1-2min)**
   - Quick tour (optional, skippable)
   - Basic profile: Name, country, preferences
   - → Redirects to calculator

4. **Carbon Calculator (3-5min)**
   - Multi-step form (5 categories)
   - Progress indicator
   - Helpful tooltips
   - Auto-save drafts
   - → Submit calculation

5. **Results Display (Immediate)**
   - Carbon score revealed
   - Grade with animation
   - Category breakdown
   - Comparisons
   - → Insights from AI

6. **AI Recommendations (1-2min)**
   - Top 3 personalized suggestions
   - Impact quantification
   - Accept/Reject options
   - → Explore more in dashboard

7. **Dashboard (Ongoing)**
   - Overview of all features
   - Quick actions
   - Challenges, badges
   - → Regular engagement

**Total Time to Value:** < 10 minutes

---

## User Journey 2: Returning User Engagement

```
[Login] → [Dashboard] → [Check Progress] → [AI Chat] → [Accept Recommendation] → [Track Action]
   ↓          ↓              ↓                ↓                ↓                      ↓
Quick      Overview      Trends/Stats    Ask Question    Start Challenge        Log Progress
```

**Weekly Engagement Pattern:**

**Day 1 (Monday):**
- Login
- Check weekend progress
- Join "Green Commute Week" challenge

**Day 3 (Wednesday):**
- Quick dashboard check
- Log public transport trip
- Earn 50 points

**Day 5 (Friday):**
- AI chat: "Best electric vehicles?"
- Browse Eco Twin scenarios
- Share badge on social media

**Day 7 (Sunday):**
- Review weekly summary email
- Complete quiz (100 points)
- Unlock new badge

---

## Workflow: Carbon Footprint Calculation

```
Start
  ↓
[Transportation Input]
  ├─ Vehicle type
  ├─ Monthly km
  ├─ Public transport
  ├─ Flights
  └─ Bicycle/Walking %
  ↓
[Energy Input]
  ├─ Electricity kWh
  ├─ Renewable %
  ├─ AC usage
  ├─ Heating type
  └─ Household size
  ↓
[Food Input]
  ├─ Diet type
  ├─ Dairy consumption
  ├─ Food waste
  └─ Local produce
  ↓
[Shopping Input]
  ├─ Clothing purchases
  ├─ Electronics
  ├─ Online deliveries
  └─ Second-hand preference
  ↓
[Waste Input]
  ├─ Recycling frequency
  ├─ Composting
  ├─ Plastic usage
  └─ Water bottle type
  ↓
[AI Processing] (2-3s)
  ├─ Calculate emissions
  ├─ Assign grade
  ├─ Generate insights
  └─ Create recommendations
  ↓
[Results Display]
  ├─ Carbon score
  ├─ Breakdown chart
  ├─ Comparisons
  ├─ Insights
  └─ Recommendations
  ↓
[Save to Database]
  ↓
[Trigger Background Jobs]
  ├─ Generate detailed recommendations
  ├─ Update analytics
  ├─ Check badge progress
  └─ Send notifications
  ↓
End
```

---

## Workflow: AI Conversation

```
User: "How can I reduce my footprint?"
  ↓
[Orchestrator Agent]
  ├─ Classify intent: "recommendation_request"
  ├─ Load user context
  └─ Route to: Recommendation Engine
  ↓
[Recommendation Engine]
  ├─ Analyze carbon profile
  ├─ Query knowledge base (RAG)
  ├─ Generate personalized suggestions
  └─ Prioritize by impact
  ↓
[Response Generator]
  ├─ Format conversational response
  ├─ Add action buttons
  ├─ Include follow-up suggestions
  └─ Stream to user (token-by-token)
  ↓
User sees response in real-time
  ↓
[User can:]
  ├─ Accept recommendation
  ├─ Ask follow-up
  ├─ Run Eco Twin simulation
  └─ View detailed guide
```

---

## Workflow: Eco Twin Simulation

```
User clicks "New Simulation"
  ↓
[Scenario Selection]
  ├─ Pre-built scenarios
  OR
  └─ Custom scenario
  ↓
[Change Configuration]
  ├─ Transportation changes
  ├─ Energy changes
  ├─ Food changes
  ├─ Shopping changes
  └─ Waste changes
  ↓
[Run Simulation] (1-2s)
  ├─ Load baseline state
  ├─ Apply changes
  ├─ Calculate new emissions
  ├─ Compute reduction
  ├─ Financial analysis
  └─ Feasibility assessment
  ↓
[Results Display]
  ├─ Side-by-side comparison
  ├─ Reduction percentage
  ├─ Cost analysis
  ├─ Timeline projection
  ├─ Feasibility score
  └─ Recommendations
  ↓
[User Actions]
  ├─ Save simulation
  ├─ Compare with other scenarios
  ├─ Accept as goal
  └─ Share results
```

---

## Admin Workflow: Content Management

```
Admin Login
  ↓
[Admin Dashboard]
  ↓
[Content Management]
  ├─ Create Article
  │   ├─ Write content (Markdown)
  │   ├─ Add metadata
  │   ├─ Upload images
  │   ├─ Preview
  │   └─ Publish
  │
  ├─ Create Challenge
  │   ├─ Define requirements
  │   ├─ Set dates
  │   ├─ Configure rewards
  │   └─ Activate
  │
  ├─ Create Badge
  │   ├─ Design badge
  │   ├─ Set criteria
  │   ├─ Assign points
  │   └─ Publish
  │
  └─ Manage Users
      ├─ View analytics
      ├─ Support tickets
      ├─ Moderate content
      └─ Export reports
```

---

## Data Flow: Complete Platform

```
[User Action]
  ↓
[Frontend (Next.js)]
  ├─ Validate input
  ├─ Update UI state (Zustand)
  └─ API call
  ↓
[API Gateway (FastAPI)]
  ├─ Authenticate (JWT)
  ├─ Rate limit check
  ├─ Validate request
  └─ Route to service
  ↓
[Service Layer]
  ├─ Business logic
  ├─ Database queries
  ├─ Cache check/update
  └─ Call AI agents (if needed)
  ↓
[AI Agent Layer] (if applicable)
  ├─ Process with Claude
  ├─ RAG retrieval (Pinecone)
  ├─ Tool calling
  └─ Generate response
  ↓
[Data Layer]
  ├─ PostgreSQL (primary data)
  ├─ Redis (cache)
  ├─ Pinecone (vectors)
  └─ S3 (files)
  ↓
[Response Processing]
  ├─ Format response
  ├─ Add metadata
  └─ Return to frontend
  ↓
[Frontend Update]
  ├─ Update state
  ├─ Re-render UI
  ├─ Show notifications
  └─ Track analytics
```

---

**Document Owner:** UX Team  
**Last Updated:** June 17, 2026
