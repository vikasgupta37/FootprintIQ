'use client';

import { useEffect, useState } from 'react';
import { ArrowRight, Car, Leaf, Sparkles, Sun, TreePine, Utensils, Zap } from 'lucide-react';
import apiClient from '@/lib/api-client';
import type { PrebuiltScenario, SimulationResult } from '@/types';

const SCENARIO_ICONS: Record<string, any> = {
  scenario_ev: Car,
  scenario_plant_based: Utensils,
  scenario_zero_waste: TreePine,
  scenario_remote: Sparkles,
  scenario_green_energy: Sun,
  scenario_sustainable: Leaf,
};

export default function EcoTwinPage() {
  const [scenarios, setScenarios] = useState<PrebuiltScenario[]>([]);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    apiClient.get('/eco-twin/scenarios')
      .then(({ data }) => setScenarios(data.scenarios))
      .catch(console.error);
  }, []);

  const runScenario = async (scenario: PrebuiltScenario) => {
    setLoading(true);
    try {
      const { data } = await apiClient.post('/eco-twin/simulate', {
        scenario_name: scenario.name,
        changes: [
          { category: 'transportation', change_type: 'replace_vehicle' },
          { category: 'energy', change_type: 'add_renewable' },
        ],
      });
      setResult(data);
    } catch (err) {
      console.error('Simulation failed', err);
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="max-w-3xl mx-auto animate-fade-in space-y-6">
        <button onClick={() => setResult(null)} className="btn-ghost text-sm">
          ← Back to scenarios
        </button>

        <h1 className="text-3xl font-display font-bold">{result.scenario_name}</h1>

        {/* Before/After */}
        <div className="grid md:grid-cols-2 gap-4">
          <div className="card p-6 border-l-4 border-red-500">
            <div className="text-sm text-slate-400 mb-1">Current Footprint</div>
            <div className="text-3xl font-display font-bold">{result.baseline.annual_tons}</div>
            <div className="text-sm text-slate-500">tons CO₂e / year</div>
          </div>
          <div className="card p-6 border-l-4 border-brand-500">
            <div className="text-sm text-slate-400 mb-1">After Changes</div>
            <div className="text-3xl font-display font-bold text-brand-400">{result.simulated.annual_tons}</div>
            <div className="text-sm text-slate-500">tons CO₂e / year</div>
          </div>
        </div>

        {/* Impact */}
        <div className="card p-6 bg-gradient-to-br from-brand-950 to-surface-800">
          <h2 className="font-display font-semibold text-lg mb-4 text-brand-400">Impact Summary</h2>
          <div className="grid grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-display font-bold text-brand-400">
                -{result.impact.reduction_percentage}%
              </div>
              <div className="text-sm text-slate-400">Reduction</div>
            </div>
            <div>
              <div className="text-3xl font-display font-bold text-emerald-400">
                {result.impact.reduction_tons}
              </div>
              <div className="text-sm text-slate-400">Tons saved/year</div>
            </div>
            <div>
              <div className="text-3xl font-display font-bold text-green-400">
                🌳 {result.impact.equivalent_trees}
              </div>
              <div className="text-sm text-slate-400">Trees equivalent</div>
            </div>
          </div>
        </div>

        {/* Financial */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">💰 Financial Impact</h2>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold">${result.financial.upfront_cost.toLocaleString()}</div>
              <div className="text-xs text-slate-500">Upfront Cost</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-brand-400">${result.financial.annual_savings.toLocaleString()}</div>
              <div className="text-xs text-slate-500">Annual Savings</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{result.financial.payback_period_years} yrs</div>
              <div className="text-xs text-slate-500">Payback Period</div>
            </div>
          </div>
        </div>

        {/* Feasibility */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">📊 Feasibility</h2>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>Difficulty</span>
                <span>{result.feasibility.difficulty_score}/100</span>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: `${result.feasibility.difficulty_score}%` }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span>AI Recommendation</span>
                <span>{result.feasibility.ai_recommendation_score}/100</span>
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-brand-500 rounded-full" style={{ width: `${result.feasibility.ai_recommendation_score}%` }} />
              </div>
            </div>
            <div className="text-sm text-slate-400 mt-2">
              Estimated timeline: <span className="text-white font-medium">{result.feasibility.timeline_months} months</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-display font-bold">Eco Twin™ Simulator</h1>
        <p className="text-slate-400 mt-1">Simulate lifestyle changes and see their environmental impact before you commit.</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scenarios.map((scenario) => {
          const Icon = SCENARIO_ICONS[scenario.id] || Sparkles;
          return (
            <div key={scenario.id} className="card p-6 group hover:border-brand-500/30 transition-all duration-300">
              <div className="w-12 h-12 rounded-xl bg-brand-500/10 flex items-center justify-center text-brand-400 mb-4 group-hover:bg-brand-500/20 transition">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{scenario.name}</h3>
              <p className="text-sm text-slate-400 mb-4">{scenario.description}</p>
              <div className="flex items-center justify-between text-xs text-slate-500 mb-4">
                <span className="px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400">
                  -{scenario.expected_reduction_pct}% CO₂
                </span>
                <span>{scenario.difficulty}</span>
                <span>{scenario.estimated_cost}</span>
              </div>
              <button
                onClick={() => runScenario(scenario)}
                disabled={loading}
                className="btn-primary w-full text-sm disabled:opacity-50"
              >
                Simulate <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
