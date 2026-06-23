'use client';

import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Analysis {
  product_name: string;
  sentiment_score: number;
  catwalk_adoption: number;
  streetstyle_adoption: number;
  prediction: string;
  risk_score: number;
  lifespan_months: number;
}

export default function Dashboard() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/analyses');
      if (response.ok) {
        const data = await response.json();
        setAnalyses(data);
      }
    } catch (error) {
      console.error('Error fetching analyses:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center p-8 text-gray-400">Loading dashboard...</div>;
  }

  if (analyses.length === 0) {
    return <div className="text-center p-8 text-gray-400">No analyses yet. Start analyzing trends!</div>;
  }

  const sentimentData = analyses.map((a, i) => ({
    name: a.product_name.substring(0, 10),
    sentiment: a.sentiment_score,
    risk: a.risk_score
  }));

  const adoptionData = analyses.map((a) => ({
    name: a.product_name.substring(0, 15),
    catwalk: a.catwalk_adoption,
    streetstyle: a.streetstyle_adoption
  }));

  const verdictCounts = {
    ADOPT: analyses.filter(a => a.prediction === 'ADOPT').length,
    MONITOR: analyses.filter(a => a.prediction === 'MONITOR').length,
    AVOID: analyses.filter(a => a.prediction === 'AVOID').length
  };

  const verdictData = [
    { name: 'ADOPT', value: verdictCounts.ADOPT, color: '#10b981' },
    { name: 'MONITOR', value: verdictCounts.MONITOR, color: '#3b82f6' },
    { name: 'AVOID', value: verdictCounts.AVOID, color: '#ef4444' }
  ];

  const avgSentiment = Math.round(analyses.reduce((a, b) => a + b.sentiment_score, 0) / analyses.length);
  const avgAdoption = Math.round((analyses.reduce((a, b) => a + b.catwalk_adoption + b.streetstyle_adoption, 0) / (analyses.length * 2)));

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <p className="text-sm text-gray-400 mb-2">Total Analyses</p>
          <p className="text-3xl font-bold text-white">{analyses.length}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <p className="text-sm text-gray-400 mb-2">Avg Sentiment</p>
          <p className="text-3xl font-bold text-blue-400">{avgSentiment}/100</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <p className="text-sm text-gray-400 mb-2">Avg Adoption</p>
          <p className="text-3xl font-bold text-purple-400">{avgAdoption}%</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <p className="text-sm text-gray-400 mb-2">Trending</p>
          <p className="text-3xl font-bold text-green-400">{verdictCounts.ADOPT}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-white mb-4">Sentiment & Risk Analysis</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={sentimentData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} labelStyle={{ color: '#fff' }} />
              <Legend />
              <Line type="monotone" dataKey="sentiment" stroke="#3b82f6" strokeWidth={2} name="Sentiment Score" />
              <Line type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} name="Risk Score" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-white mb-4">Adoption Rates</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={adoptionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} labelStyle={{ color: '#fff' }} />
              <Legend />
              <Bar dataKey="catwalk" fill="#a855f7" name="Catwalk" />
              <Bar dataKey="streetstyle" fill="#06b6d4" name="Streetstyle" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-white mb-4">Verdict Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={verdictData} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name}: ${value}`} outerRadius={100} fill="#8884d8" dataKey="value">
                {verdictData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }} labelStyle={{ color: '#fff' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-white mb-4">Recent Trends</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {analyses.slice(-5).reverse().map((analysis, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-slate-700 rounded-lg">
                <div>
                  <p className="font-semibold text-white">{analysis.product_name}</p>
                  <p className="text-sm text-gray-400">{analysis.sentiment_score}/100 sentiment</p>
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  analysis.prediction === 'ADOPT' ? 'bg-green-900/30 text-green-400' :
                  analysis.prediction === 'MONITOR' ? 'bg-blue-900/30 text-blue-400' :
                  'bg-red-900/30 text-red-400'
                }`}>
                  {analysis.prediction}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}