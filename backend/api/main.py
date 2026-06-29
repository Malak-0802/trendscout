from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
import sys
import asyncio
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

load_dotenv(dotenv_path="../.env")

from scrapers.review_scraper import get_product_reviews
from integrations.ollama_analyzer import analyze_with_ollama

print("\n✅ Imports réussis")

# ====== CONFIGURATION ======
app = FastAPI(title="Trendscout API", version="1.0.0-FINAL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:9999")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2-fashion-hf")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "default_key")
API_PORT = int(os.getenv("API_PORT", 8000))
API_HOST = os.getenv("API_HOST", "0.0.0.0")

fake_analyses_db = []

# ====== MODELS ======
class TrendAnalysisRequest(BaseModel):
    product_name: str
    category: str
    season: str

# ====== FONCTIONS ======

def get_product_image(product_name: str):
    """Return no product image to keep analysis fast."""
    return ""


async def generate_analysis_final(product_name: str):
    """
    SOLUTION FINALE: Scraping réel + Fine-tuning Hugging Face + Ollama
    """
    
    print(f"\n{'='*80}")
    print(f" ANALYSE COMPLÈTE: {product_name}")
    print(f"{'='*80}")
    
    # ÉTAPE 1: Scraper
    print(f"\n📥 ÉTAPE 1: Scraping des avis réels...")
    reviews = await get_product_reviews(product_name)
    
    if not reviews:
        print(f"⚠️ Aucun avis trouvé")
        return {
            "product_name": product_name,
            "sentiment_score": 50,
            "catwalk_adoption": 50,
            "streetstyle_adoption": 40,
            "prediction": "MONITOR",
            "risk_score": 50,
            "lifespan_months": 12,
            "image_url": get_product_image(product_name),
            "data_source": "No reviews found",
            "review_count": 0,
            "error": "Pas d'avis disponibles"
        }
    
    print(f"✅ {len(reviews)} avis extraits")
    
    # ÉTAPE 2: Analyser avec Ollama fine-tuned
    print(f"\n🤖 ÉTAPE 2: Analyse avec Ollama fine-tuned...")
    try:
        aggregated_analysis = await analyze_with_ollama(
            reviews=reviews,
            product_name=product_name,
            ollama_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL
        )
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return {
            "product_name": product_name,
            "error": str(e),
            "data_source": "Error",
            "message": "Assurez-vous qu'Ollama est lancé: ollama serve"
        }
    
    # ÉTAPE 3: Image
    print(f"\n  ÉTAPE 3: Image...")
    image_url = get_product_image(product_name)
    
    print(f"\n✅ Analyse complète")
    
    return {
        "product_name": product_name,
        "sentiment_score": aggregated_analysis['sentiment_score'],
        "catwalk_adoption": aggregated_analysis['catwalk_adoption'],
        "streetstyle_adoption": aggregated_analysis['streetstyle_adoption'],
        "prediction": aggregated_analysis['prediction'],
        "risk_score": aggregated_analysis['risk_score'],
        "lifespan_months": aggregated_analysis['lifespan_months'],
        "image_url": image_url,
        "data_source": "Real web scraping + Hugging Face fine-tuned Llama2",
        "review_count": aggregated_analysis['total_reviews_analyzed'],
        "viability_breakdown": aggregated_analysis.get('viability_breakdown', {})
    }

# ====== ENDPOINTS ======

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "version": "1.0.0-FINAL",
        "architecture": "Web Scraping + Hugging Face Fine-tuning + Ollama",
        "ollama_model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_BASE_URL
    }

@app.post("/api/analyze-trend")
async def analyze_trend(request: TrendAnalysisRequest):
    """
    Analyse complète avec scraping + fine-tuning
    """
    
    print(f"\n{'='*80}")
    print(f" NOUVELLE ANALYSE: {request.product_name}")
    print(f"{'='*80}")
    
    analysis = await generate_analysis_final(request.product_name)
    
    fake_analyses_db.append(analysis)
    
    return analysis

@app.get("/api/analyses")
async def get_analyses():
    """Toutes les analyses"""
    return fake_analyses_db

if __name__ == "__main__":
    import uvicorn
    
    print(f"\n{'='*80}")
    print(f" TRENDSCOUT API - VERSION FINALE")
    print(f"{'='*80}")
    print(f"\n Serveur: http://{API_HOST}:{API_PORT}")
    print(f" Model: {OLLAMA_MODEL}")
    print(f" Ollama: {OLLAMA_BASE_URL}")
    print(f"\n Architecture:")
    print(f"   1. Web Scraping (Google, Reddit, HN)")
    print(f"   2. Fine-tuning Hugging Face datasets")
    print(f"   3. Ollama analysis")
    print(f"\n Documentation: http://localhost:{API_PORT}/docs")
    print(f"{'='*80}\n")
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)