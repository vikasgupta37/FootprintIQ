/**
 * Zustand stores for global state management.
 */

import { create } from 'zustand';
import apiClient from '@/lib/api-client';
import type { User, CarbonScore, ChatMessage, Conversation, DashboardData } from '@/types';

// ── Auth Store ──────────────────────────────────────────────

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  googleLogin: (code: string) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email, password) => {
    const { data } = await apiClient.post('/auth/login', { email, password });
    localStorage.setItem('access_token', data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    set({ user: data.user, isAuthenticated: true });
  },

  register: async (email, password, fullName) => {
    const { data } = await apiClient.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    localStorage.setItem('access_token', data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    set({ user: data.user, isAuthenticated: true });
  },

  googleLogin: async (code) => {
    const { data } = await apiClient.post('/auth/oauth/google', { code });
    localStorage.setItem('access_token', data.tokens.access_token);
    localStorage.setItem('refresh_token', data.tokens.refresh_token);
    set({ user: data.user, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false });
  },

  loadUser: async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        set({ isLoading: false });
        return;
      }
      const { data } = await apiClient.get('/users/me');
      set({ user: data, isAuthenticated: true, isLoading: false });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));

// ── Carbon Store ────────────────────────────────────────────

interface CarbonState {
  currentScore: CarbonScore | null;
  history: CarbonScore[];
  isCalculating: boolean;
  calculate: (data: Record<string, unknown>) => Promise<CarbonScore>;
  fetchHistory: () => Promise<void>;
}

export const useCarbonStore = create<CarbonState>((set) => ({
  currentScore: null,
  history: [],
  isCalculating: false,

  calculate: async (data) => {
    set({ isCalculating: true });
    try {
      const { data: result } = await apiClient.post('/carbon/calculate', data);
      set({ currentScore: result, isCalculating: false });
      return result;
    } catch (err) {
      set({ isCalculating: false });
      throw err;
    }
  },

  fetchHistory: async () => {
    const { data } = await apiClient.get('/carbon/footprints');
    set({ history: data });
  },
}));

// ── Chat Store ──────────────────────────────────────────────

interface ChatState {
  conversations: Conversation[];
  activeConversationId: string | null;
  messages: ChatMessage[];
  isTyping: boolean;
  sendMessage: (message: string) => Promise<void>;
  loadConversations: () => Promise<void>;
  loadMessages: (conversationId: string) => Promise<void>;
  setActiveConversation: (id: string | null) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  conversations: [],
  activeConversationId: null,
  messages: [],
  isTyping: false,

  sendMessage: async (message) => {
    const { activeConversationId, messages } = get();

    // Optimistic UI
    const userMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    };
    set({ messages: [...messages, userMsg], isTyping: true });

    try {
      const { data } = await apiClient.post('/ai/chat', {
        message,
        conversation_id: activeConversationId,
      });

      const aiMsg: ChatMessage = {
        id: data.message_id,
        role: 'assistant',
        content: data.content,
        intent: data.intent,
        created_at: data.created_at,
      };

      set((state) => ({
        messages: [...state.messages, aiMsg],
        isTyping: false,
        activeConversationId: data.conversation_id,
      }));
    } catch {
      set({ isTyping: false });
    }
  },

  loadConversations: async () => {
    const { data } = await apiClient.get('/ai/conversations');
    set({ conversations: data });
  },

  loadMessages: async (conversationId) => {
    const { data } = await apiClient.get(`/ai/conversations/${conversationId}/messages`);
    set({ messages: data, activeConversationId: conversationId });
  },

  setActiveConversation: (id) => set({ activeConversationId: id, messages: [] }),
}));

// ── UI Store ────────────────────────────────────────────────

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  toggleTheme: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  theme: 'dark',
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  toggleTheme: () => set((s) => ({ theme: s.theme === 'light' ? 'dark' : 'light' })),
}));
