'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!email) return;
    login(email);
    router.push('/');
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-slate-900 rounded-3xl border border-slate-700 p-10 shadow-2xl shadow-slate-950/50">
        <h1 className="text-3xl font-bold mb-6">Connexion Trendscout</h1>
        <p className="text-sm text-slate-400 mb-8">Entrez votre email pour accéder au tableau de bord.</p>
        <form onSubmit={handleSubmit} className="space-y-6">
          <label className="block">
            <span className="text-slate-300">Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="votre@email.com"
              required
            />
          </label>

          <button
            type="submit"
            className="w-full rounded-2xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-500 transition"
          >
            Se connecter
          </button>
        </form>
      </div>
    </main>
  );
}
