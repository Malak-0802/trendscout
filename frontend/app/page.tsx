'use client';

import { useState } from 'react';
import TrendAnalyzer from './components/TrendAnalyzer';

export default function Home() {
  const [productName, setProductName] = useState('Gorpcore');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <header className="bg-slate-900 border-b border-slate-700 sticky top-0">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-white">🎯 Trendscout</h1>
          <p className="text-gray-400 mt-1">Fashion Trend Forecasting with AI</p>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="Enter trend name..."
              className="flex-1 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-gray-500 focus:outline-none focus:border-blue-500"
            />
            <button
              type="submit"
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold text-white transition"
            >
              Analyze
            </button>
          </div>
        </form>

        {submitted && productName && (
          <div className="bg-slate-800 rounded-lg border border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Analysis: {productName}</h2>
            <TrendAnalyzer product={productName} />
          </div>
        )}

        <div className="mt-12">
          <h2 className="text-2xl font-bold text-white mb-6">Featured Trends</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {['Gorpcore', 'Quiet Luxury', 'Y2K Revival'].map((trend) => (
              <button
                key={trend}
                onClick={() => {
                  setProductName(trend);
                  setSubmitted(true);
                }}
                className="p-4 bg-slate-800 border border-slate-700 rounded-lg hover:border-blue-500 transition text-left"
              >
                <p className="font-semibold text-white">{trend}</p>
                <p className="text-sm text-gray-400 mt-1">Click to analyze</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
