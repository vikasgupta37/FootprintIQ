/**
 * TypeScript type definitions for all API contracts.
 */

// ── User ────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  full_name: string;
  username?: string;
  avatar_url?: string;
  role: 'user' | 'premium' | 'admin' | 'corporate_manager';
  country?: string;
  city?: string;
  bio?: string;
  household_size: number;
  total_points: number;
  level: number;
  current_streak: number;
  longest_streak: number;
  carbon_saved_kg: number;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  user: User;
  tokens: TokenResponse;
}

// ── Carbon ──────────────────────────────────────────────────

export interface TransportationInput {
  vehicle_type: string;
  km_per_month: number;
  public_transport_km: number;
  flights_short_haul: number;
  flights_long_haul: number;
  bicycle_walking_pct: number;
}

export interface EnergyInput {
  electricity_kwh_per_month: number;
  renewable_percentage: number;
  natural_gas: boolean;
  heating_type: string;
  ac_usage_hours: number;
  household_size: number;
}

export interface FoodInput {
  diet_type: string;
  dairy_consumption: string;
  food_waste_pct: number;
  local_produce_pct: number;
}

export interface ShoppingInput {
  clothing_items_per_month: number;
  electronics_per_year: number;
  online_deliveries_per_month: number;
  second_hand_pct: number;
}

export interface WasteInput {
  recycling_frequency: string;
  composting: boolean;
  plastic_usage: string;
  reusable_water_bottle: boolean;
}

export interface CarbonCalculateRequest {
  transportation: TransportationInput;
  energy: EnergyInput;
  food: FoodInput;
  shopping: ShoppingInput;
  waste: WasteInput;
}

export interface CategoryBreakdown {
  category: string;
  monthly_kg: number;
  percentage: number;
  details?: Record<string, number>;
}

export interface CarbonScore {
  id: string;
  monthly_kg: number;
  annual_tons: number;
  daily_kg: number;
  grade: 'EXCELLENT' | 'GOOD' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  grade_color: string;
  breakdown: CategoryBreakdown[];
  comparisons: Record<string, number>;
  insights: string[];
  created_at: string;
}

// ── AI Chat ─────────────────────────────────────────────────

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  created_at: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  content: string;
  intent?: string;
  agent_used?: string;
  suggestions: string[];
  created_at: string;
}

export interface Conversation {
  id: string;
  title?: string;
  message_count: number;
  last_intent?: string;
  created_at: string;
  updated_at: string;
}

// ── Recommendations ─────────────────────────────────────────

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  detailed_steps: Record<string, unknown>[];
  category: string;
  difficulty: 'easy' | 'medium' | 'hard';
  priority_score: number;
  estimated_co2_savings_kg: number;
  estimated_cost_savings: number;
  estimated_time_weeks: number;
  impact_level: 'low' | 'medium' | 'high';
  status: string;
  confidence_score: number;
  created_at: string;
}

// ── Gamification ────────────────────────────────────────────

export interface PointsData {
  points: number;
  level: number;
  level_progress: number;
  next_level_points: number;
  total_points_earned: number;
  badges_unlocked: number;
  challenges_completed: number;
  current_streak: number;
  longest_streak: number;
}

export interface Badge {
  id: string;
  name: string;
  display_name: string;
  description: string;
  icon_url?: string;
  category: string;
  rarity: string;
  points_awarded: number;
  unlocked: boolean;
  unlocked_at?: string;
  progress: number;
}

export interface Challenge {
  id: string;
  name: string;
  display_name: string;
  description: string;
  category: string;
  challenge_type: string;
  difficulty: string;
  duration_days: number;
  points_reward: number;
  start_date?: string;
  end_date?: string;
  participant_count: number;
  user_status?: string;
  user_progress?: Record<string, unknown>;
}

export interface LeaderboardEntry {
  rank: number;
  user: { id: string; username: string; avatar_url?: string; level: number };
  score: number;
  percentile?: number;
}

// ── Eco Twin ────────────────────────────────────────────────

export interface SimulationResult {
  simulation_id: string;
  scenario_name: string;
  baseline: { annual_tons: number; monthly_kg: number };
  simulated: { annual_tons: number; monthly_kg: number };
  impact: { reduction_tons: number; reduction_percentage: number; equivalent_trees: number };
  financial: { upfront_cost: number; annual_savings: number; payback_period_years: number };
  feasibility: { difficulty_score: number; timeline_months: number; ai_recommendation_score: number };
  created_at: string;
}

export interface PrebuiltScenario {
  id: string;
  name: string;
  description: string;
  expected_reduction_pct: number;
  difficulty: string;
  estimated_cost: string;
}

// ── Analytics ───────────────────────────────────────────────

export interface DashboardData {
  period: string;
  carbon_metrics: {
    current_footprint: number;
    previous_footprint: number;
    change_pct: number;
    trend: string;
  };
  engagement: Record<string, number>;
  achievements: Record<string, number>;
  impact: Record<string, number>;
}
