'use client';

import Link from 'next/link';
import { Leaf } from 'lucide-react';
import { Hero } from '@/components/landing/Hero';
import { Stats } from '@/components/landing/Stats';
import { Features } from '@/components/landing/Features';
import { HowItWorks } from '@/components/landing/HowItWorks';
import { CTA } from '@/components/landing/CTA';

/**
 * Main landing page component composed of modular sections.
 */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-surface-900 text-white overflow-hidden">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-brand-500 text-white px-4 py-2 rounded-xl z-50 text-sm font-semibold"
      >
        Skip to content
      </a>

      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Leaf className="w-8 h-8 text-brand-400" />
            <span className="text-xl font-display font-bold">FootprintIQ</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-slate-400">
            <a href="#features" className="hover:text-white transition">Features</a>
            <a href="#how" className="hover:text-white transition">How It Works</a>
            <a href="#stats" className="hover:text-white transition">Impact</a>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/login" className="btn-ghost text-sm">Log In</Link>
            <Link href="/register" className="btn-primary text-sm !py-2 !px-5">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Composed Sections */}
      <Hero />
      <Stats />
      <Features />
      <HowItWorks />
      <CTA />

      {/* Footer */}
      <footer className="border-t border-white/5 py-12 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <Leaf className="w-5 h-5 text-brand-400" />
            <span className="font-display font-semibold">FootprintIQ</span>
          </div>
          <p className="text-sm text-slate-500">
            © 2026 FootprintIQ. Smarter Choices. Smaller Footprints. 🌱
          </p>
        </div>
      </footer>
    </div>
  );
}
