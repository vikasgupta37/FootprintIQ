import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'FootprintIQ — AI-Powered Carbon Footprint Awareness',
  description:
    'Track, reduce, and offset your carbon footprint with AI-powered insights. Calculate your emissions, get personalized recommendations, and join a community of eco-warriors.',
  keywords: ['carbon footprint', 'sustainability', 'AI', 'climate change', 'eco-friendly'],
  openGraph: {
    title: 'FootprintIQ — Smarter Choices. Smaller Footprints.',
    description: 'AI-powered platform to track and reduce your carbon footprint.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased">{children}</body>
    </html>
  );
}
