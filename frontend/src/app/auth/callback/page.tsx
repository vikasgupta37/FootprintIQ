'use client';

import { Suspense, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Leaf } from 'lucide-react';
import { useAuthStore } from '@/stores';

function CallbackHandler() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { googleLogin } = useAuthStore();

  useEffect(() => {
    const code = searchParams.get('code');
    if (code) {
      googleLogin(code)
        .then(() => router.push('/dashboard'))
        .catch(() => router.push('/login?error=oauth_failed'));
    } else {
      router.push('/login?error=no_code');
    }
  }, [searchParams, googleLogin, router]);

  return (
    <div className="text-center">
      <Leaf className="w-12 h-12 text-brand-400 mx-auto animate-pulse mb-4" />
      <p className="text-slate-400">Completing sign in...</p>
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <div className="min-h-screen bg-surface-900 flex items-center justify-center">
      <Suspense fallback={
        <div className="text-center">
          <Leaf className="w-12 h-12 text-brand-400 mx-auto animate-pulse mb-4" />
          <p className="text-slate-400">Loading auth context...</p>
        </div>
      }>
        <CallbackHandler />
      </Suspense>
    </div>
  );
}
