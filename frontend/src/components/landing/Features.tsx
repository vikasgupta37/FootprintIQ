import React from 'react';
import { BarChart3, Bot, Leaf, Shield, Sparkles, TreePine, Zap } from 'lucide-react';

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

/**
 * Features section for the landing page.
 */
export function Features() {
  return (
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
  );
}
