import React from 'react';
import Link from 'next/link';
import { ArrowRight, Sparkles } from 'lucide-react';

/**
 * Hero section for the landing page.
 */
export function Hero() {
  return (
    <section id="main-content" className="relative pt-32 pb-20 px-6">
      <div className="absolute inset-0 bg-hero-glow" />
      <div className="absolute top-20 left-1/4 w-72 h-72 bg-brand-500/10 rounded-full blur-3xl animate-pulse-soft" />
      <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl animate-float" />

      <div className="max-w-4xl mx-auto text-center relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-500/30 bg-brand-500/10 text-brand-400 text-sm font-medium mb-8 animate-fade-in">
          <Sparkles className="w-4 h-4" />
          Powered by Claude AI
        </div>

        <h1 className="text-5xl md:text-7xl font-display font-bold leading-tight mb-6 animate-slide-up">
          Smarter Choices.
          <br />
          <span className="bg-gradient-to-r from-brand-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent animate-gradient-x">
            Smaller Footprints.
          </span>
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 animate-slide-up" style={{ animationDelay: '0.1s' }}>
          Track your carbon footprint, get AI-powered recommendations, and simulate
          lifestyle changes — all in one beautiful platform.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <Link href="/register" className="btn-primary text-lg !py-4 !px-8">
            Calculate Your Footprint
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link href="#features" className="btn-secondary text-lg !py-4 !px-8">
            Learn More
          </Link>
        </div>
      </div>
    </section>
  );
}
