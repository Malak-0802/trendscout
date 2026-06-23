'use client';

import { useEffect, useState } from 'react';
import jsPDF from 'jspdf';

interface AnalysisData {
  product_name: string;
  sentiment_score: number;
  catwalk_adoption: number;
  streetstyle_adoption: number;
  prediction: string;
  risk_score: number;
  lifespan_months: number;
  image_url: string | null;
}

export default function TrendAnalyzer({ product }: { product: string }) {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!product) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          'http://localhost:8000/api/analyze-trend',
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              product_name: product,
              category: 'Ready-to-Wear',
              season: 'AH 2026/27'
            })
          }
        );

        if (!response.ok) throw new Error('API Error');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [product]);

  const downloadPDF = async () => {
    if (!data) return;

    try {
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      pdf.setFont('helvetica');

      const pageHeight = pdf.internal.pageSize.getHeight();
      const pageWidth = pdf.internal.pageSize.getWidth();
      const margin = 20;
      const textWidth = pageWidth - (margin * 2);
      let yPosition = 20;

      // Title
      pdf.setFontSize(24);
      pdf.setTextColor(0, 0, 0);
      pdf.text('TRENDSCOUT ANALYSIS', pageWidth / 2, yPosition, { align: 'center' });
      
      yPosition += 15;
      pdf.setFontSize(16);
      pdf.text(`Trend: ${data.product_name}`, pageWidth / 2, yPosition, { align: 'center' });
      
      yPosition += 15;
      pdf.setDrawColor(100, 100, 100);
      pdf.line(10, yPosition, pageWidth - 10, yPosition);
      
      yPosition += 10;

      // Add Product Image if exists
      if (data.image_url) {
        try {
          const imgWidth = 100;
          const imgHeight = 100;
          pdf.addImage(data.image_url, 'JPEG', (pageWidth - imgWidth) / 2, yPosition, imgWidth, imgHeight);
          yPosition += imgHeight + 10;
        } catch (imgErr) {
          console.error('Error adding image to PDF:', imgErr);
        }
      }

      // Metrics
      pdf.setFontSize(11);
      pdf.setTextColor(0, 0, 0);
      
      const metrics = [
        `Sentiment Score: ${data.sentiment_score.toFixed(0)}/100`,
        `Catwalk Adoption: ${data.catwalk_adoption.toFixed(0)}%`,
        `Streetstyle Adoption: ${data.streetstyle_adoption.toFixed(0)}%`,
        `Risk Score: ${data.risk_score.toFixed(0)}/100`,
        `Lifespan: ${data.lifespan_months} months`,
        `Verdict: ${data.prediction}`
      ];

      metrics.forEach(metric => {
        pdf.text(metric, margin, yPosition);
        yPosition += 8;
      });

      yPosition += 10;
      pdf.setDrawColor(100, 100, 100);
      pdf.line(10, yPosition, pageWidth - 10, yPosition);
      
      yPosition += 10;

      // Analysis Section
      const analysisContent = [
        { title: 'DETAILED ANALYSIS', text: '' },
        { title: '', text: `Trend: ${data.product_name}` },
        { title: 'EXECUTIVE SUMMARY', text: '' },
        { title: '', text: `Sentiment Score: ${data.sentiment_score}/100` },
        { title: '', text: `Catwalk Adoption Rate: ${data.catwalk_adoption}%` },
        { title: '', text: `Streetstyle Adoption Rate: ${data.streetstyle_adoption}%` },
        { title: '', text: `Market Risk Score: ${data.risk_score}/100` },
        { title: '', text: `Estimated Trend Duration: ${data.lifespan_months} months` },
        { title: 'VERDICT', text: `Status: ${data.prediction}` },
        { title: '', text: data.prediction === 'ADOPT' ? 
          'Strong positive signals detected. The trend shows high consumer interest and significant runway presence. Recommended for immediate integration into collections.' :
          data.prediction === 'MONITOR' ?
          'Mixed signals detected. Consumer sentiment is positive but adoption rates are moderate. Recommend monitoring evolution before major investment.' :
          'Weak market signals. Low consumer interest detected. Recommend avoiding major investments unless targeting niche segments.' },
        { title: 'RECOMMENDATION', text: '' },
        { title: '', text: data.prediction === 'ADOPT' ? 
          `ACTION: Integrate trend into collections immediately. Capitalize on positive momentum. Plan marketing campaigns for ${data.lifespan_months} months.` :
          data.prediction === 'MONITOR' ?
          'ACTION: Monitor public sentiment. Test with pilot pieces. Await confirmation signals before major investment.' :
          'ACTION: Avoid significant investment. Consider as niche only if aligned with brand strategy.' },
        { title: 'KEY INSIGHTS', text: '' },
        { title: '', text: `The trend shows ${data.sentiment_score > 70 ? 'very positive' : data.sentiment_score > 40 ? 'moderate positive' : 'negative'} sentiment.` },
        { title: '', text: `Market adoption is ${data.catwalk_adoption > 70 ? 'high on runways' : data.catwalk_adoption > 40 ? 'moderate on runways' : 'low on runways'}.` },
        { title: '', text: `Consumer adoption is ${data.streetstyle_adoption > 70 ? 'high in streetstyle' : data.streetstyle_adoption > 40 ? 'moderate in streetstyle' : 'low in streetstyle'}.` },
        { title: '', text: `Overall market risk is ${data.risk_score > 70 ? 'high' : data.risk_score > 40 ? 'moderate' : 'low'}.` },
        { title: '', text: '' },
        { title: '', text: 'Report Generated by Trendscout' },
        { title: '', text: 'Fashion Trend Forecasting with AI' }
      ];

      analysisContent.forEach(section => {
        if (yPosition > pageHeight - 15) {
          pdf.addPage();
          yPosition = 20;
        }

        if (section.title) {
          pdf.setFont('helvetica', 'bold');
          pdf.setFontSize(11);
          pdf.text(section.title, margin, yPosition);
          yPosition += 6;
        }

        if (section.text) {
          pdf.setFont('helvetica', 'normal');
          pdf.setFontSize(10);
          const lines = pdf.splitTextToSize(section.text, textWidth);
          lines.forEach((line: string) => {
            if (yPosition > pageHeight - 15) {
              pdf.addPage();
              yPosition = 20;
            }
            pdf.text(line, margin, yPosition);
            yPosition += 5;
          });
        }

        yPosition += 2;
      });

      pdf.save(`${data.product_name}-analysis.pdf`);
    } catch (err) {
      console.error('Error generating PDF:', err);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Analyzing...</div>;
  if (error) return <div className="text-red-400 p-8">Error: {error}</div>;
  if (!data) return <div className="text-gray-400 p-8">No data</div>;

  const sentimentColor = data.sentiment_score > 60 ? 'green' : data.sentiment_score > 0 ? 'blue' : 'red';
  const verdictColor = data.prediction === 'ADOPT' ? 'green' : data.prediction === 'MONITOR' ? 'blue' : 'red';

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-slate-900 rounded-lg border border-slate-700 p-8 space-y-6">
        
        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-white">{data.product_name}</h2>
          <p className="text-gray-400 mt-2">Trend Analysis Report</p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
            <p className="text-sm text-gray-400">Sentiment Score</p>
            <p className={`text-2xl font-bold mt-2 ${sentimentColor === 'green' ? 'text-green-400' : sentimentColor === 'blue' ? 'text-blue-400' : 'text-red-400'}`}>
              {data.sentiment_score}/100
            </p>
          </div>

          <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
            <p className="text-sm text-gray-400">Catwalk Adoption</p>
            <p className="text-2xl font-bold text-purple-400 mt-2">{data.catwalk_adoption}%</p>
          </div>

          <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
            <p className="text-sm text-gray-400">Streetstyle Adoption</p>
            <p className="text-2xl font-bold text-blue-400 mt-2">{data.streetstyle_adoption}%</p>
          </div>

          <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
            <p className="text-sm text-gray-400">Risk Score</p>
            <p className={`text-2xl font-bold mt-2 ${data.risk_score > 70 ? 'text-red-400' : 'text-green-400'}`}>
              {data.risk_score}/100
            </p>
          </div>
        </div>

        {/* Verdict */}
        <div className={`rounded-lg p-6 border ${
          verdictColor === 'green' ? 'bg-green-900/20 border-green-800' :
          verdictColor === 'blue' ? 'bg-blue-900/20 border-blue-800' :
          'bg-red-900/20 border-red-800'
        }`}>
          <p className={`text-sm font-semibold uppercase tracking-wide ${
            verdictColor === 'green' ? 'text-green-400' :
            verdictColor === 'blue' ? 'text-blue-400' :
            'text-red-400'
          }`}>
            VERDICT
          </p>
          <p className={`text-2xl font-bold mt-2 ${
            verdictColor === 'green' ? 'text-green-300' :
            verdictColor === 'blue' ? 'text-blue-300' :
            'text-red-300'
          }`}>
            {data.prediction === 'ADOPT' ? 'ADOPT' :
             data.prediction === 'MONITOR' ? 'MONITOR' : 'AVOID'}
          </p>
          <p className="text-gray-300 mt-3">
            Estimated lifespan: {data.lifespan_months} months
          </p>
        </div>

        {/* Analysis Summary */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-bold text-white mb-4">Analysis Summary</h3>
          <div className="space-y-3 text-gray-300 text-sm">
            <p><strong>Sentiment:</strong> {data.sentiment_score > 70 ? 'Very Positive' : data.sentiment_score > 40 ? 'Moderately Positive' : 'Negative'}</p>
            <p><strong>Catwalk Presence:</strong> {data.catwalk_adoption > 70 ? 'Strong runway presence' : data.catwalk_adoption > 40 ? 'Moderate runway presence' : 'Limited runway presence'}</p>
            <p><strong>Consumer Adoption:</strong> {data.streetstyle_adoption > 70 ? 'High street adoption' : data.streetstyle_adoption > 40 ? 'Moderate street adoption' : 'Low street adoption'}</p>
            <p><strong>Risk Level:</strong> {data.risk_score > 70 ? 'High' : data.risk_score > 40 ? 'Moderate' : 'Low'}</p>
          </div>
        </div>

      </div>

      {/* Download Button */}
      <button
        onClick={downloadPDF}
        className="mt-6 w-full px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold text-white transition"
      >
        Download as PDF
      </button>
    </div>
  );
}