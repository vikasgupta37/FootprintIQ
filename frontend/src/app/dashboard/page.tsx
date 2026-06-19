'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { ArrowDown, ArrowUp, BarChart3, Bot, Calculator, Flame, Leaf, Sparkles, Target, TrendingDown, Trophy } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { useAuthStore } from '@/stores';
import type { DashboardData } from '@/types';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get('/analytics/dashboard?period=month')
      .then(({ data }) => setData(data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const quickActions = [
    { href: '/dashboard/calculator', icon: Calculator, label: 'Calculate', desc: 'New footprint', color: 'from-brand-500 to-emerald-500' },
    { href: '/dashboard/chat', icon: Bot, label: 'AI Advisor', desc: 'Get advice', color: 'from-blue-500 to-indigo-500' },
    { href: '/dashboard/eco-twin', icon: Sparkles, label: 'Eco Twin', desc: 'Simulate', color: 'from-purple-500 to-pink-500' },
    { href: '/dashboard/leaderboard', icon: Trophy, label: 'Leaderboard', desc: 'Compete', color: 'from-amber-500 to-orange-500' },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-display font-bold">
          Welcome back, {user?.full_name?.split(' ')[0] || 'Eco Warrior'} 🌱
        </h1>
        <p className="text-slate-400 mt-1">Here&apos;s your sustainability overview for this month.</p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {quickActions.map((action) => (
          <Link
            key={action.href}
            href={action.href}
            className="card p-5 group hover:scale-[1.02] transition-all duration-300"
          >
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center mb-3 group-hover:shadow-lg transition`}>
              <action.icon className="w-5 h-5 text-white" />
            </div>
            <div className="font-semibold text-sm">{action.label}</div>
            <div className="text-xs text-slate-500">{action.desc}</div>
          </Link>
        ))}
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Carbon Score */}
        <div className="card p-6 md:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-lg">Carbon Footprint</h2>
            <span className="text-xs text-slate-500">This month</span>
          </div>
          {data?.carbon_metrics ? (
            <div className="flex items-end gap-8">
              <div>
                <div className="text-4xl font-display font-bold">
                  {data.carbon_metrics.current_footprint.toFixed(0)}
                  <span className="text-lg text-slate-500 ml-1">kg CO₂e</span>
                </div>
                <div className={`flex items-center gap-1 mt-2 text-sm ${data.carbon_metrics.change_pct < 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                  {data.carbon_metrics.change_pct < 0 ? <ArrowDown className="w-4 h-4" /> : <ArrowUp className="w-4 h-4" />}
                  {Math.abs(data.carbon_metrics.change_pct).toFixed(1)}% vs last month
                </div>
              </div>
              <div className="flex-1 flex justify-end">
                <div className="w-28 h-28 rounded-full border-4 border-brand-500 flex items-center justify-center">
                  <div className="text-center">
                    <Leaf className="w-6 h-6 text-brand-400 mx-auto" />
                    <div className="text-xs text-slate-400 mt-1">{data.carbon_metrics.trend}</div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-slate-500">
              <Calculator className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No calculations yet.</p>
              <Link href="/dashboard/calculator" className="btn-primary text-sm mt-3 !py-2">
                Calculate Now
              </Link>
            </div>
          )}
        </div>

        {/* Streak & Level */}
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">Your Progress</h2>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center">
                <Flame className="w-5 h-5 text-amber-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{user?.current_streak || 0}</div>
                <div className="text-xs text-slate-500">Day Streak</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center">
                <Target className="w-5 h-5 text-brand-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">Level {user?.level || 1}</div>
                <div className="text-xs text-slate-500">{user?.total_points || 0} points</div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
                <Trophy className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <div className="text-2xl font-bold">{user?.carbon_saved_kg || 0}</div>
                <div className="text-xs text-slate-500">kg CO₂ saved</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Impact Equivalents */}
      {data?.impact && (
        <div className="card p-6">
          <h2 className="font-display font-semibold text-lg mb-4">Your Environmental Impact</h2>
          <div className="grid grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-display font-bold text-brand-400">{data.impact.equivalent_trees || 0}</div>
              <div className="text-sm text-slate-400 mt-1">🌳 Trees equivalent</div>
            </div>
            <div>
              <div className="text-3xl font-display font-bold text-blue-400">{data.impact.total_co2_saved_kg || 0}</div>
              <div className="text-sm text-slate-400 mt-1">kg CO₂ saved</div>
            </div>
            <div>
              <div className="text-3xl font-display font-bold text-amber-400">{data.impact.equivalent_car_km || 0}</div>
              <div className="text-sm text-slate-400 mt-1">🚗 km offset</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
