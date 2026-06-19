'use client';

import { useEffect, useState } from 'react';
import { BookOpen, ChevronRight, Search, Star } from 'lucide-react';
import apiClient from '@/lib/api-client';

interface ContentItem {
  id: string;
  title: string;
  slug: string;
  description: string;
  category: string;
  difficulty: string;
  content_type: string;
  thumbnail_url?: string;
  estimated_read_time?: number;
  view_count: number;
  like_count: number;
  tags: string[];
  is_featured: boolean;
}

const CATEGORY_LABELS: Record<string, string> = {
  climate_basics: '🌍 Climate Basics',
  energy: '⚡ Energy',
  food: '🥗 Food & Agriculture',
  transportation: '🚗 Transportation',
  lifestyle: '🏠 Lifestyle',
  technology: '💡 Technology',
};

const DIFFICULTY_COLORS: Record<string, string> = {
  beginner: 'bg-green-500/10 text-green-400',
  intermediate: 'bg-amber-500/10 text-amber-400',
  advanced: 'bg-red-500/10 text-red-400',
};

export default function LearnPage() {
  const [content, setContent] = useState<ContentItem[]>([]);
  const [category, setCategory] = useState('');
  const [search, setSearch] = useState('');

  useEffect(() => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    apiClient.get(`/learning/content?${params}`)
      .then(({ data }) => setContent(data))
      .catch(console.error);
  }, [category]);

  const filtered = content.filter(
    (c) => !search || c.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-display font-bold">Learning Center</h1>
          <p className="text-slate-400 mt-1">Expand your knowledge about sustainability and climate action.</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-8 flex-wrap">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search articles..."
            className="input-field pl-11"
          />
        </div>
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setCategory('')}
            className={`px-3 py-2 rounded-lg text-sm transition ${!category ? 'bg-brand-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}
          >
            All
          </button>
          {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setCategory(key)}
              className={`px-3 py-2 rounded-lg text-sm transition ${category === key ? 'bg-brand-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Content Grid */}
      {filtered.length > 0 ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((item) => (
            <div key={item.id} className="card group overflow-hidden hover:border-brand-500/30 transition-all duration-300">
              {/* Thumbnail placeholder */}
              <div className="h-40 bg-gradient-to-br from-brand-900/50 to-surface-800 flex items-center justify-center">
                <BookOpen className="w-10 h-10 text-brand-500/30" />
              </div>

              <div className="p-5">
                <div className="flex items-center gap-2 mb-2">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${DIFFICULTY_COLORS[item.difficulty] || 'bg-slate-700 text-slate-400'}`}>
                    {item.difficulty}
                  </span>
                  <span className="text-xs text-slate-500 capitalize">{item.content_type}</span>
                  {item.is_featured && (
                    <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                  )}
                </div>

                <h3 className="font-semibold mb-2 group-hover:text-brand-400 transition">{item.title}</h3>
                <p className="text-sm text-slate-400 line-clamp-2 mb-3">{item.description}</p>

                <div className="flex items-center justify-between text-xs text-slate-500">
                  <div className="flex gap-3">
                    {item.estimated_read_time && <span>{item.estimated_read_time} min read</span>}
                    <span>{item.view_count} views</span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-brand-400 opacity-0 group-hover:opacity-100 transition" />
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 text-slate-500">
          <BookOpen className="w-10 h-10 mx-auto mb-3 opacity-50" />
          <p>No articles found. Content will appear as it&apos;s published.</p>
        </div>
      )}
    </div>
  );
}
