'use client';

import { useEffect, useState } from 'react';
import { Crown, Medal, Trophy } from 'lucide-react';
import apiClient from '@/lib/api-client';
import { useAuthStore } from '@/stores';
import type { LeaderboardEntry } from '@/types';

const RANK_STYLES = [
  { icon: Crown, color: 'text-amber-400', bg: 'bg-amber-500/10', ring: 'ring-amber-500/30' },
  { icon: Medal, color: 'text-slate-300', bg: 'bg-slate-500/10', ring: 'ring-slate-400/30' },
  { icon: Medal, color: 'text-orange-400', bg: 'bg-orange-500/10', ring: 'ring-orange-500/30' },
];

export default function LeaderboardPage() {
  const { user } = useAuthStore();
  const [rankings, setRankings] = useState<LeaderboardEntry[]>([]);
  const [period, setPeriod] = useState('weekly');
  const [metric, setMetric] = useState('points');
  const [total, setTotal] = useState(0);
  const [activeTab, setActiveTab] = useState<'leaderboard' | 'badges' | 'challenges'>('leaderboard');

  useEffect(() => {
    apiClient.get(`/gamification/leaderboard?period=${period}&metric=${metric}`)
      .then(({ data }) => {
        setRankings(data.rankings);
        setTotal(data.total_participants);
      })
      .catch(console.error);
  }, [period, metric]);

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-bold">Community Gamification</h1>
          <p className="text-slate-400 mt-1">Compete, collect badges, and complete challenges</p>
        </div>
        
        <div className="flex bg-slate-800/50 p-1 rounded-xl">
          <button 
            onClick={() => setActiveTab('leaderboard')}
            className={`px-4 py-2 rounded-lg text-sm font-bold transition ${activeTab === 'leaderboard' ? 'bg-brand-500 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
          >Leaderboard</button>
          <button 
            onClick={() => setActiveTab('badges')}
            className={`px-4 py-2 rounded-lg text-sm font-bold transition ${activeTab === 'badges' ? 'bg-brand-500 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
          >Badges</button>
          <button 
            onClick={() => setActiveTab('challenges')}
            className={`px-4 py-2 rounded-lg text-sm font-bold transition ${activeTab === 'challenges' ? 'bg-brand-500 text-white shadow-lg' : 'text-slate-400 hover:text-white'}`}
          >Challenges</button>
        </div>
      </div>

      {activeTab === 'leaderboard' && (
        <div className="animate-fade-in">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Top Eco-Warriors ({total} total)</h2>
            <div className="flex gap-2">
          {['weekly', 'monthly', 'all_time'].map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${period === p ? 'bg-brand-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}
            >
              {p === 'all_time' ? 'All Time' : p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Top 3 Podium */}
      {rankings.length >= 3 && (
        <div className="flex items-end justify-center gap-4 mb-10">
          {[1, 0, 2].map((idx) => {
            const entry = rankings[idx];
            const style = RANK_STYLES[idx];
            const height = idx === 0 ? 'h-32' : idx === 1 ? 'h-24' : 'h-20';
            return (
              <div key={entry.rank} className="text-center">
                <div className={`w-14 h-14 rounded-full ${style.bg} ring-2 ${style.ring} flex items-center justify-center mx-auto mb-2`}>
                  <span className="text-lg font-bold">{entry.user.username?.charAt(0)?.toUpperCase() || '?'}</span>
                </div>
                <div className="text-sm font-semibold mb-1 truncate w-24">{entry.user.username}</div>
                <div className={`text-xs ${style.color} mb-2`}>
                  <style.icon className="w-4 h-4 inline mr-1" />
                  #{entry.rank}
                </div>
                <div className={`${height} w-24 rounded-t-xl bg-gradient-to-t from-brand-600/20 to-brand-500/10 flex items-center justify-center`}>
                  <span className="text-sm font-bold">{entry.score.toLocaleString()}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Full Rankings */}
      <div className="card overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700/50 text-xs text-slate-500 uppercase">
              <th className="text-left px-6 py-3">Rank</th>
              <th className="text-left px-6 py-3">User</th>
              <th className="text-right px-6 py-3">Score</th>
              <th className="text-right px-6 py-3">Level</th>
            </tr>
          </thead>
          <tbody>
            {rankings.map((entry) => {
              const isCurrentUser = entry.user.id === user?.id;
              return (
                <tr
                  key={entry.rank}
                  className={`border-b border-slate-700/30 hover:bg-slate-800/50 transition ${isCurrentUser ? 'bg-brand-500/5' : ''}`}
                >
                  <td className="px-6 py-3">
                    <span className={`font-bold ${entry.rank <= 3 ? RANK_STYLES[entry.rank - 1]?.color : 'text-slate-400'}`}>
                      #{entry.rank}
                    </span>
                  </td>
                  <td className="px-6 py-3">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold">
                        {entry.user.username?.charAt(0)?.toUpperCase() || '?'}
                      </div>
                      <span className={`font-medium ${isCurrentUser ? 'text-brand-400' : ''}`}>
                        {entry.user.username}
                        {isCurrentUser && <span className="text-xs ml-1 text-slate-500">(You)</span>}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-3 text-right font-semibold">{entry.score.toLocaleString()}</td>
                  <td className="px-6 py-3 text-right text-sm text-slate-400">Lv.{entry.user.level}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
        </div>
      )}

      {activeTab === 'badges' && (
        <div className="animate-fade-in">
          <h2 className="text-xl font-bold mb-6">Green Achievement Badges</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {['First Step', 'Public Transit Hero', 'Plant Based Week', 'Eco Twin Master'].map((badge, i) => (
              <div key={i} className="card p-6 text-center hover:border-brand-500/50 transition cursor-pointer group">
                <div className="w-20 h-20 mx-auto bg-slate-800 rounded-full border-4 border-slate-700 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:border-brand-500 transition-all duration-300">
                  <Medal className="w-8 h-8 text-brand-400" />
                </div>
                <h3 className="font-bold mb-1">{badge}</h3>
                <p className="text-xs text-slate-400">Unlock by completing specific sustainability goals.</p>
              </div>
            ))}
            <div className="card p-6 text-center border-dashed border-slate-700 bg-slate-800/20 opacity-50">
              <div className="w-20 h-20 mx-auto bg-slate-900 rounded-full border-4 border-slate-800 flex items-center justify-center mb-4">
                <span className="text-slate-600 font-bold">?</span>
              </div>
              <h3 className="font-bold mb-1">Locked</h3>
            </div>
            <div className="card p-6 text-center border-dashed border-slate-700 bg-slate-800/20 opacity-50">
              <div className="w-20 h-20 mx-auto bg-slate-900 rounded-full border-4 border-slate-800 flex items-center justify-center mb-4">
                <span className="text-slate-600 font-bold">?</span>
              </div>
              <h3 className="font-bold mb-1">Locked</h3>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'challenges' && (
        <div className="animate-fade-in">
          <h2 className="text-xl font-bold mb-6">Active Community Challenges</h2>
          <div className="space-y-4">
            {[
              { title: "Meatless Week Challenge", points: 300, joined: 1245, desc: "Go completely meat-free for 7 days." },
              { title: "Energy Vampire Hunt", points: 150, joined: 843, desc: "Unplug all unused electronics for a week." },
              { title: "Transit Commuter", points: 200, joined: 2150, desc: "Take public transit 3 times this week." }
            ].map((challenge, i) => (
              <div key={i} className="card p-6 flex items-center justify-between group hover:border-brand-500/30 transition">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-bold text-lg">{challenge.title}</h3>
                    <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-400">
                      +{challenge.points} pts
                    </span>
                  </div>
                  <p className="text-slate-400 text-sm mb-3">{challenge.desc}</p>
                  <div className="text-xs text-slate-500 font-medium">
                    {challenge.joined.toLocaleString()} eco-warriors participating
                  </div>
                </div>
                <button className="btn-primary opacity-0 group-hover:opacity-100 transition translate-x-4 group-hover:translate-x-0">
                  Join Challenge
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
