'use client';

import { useEffect, useRef, useState } from 'react';
import { Bot, Leaf, Send, Sparkles, User } from 'lucide-react';
import { useChatStore, useAuthStore } from '@/stores';
import { InsightCard } from '@/components/dashboard/InsightCard';

export default function ChatPage() {
  const { user } = useAuthStore();
  const { messages, isTyping, sendMessage, conversations, loadConversations, loadMessages, setActiveConversation, activeConversationId } = useChatStore();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput('');
  };

  const suggestions = [
    '🌍 How can I reduce my carbon footprint?',
    '🚗 Should I switch to an electric vehicle?',
    '🥗 What diet is best for the planet?',
    '⚡ How do solar panels help?',
  ];

  const renderMessageContent = (content: string) => {
    const parts = content.split(/(```json[\s\S]*?```)/g);
    return parts.map((part, i) => {
      if (part.startsWith('```json')) {
        try {
          const jsonStr = part.replace(/```json\n?/, '').replace(/```$/, '');
          const data = JSON.parse(jsonStr);
          if (data.type === 'InsightCard' || data.visualization_data) {
             const visData = data.visualization_data || data.visualization;
             return (
               <div key={i} className="my-4 w-full">
                 <InsightCard 
                   title={data.title}
                   description={data.description}
                   impact_level={data.impact_level}
                   co2_saved={data.estimated_co2_savings_kg}
                   visualization={visData}
                 />
               </div>
             );
          }
        } catch (e) {
          // fallback to text
        }
      }
      return <span key={i} className="whitespace-pre-wrap">{part}</span>;
    });
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4 animate-fade-in">
      {/* Conversation Sidebar */}
      <div className="w-64 flex-shrink-0 card p-4 flex flex-col">
        <button
          onClick={() => { setActiveConversation(null); }}
          className="btn-primary w-full text-sm mb-4"
        >
          <Sparkles className="w-4 h-4" /> New Chat
        </button>

        <div className="flex-1 overflow-y-auto space-y-1">
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => loadMessages(conv.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm truncate transition ${activeConversationId === conv.id ? 'bg-brand-500/10 text-brand-400' : 'text-slate-400 hover:bg-slate-800'}`}
            >
              {conv.title || 'Untitled Conversation'}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 card flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-700/50 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-emerald-500 flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="font-semibold">AI Sustainability Advisor</div>
            <div className="text-xs text-slate-500">Powered by Claude • Always here to help</div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 rounded-2xl bg-brand-500/10 flex items-center justify-center mb-4">
                <Leaf className="w-8 h-8 text-brand-400" />
              </div>
              <h3 className="text-lg font-display font-semibold mb-2">Ask me anything about sustainability!</h3>
              <p className="text-sm text-slate-400 mb-6 max-w-sm">
                I can help you understand your carbon footprint, suggest ways to reduce it, and simulate lifestyle changes.
              </p>
              <div className="grid grid-cols-2 gap-2 w-full max-w-md">
                {suggestions.map((s) => (
                  <button
                    key={s}
                    onClick={() => { setInput(''); sendMessage(s.replace(/^.+\s/, '')); }}
                    className="text-left p-3 rounded-xl border border-slate-700 hover:border-brand-500/50 hover:bg-brand-500/5 transition text-sm text-slate-300"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-brand-500/10 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-brand-400" />
                </div>
              )}
              <div className={`max-w-[70%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-brand-500 text-white rounded-br-md'
                  : 'bg-slate-800 text-slate-200 rounded-bl-md'
              }`}>
                {msg.role === 'user' ? msg.content : renderMessageContent(msg.content)}
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-slate-700 flex items-center justify-center flex-shrink-0">
                  <User className="w-4 h-4 text-slate-300" />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-lg bg-brand-500/10 flex items-center justify-center">
                <Bot className="w-4 h-4 text-brand-400" />
              </div>
              <div className="bg-slate-800 rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 rounded-full bg-brand-400 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-6 py-4 border-t border-slate-700/50">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about sustainability, carbon footprint, or eco-friendly tips..."
              className="input-field flex-1"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              className="btn-primary !px-4 disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
