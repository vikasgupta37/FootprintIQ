import React from 'react';

const steps = [
  { step: '01', title: 'Calculate', desc: 'Answer simple questions about your lifestyle across 5 categories.' },
  { step: '02', title: 'Discover', desc: 'Get AI-powered insights and personalized recommendations.' },
  { step: '03', title: 'Improve', desc: 'Track your progress, earn rewards, and make a real difference.' },
];

/**
 * How It Works section for the landing page.
 */
export function HowItWorks() {
  return (
    <section id="how" className="py-24 px-6 bg-surface-800/50">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl md:text-4xl font-display font-bold mb-16">
          Three Steps to a Smaller Footprint
        </h2>
        <div className="grid md:grid-cols-3 gap-12">
          {steps.map((item) => (
            <div key={item.step}>
              <div className="text-5xl font-display font-bold text-brand-500/20 mb-4">{item.step}</div>
              <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
              <p className="text-slate-400 text-sm">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
