'use client';

import { useAuth } from '../contexts/AuthContext';
import Logo from './Logo';
import Link from 'next/link';

export default function Navbar() {
  const { email, logout } = useAuth();

  return (
    <header className="bg-slate-900 border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition">
          <Logo />
          <div>
            <h1 className="text-2xl font-bold text-white">Trendscout</h1>
            <p className="text-xs text-gray-400">Fashion AI</p>
          </div>
        </Link>

        <nav className="flex items-center gap-6">
          <Link 
            href="/" 
            className="text-gray-300 hover:text-white transition"
          >
            Analyze
          </Link>
          <Link 
            href="/dashboard" 
            className="text-gray-300 hover:text-white transition"
          >
            Dashboard
          </Link>
          <div className="flex items-center gap-4">
            <p className="text-sm text-gray-400">{email}</p>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-sm font-semibold text-white transition"
            >
              Logout
            </button>
          </div>
        </nav>
      </div>
    </header>
  );
}