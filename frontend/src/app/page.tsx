'use client';

import Link from 'next/link';
import { ArrowRight, BarChart3, Bot, Leaf, Shield, Sparkles, TreePine, Zap } from 'lucide-react';

const features = [
  {
    icon: <BarChart3 className="w-6 h-6" />,
    title: 'Smart Calculator',
    desc: 'Calculate your carbon footprint across 5 categories with IPCC-validated emission factors.',
  },
  {
    icon: <Bot className="w-6 h-6" />,
    title: 'AI Advisor',
    desc: 'Get personalized sustainability advice from our Claude-powered AI assistant.',
  },
  {
    icon: <Sparkles className="w-6 h-6" />,
    title: 'Eco Twin™',
    desc: 'Simulate lifestyle changes and see their impact before you commit.',
  },
  {
    icon: <Zap className="w-6 h-6" />,
    title: 'Gamification',
    desc: 'Earn points, unlock badges, and compete on leaderboards to stay motivated.',
  },
  {
    icon: <TreePine className="w-6 h-6" />,
    title: 'Impact Tracking',
    desc: 'Visualize your progress with beautiful charts and real-time analytics.',
  },
  {
    icon: <Shield className="w-6 h-6" />,
    title: 'Privacy First',
    desc: 'Your data is encrypted and protected. GDPR compliant by design.',
  },
];

const stats = [
  { value: '200K+', label: 'Users Worldwide' },
  { value: '10K', label: 'Tons CO₂ Saved' },
  { value: '4.8★', label: 'User Rating' },
  { value: '50+', label: 'AI Models' },
];

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

      {/* Hero */}
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

      {/* Stats */}
      <section id="stats" className="py-16 px-6 border-y border-white/5">
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl md:text-4xl font-display font-bold text-brand-400">{stat.value}</div>
              <div className="text-sm text-slate-500 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-display font-bold mb-4">
              Everything You Need to Go Green
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              A complete sustainability toolkit powered by cutting-edge AI.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feat) => (
              <div
                key={feat.title}
                className="card p-6 group hover:border-brand-500/30 dark:hover:border-brand-500/30 transition-all duration-300"
              >
                <div className="w-12 h-12 rounded-xl bg-brand-500/10 flex items-center justify-center text-brand-400 mb-4 group-hover:bg-brand-500/20 transition">
                  {feat.icon}
                </div>
                <h3 className="text-lg font-semibold mb-2">{feat.title}</h3>
                <p className="text-sm text-slate-400">{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how" className="py-24 px-6 bg-surface-800/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold mb-16">
            Three Steps to a Smaller Footprint
          </h2>
          <div className="grid md:grid-cols-3 gap-12">
            {[
              { step: '01', title: 'Calculate', desc: 'Answer simple questions about your lifestyle across 5 categories.' },
              { step: '02', title: 'Discover', desc: 'Get AI-powered insights and personalized recommendations.' },
              { step: '03', title: 'Improve', desc: 'Track your progress, earn rewards, and make a real difference.' },
            ].map((item) => (
              <div key={item.step}>
                <div className="text-5xl font-display font-bold text-brand-500/20 mb-4">{item.step}</div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-slate-400 text-sm">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold mb-6">
            Ready to Make a Difference?
          </h2>
          <p className="text-slate-400 mb-10">
            Join 200,000+ people using AI to live more sustainably. It takes less than 10 minutes.
          </p>
          <Link href="/register" className="btn-primary text-lg !py-4 !px-10">
            Start Free — Calculate Now
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

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
