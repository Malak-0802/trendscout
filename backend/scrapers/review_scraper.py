"""
Web scraper pour extraire les avis réels
Source: Google, Twitter/X, Reddit, forums
"""

import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict
import re

class ReviewScraper:
    """
    Scrape les avis de multiples sources
    """
    
    def __init__(self):
        self.timeout = 10.0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def scrape_searx(self, product_name: str, max_results: int = 8) -> List[Dict]:
        """
        Scrape via SearXNG (métamoteur open source)
        """
        
        print(f"\n🔍 Scraping SearXNG pour: {product_name}")
        
        try:
            search_query = f"{product_name} review avis opinion feedback"
            
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.get(
                    "https://searx.be/search",
                    params={
                        "q": search_query,
                        "format": "json",
                        "lang": "fr"
                    }
                )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])[:max_results]
                
                reviews = []
                for result in results:
                    content = result.get('content', '')
                    if content and len(content) > 20:
                        reviews.append({
                            'source': 'searx',
                            'product': product_name,
                            'title': result.get('title', '')[:100],
                            'content': content[:300],
                            'url': result.get('url', '')
                        })
                
                print(f"✅ {len(reviews)} résultats trouvés")
                return reviews
        
        except Exception as e:
            print(f"❌ Erreur SearXNG: {e}")
        
        return []
    
    async def scrape_reddit(self, product_name: str, max_results: int = 5) -> List[Dict]:
        """Scrape Reddit (public)"""
        
        print(f"\n🔍 Scraping Reddit pour: {product_name}")
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.get(
                    f"https://old.reddit.com/r/fashion/search.json",
                    params={
                        "q": product_name,
                        "limit": max_results,
                        "sort": "new"
                    }
                )
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])[:max_results]
                
                reviews = []
                for post in posts:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    
                    content = f"{title}. {selftext}"[:300]
                    
                    if content and len(content) > 20:
                        reviews.append({
                            'source': 'reddit',
                            'product': product_name,
                            'title': title[:100],
                            'content': content,
                            'url': f"https://reddit.com{post_data.get('permalink', '')}"
                        })
                
                print(f"✅ {len(reviews)} posts trouvés")
                return reviews
        
        except Exception as e:
            print(f"❌ Erreur Reddit: {e}")
        
        return []
    
    async def scrape_hacker_news(self, product_name: str, max_results: int = 4) -> List[Dict]:
        """Scrape Hacker News"""
        
        print(f"\n🔍 Scraping Hacker News pour: {product_name}")
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.get(
                    "https://hn.algolia.com/api/v1/search",
                    params={
                        "query": product_name,
                        "hitsPerPage": max_results
                    }
                )
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', [])[:max_results]
                
                reviews = []
                for hit in hits:
                    title = hit.get('title', '')
                    story_text = hit.get('story_text', '')
                    
                    content = f"{title}. {story_text}"[:300]
                    
                    if content and len(content) > 20:
                        reviews.append({
                            'source': 'hackernews',
                            'product': product_name,
                            'title': title[:100],
                            'content': content,
                            'url': hit.get('story_url', '')
                        })
                
                print(f"✅ {len(reviews)} articles trouvés")
                return reviews
        
        except Exception as e:
            print(f"❌ Erreur Hacker News: {e}")
        
        return []
    
    async def scrape_all_sources(self, product_name: str) -> List[Dict]:
        """Scrape toutes les sources en parallèle"""
        
        print(f"\n{'='*70}")
        print(f"🚀 EXTRACTION MULTI-SOURCE: {product_name}")
        print(f"{'='*70}")
        
        results = await asyncio.gather(
            self.scrape_searx(product_name, max_results=6),
            self.scrape_reddit(product_name, max_results=4),
            self.scrape_hacker_news(product_name, max_results=3)
        )
        
        all_reviews = []
        for source_reviews in results:
            all_reviews.extend(source_reviews)
        
        print(f"\n{'='*70}")
        print(f"✅ TOTAL: {len(all_reviews)} avis extraits")
        print(f"{'='*70}")
        
        return all_reviews


async def get_product_reviews(product_name: str) -> List[Dict]:
    """Fonction publique"""
    scraper = ReviewScraper()
    return await scraper.scrape_all_sources(product_name)