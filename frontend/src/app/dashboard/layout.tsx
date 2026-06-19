'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BarChart3, Bot, Calculator, FileText, Flame, Home, Leaf, LogOut,
  Medal, Settings, Sparkles, BookOpen, Trophy, User,
} from 'lucide-react';
import { useAuthStore, useUIStore } from '@/stores';

const navItems = [
  { href: '/dashboard', icon: Home, label: 'Dashboard' },
  { href: '/dashboard/calculator', icon: Calculator, label: 'Calculator' },
  { href: '/dashboard/chat', icon: Bot, label: 'AI Advisor' },
  { href: '/dashboard/eco-twin', icon: Sparkles, label: 'Eco Twin' },
  { href: '/dashboard/analytics', icon: BarChart3, label: 'Analytics' },
  { href: '/dashboard/reports', icon: FileText, label: 'Reports' },
  { href: '/dashboard/leaderboard', icon: Trophy, label: 'Leaderboard' },
  { href: '/dashboard/learn', icon: BookOpen, label: 'Learn' },
  { href: '/dashboard/profile', icon: User, label: 'Profile' },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, loadUser, logout, isLoading } = useAuthStore();
  const { sidebarOpen } = useUIStore();

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-surface-900 flex items-center justify-center">
        <Leaf className="w-10 h-10 text-brand-400 animate-pulse" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-900 flex">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} flex-shrink-0 border-r border-white/5 bg-surface-800/50 flex flex-col transition-all duration-300`}>
        {/* Logo */}
        <div className="p-6 flex items-center gap-3">
          <Leaf className="w-8 h-8 text-brand-400 flex-shrink-0" />
          {sidebarOpen && <span className="text-lg font-display font-bold">FootprintIQ</span>}
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`sidebar-link ${isActive ? 'sidebar-link-active' : ''}`}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span>{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* User Footer */}
        {user && sidebarOpen && (
          <div className="p-4 border-t border-white/5">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-9 h-9 rounded-full bg-brand-500/20 flex items-center justify-center text-brand-400 text-sm font-bold">
                {user.full_name?.charAt(0)?.toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium truncate">{user.full_name}</div>
                <div className="text-xs text-slate-500">Level {user.level} • {user.total_points} pts</div>
              </div>
            </div>
            <button onClick={logout} className="sidebar-link w-full text-red-400 hover:text-red-300 hover:bg-red-500/10">
              <LogOut className="w-4 h-4" />
              <span className="text-sm">Sign Out</span>
            </button>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
