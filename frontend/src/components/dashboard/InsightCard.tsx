import React from 'react';
import { ArrowDown, TrendingDown, Info } from 'lucide-react';

interface VisualizationData {
  chart_type: 'bar' | 'doughnut' | 'progress';
  metric_label: string;
  before_value: number;
  after_value: number;
  unit: string;
}

interface InsightCardProps {
  title: string;
  description: string;
  visualization?: VisualizationData;
  impact_level?: string;
  co2_saved?: number;
}

export function InsightCard({ title, description, visualization, impact_level, co2_saved }: InsightCardProps) {
  return (
    <div className="card p-6 border-l-4 border-l-brand-500 bg-gradient-to-br from-slate-900 to-slate-800 relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition">
        <Info className="w-24 h-24" />
      </div>
      
      <div className="flex justify-between items-start mb-4 relative z-10">
        <div>
          <h3 className="text-xl font-bold text-white">{title}</h3>
          <p className="text-slate-400 mt-1">{description}</p>
        </div>
        {impact_level && (
          <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-brand-500/20 text-brand-400 border border-brand-500/30">
            {impact_level} Impact
          </span>
        )}
      </div>

      {visualization && (
        <div className="mt-6 bg-slate-950/50 rounded-xl p-5 border border-slate-700/50 relative z-10">
          <div className="flex justify-between items-end mb-4">
            <span className="text-sm font-medium text-slate-300">{visualization.metric_label}</span>
            {co2_saved && (
              <span className="text-emerald-400 font-bold flex items-center text-sm">
                <TrendingDown className="w-4 h-4 mr-1" />
                -{co2_saved} {visualization.unit}
              </span>
            )}
          </div>
          
          {visualization.chart_type === 'bar' && (
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Current</span>
                  <span className="font-bold">{visualization.before_value} {visualization.unit}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-3">
                  <div className="bg-slate-500 h-3 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-brand-400 font-bold">Projected</span>
                  <span className="text-brand-400 font-bold">{visualization.after_value} {visualization.unit}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-3">
                  <div 
                    className="bg-brand-500 h-3 rounded-full shadow-[0_0_10px_rgba(34,197,94,0.5)]" 
                    style={{ width: `${Math.max(10, (visualization.after_value / visualization.before_value) * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}

          {visualization.chart_type === 'progress' && (
            <div className="flex items-center gap-4">
               <div className="w-full bg-slate-800 rounded-full h-6 overflow-hidden relative">
                  <div 
                    className="bg-brand-500 h-full absolute left-0 top-0 transition-all duration-1000 flex items-center justify-end px-2" 
                    style={{ width: `${Math.max(10, (visualization.after_value / visualization.before_value) * 100)}%` }}
                  >
                    <span className="text-[10px] font-bold text-white drop-shadow-md">New Goal</span>
                  </div>
                </div>
                <div className="shrink-0 text-right">
                  <div className="text-xs text-slate-400">Reduction</div>
                  <div className="text-lg font-bold text-emerald-400">
                    -{Math.round(((visualization.before_value - visualization.after_value) / visualization.before_value) * 100)}%
                  </div>
                </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
