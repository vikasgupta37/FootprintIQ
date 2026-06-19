'use client';

import { useState } from 'react';
import { Camera, Check, Save } from 'lucide-react';
import { useAuthStore } from '@/stores';
import apiClient from '@/lib/api-client';

export default function ProfilePage() {
  const { user, loadUser } = useAuthStore();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    username: user?.username || '',
    country: user?.country || '',
    city: user?.city || '',
    bio: user?.bio || '',
    household_size: user?.household_size || 1,
  });

  const handleSave = async () => {
    setSaving(true);
    try {
      await apiClient.put('/users/me', formData);
      await loadUser();
      setEditing(false);
    } catch (err) {
      console.error('Save failed', err);
    } finally {
      setSaving(false);
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto animate-fade-in space-y-6">
      <h1 className="text-3xl font-display font-bold">Your Profile</h1>

      {/* Avatar & Basic Info */}
      <div className="card p-6">
        <div className="flex items-center gap-6 mb-6">
          <div className="relative">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-500 to-emerald-500 flex items-center justify-center text-white text-2xl font-bold">
              {user.full_name?.charAt(0)?.toUpperCase()}
            </div>
            <button className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center border-2 border-surface-800 hover:bg-slate-600 transition">
              <Camera className="w-3.5 h-3.5" />
            </button>
          </div>
          <div>
            <h2 className="text-xl font-semibold">{user.full_name}</h2>
            <p className="text-sm text-slate-400">{user.email}</p>
            <div className="flex gap-3 mt-2">
              <span className="px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 text-xs font-medium">Level {user.level}</span>
              <span className="px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 text-xs font-medium">{user.total_points} pts</span>
              <span className="px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-400 text-xs font-medium capitalize">{user.role}</span>
            </div>
          </div>
        </div>

        {!editing ? (
          <button onClick={() => setEditing(true)} className="btn-secondary text-sm">
            Edit Profile
          </button>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="input-field"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Country</label>
                <input
                  type="text"
                  value={formData.country}
                  onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">City</label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="input-field"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Bio</label>
              <textarea
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                className="input-field h-24 resize-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Household Size: {formData.household_size}</label>
              <input
                type="range"
                min="1"
                max="10"
                value={formData.household_size}
                onChange={(e) => setFormData({ ...formData, household_size: +e.target.value })}
                className="w-full accent-brand-500"
              />
            </div>
            <div className="flex gap-3">
              <button onClick={handleSave} disabled={saving} className="btn-primary text-sm disabled:opacity-50">
                <Save className="w-4 h-4" />
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button onClick={() => setEditing(false)} className="btn-ghost text-sm">
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="card p-6">
        <h2 className="font-display font-semibold text-lg mb-4">Sustainability Stats</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-brand-400">{user.carbon_saved_kg}</div>
            <div className="text-xs text-slate-500">kg CO₂ saved</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-amber-400">{user.current_streak}</div>
            <div className="text-xs text-slate-500">Day streak</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-400">{user.longest_streak}</div>
            <div className="text-xs text-slate-500">Best streak</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-400">Lv.{user.level}</div>
            <div className="text-xs text-slate-500">{user.total_points} points</div>
          </div>
        </div>
      </div>

      {/* Account Info */}
      <div className="card p-6">
        <h2 className="font-display font-semibold text-lg mb-4">Account</h2>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-400">Email</span>
            <span>{user.email}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Member since</span>
            <span>{new Date(user.created_at).toLocaleDateString()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Account type</span>
            <span className="capitalize">{user.role}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
