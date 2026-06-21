'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, ArrowRight, Car, Factory, Leaf, ShoppingBag, Trash, Utensils, Zap } from 'lucide-react';
import { useCarbonStore } from '@/stores';
import type { CarbonCalculateRequest, CarbonScore } from '@/types';

const STEPS = [
  { key: 'transportation', icon: Car, label: 'Transportation', color: 'text-blue-400' },
  { key: 'energy', icon: Zap, label: 'Energy', color: 'text-amber-400' },
  { key: 'food', icon: Utensils, label: 'Food', color: 'text-green-400' },
  { key: 'shopping', icon: ShoppingBag, label: 'Shopping', color: 'text-purple-400' },
  { key: 'waste', icon: Trash, label: 'Waste', color: 'text-red-400' },
];

const GRADE_STYLES: Record<string, string> = {
  EXCELLENT: 'from-emerald-500 to-green-500',
  GOOD: 'from-green-400 to-emerald-500',
  MODERATE: 'from-amber-400 to-yellow-500',
  HIGH: 'from-orange-400 to-red-400',
  CRITICAL: 'from-red-500 to-rose-600',
};

export default function CalculatorPage() {
  const [step, setStep] = useState(0);
  const [result, setResult] = useState<CarbonScore | null>(null);
  const { calculate, isCalculating } = useCarbonStore();

  const [formData, setFormData] = useState<CarbonCalculateRequest>({
    transportation: { vehicle_type: 'car_petrol', km_per_month: 800, public_transport_km: 100, flights_short_haul: 2, flights_long_haul: 1, bicycle_walking_pct: 10 },
    energy: { electricity_kwh_per_month: 300, renewable_percentage: 0, natural_gas: false, heating_type: 'electric', ac_usage_hours: 2, household_size: 2 },
    food: { diet_type: 'mixed', dairy_consumption: 'moderate', food_waste_pct: 15, local_produce_pct: 20 },
    shopping: { clothing_items_per_month: 3, electronics_per_year: 3, online_deliveries_per_month: 6, second_hand_pct: 10 },
    waste: { recycling_frequency: 'sometimes', composting: false, plastic_usage: 'moderate', reusable_water_bottle: false },
  });

  const updateField = (category: string, field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [category]: { ...(prev as any)[category], [field]: value },
    }));
  };

  const handleSubmit = async () => {
    try {
      const score = await calculate(formData as any);
      setResult(score);
    } catch (err) {
      console.error('Calculation failed', err);
    }
  };

  if (result) {
    return (
      <div className="max-w-3xl mx-auto animate-fade-in space-y-6">
        <h1 className="text-3xl font-display font-bold">Your Carbon Footprint</h1>

        {/* Score Card */}
        <div className={`card p-8 bg-gradient-to-br ${GRADE_STYLES[result.grade]} text-white relative overflow-hidden`}>
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-10 translate-x-10" />
          <div className="relative z-10">
            <div className="text-6xl font-display font-bold">{result.monthly_kg.toFixed(0)}</div>
            <div className="text-lg opacity-90">kg CO₂e / month</div>
            <div className="mt-4 flex items-center gap-4">
              <span className="px-3 py-1 rounded-full bg-white/20 text-sm font-semibold">{result.grade}</span>
              <span className="text-sm opacity-80">{result.annual_tons} tons/year</span>
            </div>
          </div>
        </div>

        {/* Breakdown */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">Category Breakdown</h2>
          <div className="space-y-3">
            {result.breakdown.map((cat) => (
              <div key={cat.category} className="flex items-center gap-4">
                <div className="w-28 text-sm capitalize text-slate-400">{cat.category}</div>
                <div className="flex-1">
                  <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-brand-500 to-brand-400 rounded-full transition-all duration-700"
                      style={{ width: `${cat.percentage}%` }}
                    />
                  </div>
                </div>
                <div className="w-20 text-right text-sm font-medium">{cat.monthly_kg.toFixed(1)} kg</div>
                <div className="w-14 text-right text-xs text-slate-500">{cat.percentage.toFixed(0)}%</div>
              </div>
            ))}
          </div>
        </div>

        {/* Insights */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">💡 AI Insights</h2>
          <ul className="space-y-2">
            {result.insights.map((insight, i) => (
              <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                <Leaf className="w-4 h-4 text-brand-400 mt-0.5 flex-shrink-0" />
                {insight}
              </li>
            ))}
          </ul>
        </div>

        {/* Comparisons */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">How You Compare</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(result.comparisons).map(([key, value]) => (
              <div key={key} className="text-center p-3 rounded-xl bg-slate-800/50">
                <div className="text-lg font-bold">{(value as number).toFixed(0)}</div>
                <div className="text-xs text-slate-500 capitalize">{key.replace(/_/g, ' ')}</div>
              </div>
            ))}
          </div>
        </div>

        <button onClick={() => { setResult(null); setStep(0); }} className="btn-secondary">
          Calculate Again
        </button>
      </div>
    );
  }

  const currentStep = STEPS[step];

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <h1 className="text-3xl font-display font-bold mb-2">Carbon Calculator</h1>
      <p className="text-slate-400 mb-8">Answer questions about your lifestyle to calculate your carbon footprint.</p>

      {/* Progress */}
      <div className="flex items-center gap-2 mb-8">
        {STEPS.map((s, i) => (
          <div key={s.key} className="flex items-center gap-2 flex-1">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition ${i <= step ? 'bg-brand-500 text-white' : 'bg-slate-700 text-slate-400'}`}>
              {i + 1}
            </div>
            {i < STEPS.length - 1 && <div className={`flex-1 h-0.5 ${i < step ? 'bg-brand-500' : 'bg-slate-700'}`} />}
          </div>
        ))}
      </div>

      {/* Step Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className={`w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center ${currentStep.color}`}>
          <currentStep.icon className="w-5 h-5" />
        </div>
        <h2 className="text-xl font-display font-semibold">{currentStep.label}</h2>
      </div>

      {/* Step Content */}
      <div className="card p-6 space-y-5">
        {step === 0 && (
          <>
            <div>
              <label htmlFor="vehicle-type" className="block text-sm font-medium mb-2">Vehicle Type</label>
              <select id="vehicle-type" value={formData.transportation.vehicle_type} onChange={(e) => updateField('transportation', 'vehicle_type', e.target.value)} className="input-field">
                <option value="car_petrol">Petrol Car</option>
                <option value="car_diesel">Diesel Car</option>
                <option value="car_hybrid">Hybrid Car</option>
                <option value="ev">Electric Vehicle</option>
                <option value="none">No Vehicle</option>
              </select>
            </div>
            <div>
              <label htmlFor="km-per-month" className="block text-sm font-medium mb-2">Kilometers per month: {formData.transportation.km_per_month}</label>
              <input id="km-per-month" type="range" min="0" max="5000" value={formData.transportation.km_per_month} onChange={(e) => updateField('transportation', 'km_per_month', +e.target.value)} className="w-full accent-brand-500" />
            </div>
            <div>
              <label htmlFor="public-transport-km" className="block text-sm font-medium mb-2">Public transport km/month: {formData.transportation.public_transport_km}</label>
              <input id="public-transport-km" type="range" min="0" max="2000" value={formData.transportation.public_transport_km} onChange={(e) => updateField('transportation', 'public_transport_km', +e.target.value)} className="w-full accent-brand-500" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label htmlFor="flights-short-haul" className="block text-sm font-medium mb-2">Short-haul flights/year</label>
                <input id="flights-short-haul" type="number" min="0" value={formData.transportation.flights_short_haul} onChange={(e) => updateField('transportation', 'flights_short_haul', +e.target.value)} className="input-field" />
              </div>
              <div>
                <label htmlFor="flights-long-haul" className="block text-sm font-medium mb-2">Long-haul flights/year</label>
                <input id="flights-long-haul" type="number" min="0" value={formData.transportation.flights_long_haul} onChange={(e) => updateField('transportation', 'flights_long_haul', +e.target.value)} className="input-field" />
              </div>
            </div>
          </>
        )}
        {step === 1 && (
          <>
            <div>
              <label htmlFor="electricity-kwh" className="block text-sm font-medium mb-2">Electricity (kWh/month): {formData.energy.electricity_kwh_per_month}</label>
              <input id="electricity-kwh" type="range" min="50" max="2000" value={formData.energy.electricity_kwh_per_month} onChange={(e) => updateField('energy', 'electricity_kwh_per_month', +e.target.value)} className="w-full accent-amber-500" />
            </div>
            <div>
              <label htmlFor="renewable-pct" className="block text-sm font-medium mb-2">Renewable %: {formData.energy.renewable_percentage}%</label>
              <input id="renewable-pct" type="range" min="0" max="100" value={formData.energy.renewable_percentage} onChange={(e) => updateField('energy', 'renewable_percentage', +e.target.value)} className="w-full accent-brand-500" />
            </div>
            <div>
              <label htmlFor="heating-type" className="block text-sm font-medium mb-2">Heating Type</label>
              <select id="heating-type" value={formData.energy.heating_type} onChange={(e) => updateField('energy', 'heating_type', e.target.value)} className="input-field">
                <option value="electric">Electric</option>
                <option value="gas">Natural Gas</option>
                <option value="oil">Oil</option>
                <option value="heat_pump">Heat Pump</option>
              </select>
            </div>
            <div>
              <label htmlFor="ac-usage" className="block text-sm font-medium mb-2">AC usage hours/day: {formData.energy.ac_usage_hours}</label>
              <input id="ac-usage" type="range" min="0" max="24" value={formData.energy.ac_usage_hours} onChange={(e) => updateField('energy', 'ac_usage_hours', +e.target.value)} className="w-full accent-amber-500" />
            </div>
          </>
        )}
        {step === 2 && (
          <>
            <div>
              <label htmlFor="diet-type" className="block text-sm font-medium mb-2">Diet Type</label>
              <select id="diet-type" value={formData.food.diet_type} onChange={(e) => updateField('food', 'diet_type', e.target.value)} className="input-field">
                <option value="vegan">Vegan</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="pescatarian">Pescatarian</option>
                <option value="mixed">Mixed (Omnivore)</option>
                <option value="heavy_meat">Heavy Meat</option>
              </select>
            </div>
            <div>
              <label htmlFor="dairy-consumption" className="block text-sm font-medium mb-2">Dairy Consumption</label>
              <select id="dairy-consumption" value={formData.food.dairy_consumption} onChange={(e) => updateField('food', 'dairy_consumption', e.target.value)} className="input-field">
                <option value="none">None</option>
                <option value="low">Low</option>
                <option value="moderate">Moderate</option>
                <option value="high">High</option>
              </select>
            </div>
            <div>
              <label htmlFor="food-waste" className="block text-sm font-medium mb-2">Food Waste: {formData.food.food_waste_pct}%</label>
              <input id="food-waste" type="range" min="0" max="50" value={formData.food.food_waste_pct} onChange={(e) => updateField('food', 'food_waste_pct', +e.target.value)} className="w-full accent-green-500" />
            </div>
            <div>
              <label htmlFor="local-produce" className="block text-sm font-medium mb-2">Local Produce: {formData.food.local_produce_pct}%</label>
              <input id="local-produce" type="range" min="0" max="100" value={formData.food.local_produce_pct} onChange={(e) => updateField('food', 'local_produce_pct', +e.target.value)} className="w-full accent-green-500" />
            </div>
          </>
        )}
        {step === 3 && (
          <>
            <div>
              <label htmlFor="clothing-items" className="block text-sm font-medium mb-2">Clothing items/month: {formData.shopping.clothing_items_per_month}</label>
              <input id="clothing-items" type="range" min="0" max="20" value={formData.shopping.clothing_items_per_month} onChange={(e) => updateField('shopping', 'clothing_items_per_month', +e.target.value)} className="w-full accent-purple-500" />
            </div>
            <div>
              <label htmlFor="electronics" className="block text-sm font-medium mb-2">Electronics/year: {formData.shopping.electronics_per_year}</label>
              <input id="electronics" type="range" min="0" max="20" value={formData.shopping.electronics_per_year} onChange={(e) => updateField('shopping', 'electronics_per_year', +e.target.value)} className="w-full accent-purple-500" />
            </div>
            <div>
              <label htmlFor="online-deliveries" className="block text-sm font-medium mb-2">Online deliveries/month: {formData.shopping.online_deliveries_per_month}</label>
              <input id="online-deliveries" type="range" min="0" max="30" value={formData.shopping.online_deliveries_per_month} onChange={(e) => updateField('shopping', 'online_deliveries_per_month', +e.target.value)} className="w-full accent-purple-500" />
            </div>
            <div>
              <label htmlFor="second-hand-pct" className="block text-sm font-medium mb-2">Second-hand %: {formData.shopping.second_hand_pct}%</label>
              <input id="second-hand-pct" type="range" min="0" max="100" value={formData.shopping.second_hand_pct} onChange={(e) => updateField('shopping', 'second_hand_pct', +e.target.value)} className="w-full accent-brand-500" />
            </div>
          </>
        )}
        {step === 4 && (
          <>
            <div>
              <label htmlFor="recycling-frequency" className="block text-sm font-medium mb-2">Recycling Frequency</label>
              <select id="recycling-frequency" value={formData.waste.recycling_frequency} onChange={(e) => updateField('waste', 'recycling_frequency', e.target.value)} className="input-field">
                <option value="never">Never</option>
                <option value="sometimes">Sometimes</option>
                <option value="often">Often</option>
                <option value="always">Always</option>
              </select>
            </div>
            <div>
              <label htmlFor="plastic-usage" className="block text-sm font-medium mb-2">Plastic Usage</label>
              <select id="plastic-usage" value={formData.waste.plastic_usage} onChange={(e) => updateField('waste', 'plastic_usage', e.target.value)} className="input-field">
                <option value="low">Low</option>
                <option value="moderate">Moderate</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="flex items-center gap-3">
              <input id="composting" type="checkbox" checked={formData.waste.composting} onChange={(e) => updateField('waste', 'composting', e.target.checked)} className="accent-brand-500 w-4 h-4" />
              <label htmlFor="composting" className="text-sm">I compost food waste</label>
            </div>
            <div className="flex items-center gap-3">
              <input id="reusable-bottle" type="checkbox" checked={formData.waste.reusable_water_bottle} onChange={(e) => updateField('waste', 'reusable_water_bottle', e.target.checked)} className="accent-brand-500 w-4 h-4" />
              <label htmlFor="reusable-bottle" className="text-sm">I use a reusable water bottle</label>
            </div>
          </>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between mt-6">
        <button onClick={() => setStep(Math.max(0, step - 1))} disabled={step === 0} className="btn-ghost disabled:opacity-30">
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
        {step < STEPS.length - 1 ? (
          <button onClick={() => setStep(step + 1)} className="btn-primary">
            Next <ArrowRight className="w-4 h-4" />
          </button>
        ) : (
          <button onClick={handleSubmit} disabled={isCalculating} className="btn-primary disabled:opacity-50">
            {isCalculating ? 'Calculating...' : 'Calculate Footprint'} <Leaf className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}
