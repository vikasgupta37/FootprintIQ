import React from 'react';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

/**
 * Call to Action section for the landing page.
 */
export function CTA() {
  return (
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
  );
}
