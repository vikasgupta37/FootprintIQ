'use client';

import { useEffect, useState } from 'react';
import { ArrowDown, ArrowUp, BarChart3, TrendingDown, TrendingUp, Target } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface BreakdownCategory {
  category: string;
  current_kg: number;
  previous_kg: number;
  change_pct: number;
  percentage_of_total: number;
  trend: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  transportation: 'bg-blue-500',
  energy: 'bg-amber-500',
  food: 'bg-green-500',
  shopping: 'bg-purple-500',
  waste: 'bg-red-500',
};

export default function AnalyticsPage() {
  const [breakdown, setBreakdown] = useState<BreakdownCategory[]>([]);
  const [predictions, setPredictions] = useState<any>(null);
  const [totalCurrent, setTotalCurrent] = useState(0);
  const [totalPrevious, setTotalPrevious] = useState(0);

  useEffect(() => {
    apiClient.get('/analytics/breakdown?period=month')
      .then(({ data }) => {
        setBreakdown(data.categories);
        setTotalCurrent(data.total_current);
        setTotalPrevious(data.total_previous);
      })
      .catch(console.error);

    apiClient.get('/analytics/predictions?timeframe=90d')
      .then(({ data }) => setPredictions(data))
      .catch(console.error);
  }, []);

  const totalChange = totalPrevious > 0 ? ((totalCurrent - totalPrevious) / totalPrevious * 100).toFixed(1) : '0';

  return (
    <div className="animate-fade-in space-y-8">
      <div>
        <h1 className="text-3xl font-display font-bold">Analytics</h1>
        <p className="text-slate-400 mt-1">Detailed breakdown and future predictions.</p>
      </div>

      {/* Overview */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="card p-6">
          <div className="text-sm text-slate-400 mb-1">Current Month</div>
          <div className="text-3xl font-display font-bold">{totalCurrent.toFixed(0)}<span className="text-lg text-slate-500 ml-1">kg</span></div>
        </div>
        <div className="card p-6">
          <div className="text-sm text-slate-400 mb-1">Previous Month</div>
          <div className="text-3xl font-display font-bold text-slate-400">{totalPrevious.toFixed(0)}<span className="text-lg text-slate-500 ml-1">kg</span></div>
        </div>
        <div className="card p-6">
          <div className="text-sm text-slate-400 mb-1">Change</div>
          <div className={`text-3xl font-display font-bold flex items-center gap-2 ${Number(totalChange) < 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {Number(totalChange) < 0 ? <ArrowDown className="w-6 h-6" /> : <ArrowUp className="w-6 h-6" />}
            {Math.abs(Number(totalChange))}%
          </div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="card p-6">
        <h2 className="font-display font-semibold text-lg mb-6">Category Breakdown</h2>
        <div className="space-y-4">
          {breakdown.map((cat) => (
            <div key={cat.category} className="flex items-center gap-4">
              <div className={`w-3 h-3 rounded-full ${CATEGORY_COLORS[cat.category] || 'bg-slate-500'}`} />
              <div className="w-28 text-sm capitalize">{cat.category}</div>
              <div className="flex-1">
                <div className="h-4 bg-slate-700/50 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${CATEGORY_COLORS[cat.category] || 'bg-slate-500'} rounded-full transition-all duration-700`}
                    style={{ width: `${cat.percentage_of_total}%` }}
                  />
                </div>
              </div>
              <div className="w-20 text-right text-sm font-medium">{cat.current_kg.toFixed(1)} kg</div>
              <div className={`w-16 text-right text-xs flex items-center justify-end gap-1 ${cat.change_pct < 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {cat.change_pct < 0 ? <TrendingDown className="w-3 h-3" /> : <TrendingUp className="w-3 h-3" />}
                {Math.abs(cat.change_pct)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Predictions */}
      {predictions && (
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">
            <BarChart3 className="w-5 h-5 inline mr-2 text-brand-400" />
            6-Month Emissions Forecast
          </h2>
          
          <div className="h-72 w-full mb-6 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={predictions.predictions.map((p: any, i: number) => ({
                month: `Month ${p.month}`,
                predicted: p.predicted_kg,
                target: predictions.target_curve?.[i]?.target_kg || p.predicted_kg
              }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} unit="kg" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Line type="monotone" name="Predicted Trend" dataKey="predicted" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line type="monotone" name="2°C Target Baseline" dataKey="target" stroke="#10b981" strokeDasharray="5 5" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
          <div className="flex items-center justify-between text-sm bg-slate-800/50 p-4 rounded-xl">
            <span className="text-slate-300">
              Projected 6-month reduction: <span className="text-brand-400 font-bold ml-1">{predictions.projected_reduction_pct}%</span>
            </span>
            <span className="text-slate-400">
              AI Confidence: <span className="font-bold text-slate-300">{(predictions.confidence_score * 100).toFixed(0)}%</span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
