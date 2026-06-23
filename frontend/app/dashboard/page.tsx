'use client';

import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Dashboard from '../components/Dashboard';
import Navbar from '../components/Navbar';

export default function DashboardPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white">Analytics Dashboard</h2>
          <p className="text-gray-400 mt-2">Track your trend analysis performance</p>
        </div>
        <Dashboard />
      </div>
    </main>
  );
}
