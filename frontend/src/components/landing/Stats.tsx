import React from 'react';

const stats = [
  { value: '200K+', label: 'Users Worldwide' },
  { value: '10K', label: 'Tons CO₂ Saved' },
  { value: '4.8★', label: 'User Rating' },
  { value: '50+', label: 'AI Models' },
];

/**
 * Stats section for the landing page.
 */
export function Stats() {
  return (
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
  );
}
