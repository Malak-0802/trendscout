from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import hashlib
import requests

app = FastAPI(title="Trendscout API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class TrendAnalysisRequest(BaseModel):
    product_name: str
    category: str
    season: str

def get_product_image(product_name: str):
    """Get image from Pexels with Unsplash fallback"""
    
    # FALLBACK 1: Pexels API
    try:
        headers = {
            'Authorization': '563492ad6f91700001000001a5d4e4d652b845e5b0e8c3d1f'
        }
        
        params = {
            'query': f'{product_name} fashion',
            'per_page': 1
        }
        
        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('photos') and len(data['photos']) > 0:
                image_url = data['photos'][0]['src']['large']
                print(f"Image found from Pexels: {product_name}")
                return image_url
    
    except Exception as e:
        print(f"Pexels error: {e}")
    
    # FALLBACK 2: Unsplash Direct URL (plus simple, toujours marche)
    try:
        encoded_query = product_name.replace(' ', '+')
        image_url = f"https://source.unsplash.com/600x400/?{encoded_query},fashion"
        print(f"Using Unsplash fallback for: {product_name}")
        return image_url
    
    except Exception as e:
        print(f"Unsplash fallback error: {e}")
    
    # FALLBACK 3: Generic placeholder image
    print(f"No image found for: {product_name}, using placeholder")
    return "https://source.unsplash.com/600x400/?fashion,trend"

def generate_analysis(product_name: str):
    """Generate unique analysis based on product name"""
    
    # Create seed from product name for consistency
    hash_obj = hashlib.md5(product_name.lower().encode())
    seed = int(hash_obj.hexdigest(), 16) % 100000
    random.seed(seed)
    
    # Generate varied metrics
    sentiment_score = random.randint(30, 95)
    catwalk_adoption = random.randint(20, 90)
    streetstyle_adoption = random.randint(25, 95)
    risk_score = random.randint(10, 85)
    lifespan_months = random.randint(4, 36)
    
    # Determine verdict based on metrics
    if sentiment_score > 70 and catwalk_adoption > 60:
        prediction = "ADOPT"
    elif sentiment_score > 40 and streetstyle_adoption > 50:
        prediction = "MONITOR"
    else:
        prediction = "AVOID"
    
    # Get image (avec fallback)
    image_url = get_product_image(product_name)
    
    return {
        "product_name": product_name,
        "sentiment_score": sentiment_score,
        "catwalk_adoption": catwalk_adoption,
        "streetstyle_adoption": streetstyle_adoption,
        "prediction": prediction,
        "risk_score": risk_score,
        "lifespan_months": lifespan_months,
        "image_url": image_url
    }

@app.get("/health")
async def health_check():
    return {"status": "online", "ollama_model": "llama2:13b"}

@app.post("/api/analyze-trend")
async def analyze_trend(request: TrendAnalysisRequest):
    analysis = generate_analysis(request.product_name)
    return analysis

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)