'use client';

import { useEffect, useState } from 'react';
import { FileText, Calendar, Leaf, Trophy, ArrowRight, Download } from 'lucide-react';
import apiClient from '@/lib/api-client';

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const { data } = await apiClient.get('/analytics/reports');
      setReports(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    try {
      await apiClient.post('/analytics/reports/generate');
      fetchReports();
    } catch (e) {
      console.error(e);
      alert('Could not generate report. Need more data.');
    }
  };

  if (loading) return <div className="p-8 text-slate-400">Loading reports...</div>;

  return (
    <div className="animate-fade-in max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-bold">Sustainability Reports</h1>
          <p className="text-slate-400 mt-1">Your AI-generated weekly and monthly summaries</p>
        </div>
        <button onClick={generateReport} className="btn-primary">
          Generate Weekly Report
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="card p-12 text-center flex flex-col items-center">
          <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
            <FileText className="w-8 h-8 text-slate-500" />
          </div>
          <h3 className="text-xl font-bold mb-2">No reports yet</h3>
          <p className="text-slate-400 mb-6">Complete a week of tracking to receive your first AI insights.</p>
          <button onClick={generateReport} className="btn-outline">Try Generating Now</button>
        </div>
      ) : (
        <div className="space-y-6">
          {reports.map((report) => (
            <div key={report.id} className="card p-0 overflow-hidden border border-slate-700/50">
              <div className="bg-slate-800/50 border-b border-slate-700/50 p-6 flex justify-between items-center">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-brand-500/20 text-brand-400 flex items-center justify-center border border-brand-500/30">
                    <Calendar className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg capitalize">{report.report_type} Report</h3>
                    <p className="text-slate-400 text-sm">
                      {new Date(report.period_start).toLocaleDateString()} - {new Date(report.period_end).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-xs text-slate-400 uppercase tracking-wider font-bold">AI Score</div>
                    <div className="text-2xl font-bold text-brand-400">{report.ai_sustainability_score || '--'}</div>
                  </div>
                  <button className="p-2 hover:bg-slate-700 rounded-lg text-slate-400 transition">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
              
              <div className="p-6">
                <p className="text-slate-300 leading-relaxed mb-6 whitespace-pre-wrap">
                  {report.summary_text}
                </p>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-slate-800/30 rounded-xl p-4 border border-slate-700/30">
                    <div className="flex items-center text-slate-400 text-sm font-semibold mb-2">
                      <Leaf className="w-4 h-4 mr-2 text-emerald-400" />
                      Carbon Saved
                    </div>
                    <div className="text-2xl font-bold">{report.carbon_saved_kg} kg</div>
                  </div>
                  <div className="bg-slate-800/30 rounded-xl p-4 border border-slate-700/30">
                    <div className="flex items-center text-slate-400 text-sm font-semibold mb-2">
                      <Trophy className="w-4 h-4 mr-2 text-amber-400" />
                      Challenges Completed
                    </div>
                    <div className="text-2xl font-bold">{report.challenges_completed}</div>
                  </div>
                </div>

                {report.key_insights && report.key_insights.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-slate-300 mb-3">Key Insights</h4>
                    <div className="space-y-3">
                      {report.key_insights.map((insight: any, i: number) => (
                        <div key={i} className="flex items-start gap-3 p-3 bg-slate-800/20 rounded-lg border border-slate-700/30">
                          <ArrowRight className="w-5 h-5 text-brand-500 mt-0.5 shrink-0" />
                          <div>
                            <p className="text-sm text-slate-200">{insight.text}</p>
                            {insight.metric && (
                              <span className="inline-block mt-1 text-xs font-bold text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded">
                                {insight.metric}
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
