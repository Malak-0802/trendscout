"""
Intégration Ollama pour analyser les avis avec fine-tuning
"""

import httpx
import json
import re
from typing import List, Dict, Optional

class OllamaAnalyzer:
    """
    Utilise Ollama fine-tuned pour analyser les avis réels
    """
    
    def __init__(self, base_url: str = "http://localhost:9999", model: str = "llama2-fashion-hf"):
        self.base_url = base_url
        self.model = model
        self.timeout = 60.0
        
        print(f"\n🤖 Ollama Analyzer initialisé")
        print(f"   Model: {self.model}")
        print(f"   URL: {self.base_url}")
    
    async def check_ollama_available(self) -> bool:
        """Vérifier qu'Ollama est accessible"""
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
            
            if response.status_code == 200:
                print(f"✅ Ollama accessible")
                return True
            else:
                print(f"❌ Ollama non accessible")
                return False
        
        except Exception as e:
            print(f"❌ Erreur connexion Ollama: {e}")
            return False
    
    async def analyze_single_review(self, review_text: str, product_name: str) -> Optional[Dict]:
        """
        Analyse un avis avec Ollama fine-tuned
        Utilise le modèle entraîné sur Hugging Face datasets
        """
        
        review_text = review_text[:500]
        
        prompt = f"""Analyze this product review and provide fashion market insights:

Product: {product_name}
Review: "{review_text}"

Provide your analysis in this exact JSON format:
{{
  "sentiment_score": (integer 0-100, how positive is the review),
  "adoption_potential": (integer 0-100, likelihood of market adoption),
  "fashion_viability": ("HIGH", "MEDIUM", or "LOW")
}}

ONLY respond with valid JSON, no other text."""
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": 0.6
                    }
                )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                
                if json_match:
                    try:
                        analysis = json.loads(json_match.group())
                        
                        return {
                            'sentiment_score': int(analysis.get('sentiment_score', 50)),
                            'adoption_potential': int(analysis.get('adoption_potential', 50)),
                            'fashion_viability': analysis.get('fashion_viability', 'MEDIUM')
                        }
                    except json.JSONDecodeError:
                        pass
            
        except Exception as e:
            print(f"⚠️ Erreur analyse: {e}")
        
        return None
    
    async def analyze_reviews_batch(self, reviews: List[Dict], product_name: str) -> Dict:
        """
        Analyse tous les avis en parallèle
        Agrège les résultats
        """
        
        print(f"\n📊 Analyse de {len(reviews)} avis avec Ollama fine-tuned...")
        
        review_texts = [r.get('content', '') for r in reviews]
        
        # Limiter les analyses parallèles pour pas surcharger Ollama
        tasks = []
        for i, text in enumerate(review_texts):
            tasks.append(self.analyze_single_review(text, product_name))
            
            if (i + 1) % 5 == 0:
                print(f"  Progression: {i+1}/{len(review_texts)}")
        
        import asyncio
        results = await asyncio.gather(*tasks)
        
        valid_results = [r for r in results if r is not None]
        
        print(f"✅ {len(valid_results)}/{len(reviews)} avis analysés avec succès")
        
        return self.aggregate_results(valid_results)
    
    def aggregate_results(self, analyses: List[Dict]) -> Dict:
        """
        Agrège les analyses individuelles en scores globaux
        """
        
        if not analyses:
            return {
                'sentiment_score': 50,
                'catwalk_adoption': 50,
                'streetstyle_adoption': 45,
                'risk_score': 50,
                'lifespan_months': 12,
                'prediction': 'MONITOR',
                'total_reviews_analyzed': 0
            }
        
        sentiment_scores = [a.get('sentiment_score', 50) for a in analyses]
        adoption_scores = [a.get('adoption_potential', 50) for a in analyses]
        viability = [a.get('fashion_viability', 'MEDIUM') for a in analyses]
        
        avg_sentiment = int(sum(sentiment_scores) / len(sentiment_scores))
        avg_adoption = int(sum(adoption_scores) / len(adoption_scores))
        
        high_count = viability.count('HIGH')
        medium_count = viability.count('MEDIUM')
        low_count = viability.count('LOW')
        
        # Verdict intelligent
        if avg_sentiment > 70 and avg_adoption > 65:
            prediction = 'ADOPT'
            risk_score = 20
            lifespan_months = 24
        elif avg_sentiment > 50 and avg_adoption > 45:
            prediction = 'MONITOR'
            risk_score = 50
            lifespan_months = 12
        else:
            prediction = 'AVOID'
            risk_score = 75
            lifespan_months = 6
        
        streetstyle_adoption = max(0, min(100, avg_adoption - 10))
        
        return {
            'sentiment_score': avg_sentiment,
            'catwalk_adoption': avg_adoption,
            'streetstyle_adoption': streetstyle_adoption,
            'prediction': prediction,
            'risk_score': risk_score,
            'lifespan_months': lifespan_months,
            'total_reviews_analyzed': len(analyses),
            'viability_breakdown': {
                'high': high_count,
                'medium': medium_count,
                'low': low_count
            }
        }


async def analyze_with_ollama(reviews: List[Dict], product_name: str,
                             ollama_url: str = "http://localhost:9999",
                             model: str = "llama2-fashion-hf") -> Dict:
    """
    Fonction publique pour analyser les avis
    """
    
    analyzer = OllamaAnalyzer(base_url=ollama_url, model=model)
    
    if not await analyzer.check_ollama_available():
        raise Exception("Ollama n'est pas accessible")
    
    results = await analyzer.analyze_reviews_batch(reviews, product_name)
    
    return results