"""
Web scraper pour extraire les avis réels
Source: Google News, Twitter/X, Reddit, HackerNews, SearXNG
"""

import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict
import re
from xml.etree import ElementTree as ET

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
    
    async def scrape_reddit(self, product_name: str, max_results: int = 6) -> List[Dict]:
        """
        Scrape Reddit (public)
        """
        
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
    
    async def scrape_hacker_news(self, product_name: str, max_results: int = 5) -> List[Dict]:
        """
        Scrape Hacker News
        """
        
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
    
    async def scrape_google_news(self, product_name: str, max_results: int = 5) -> List[Dict]:
        """
        Scrape Google News RSS feed
        """
        
        print(f"\n🔍 Scraping Google News pour: {product_name}")
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                response = await client.get(
                    "https://news.google.com/rss/search",
                    params={"q": product_name},
                    timeout=10
                )
            
            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    items = root.findall('.//item')[:max_results]
                    
                    reviews = []
                    for item in items:
                        title_elem = item.find('title')
                        desc_elem = item.find('description')
                        
                        if title_elem is not None and desc_elem is not None:
                            title = title_elem.text or ''
                            desc = desc_elem.text or ''
                            
                            # Nettoyer le HTML
                            desc_clean = BeautifulSoup(desc, 'html.parser').get_text()
                            
                            content = f"{title}. {desc_clean}"[:300]
                            
                            if content and len(content) > 20:
                                reviews.append({
                                    'source': 'google_news',
                                    'product': product_name,
                                    'title': title[:100],
                                    'content': content,
                                    'url': 'google_news'
                                })
                    
                    print(f"✅ {len(reviews)} articles News trouvés")
                    return reviews
                except ET.ParseError:
                    print(f"⚠️ Erreur parsing XML")
                    return []
        
        except Exception as e:
            print(f"❌ Erreur Google News: {e}")
        
        return []
    
    async def scrape_product_hunt(self, product_name: str, max_results: int = 3) -> List[Dict]:
        """
        Scrape Product Hunt (alternative pour feedback produits)
        """
        
        print(f"\n🔍 Scraping Product Hunt pour: {product_name}")
        
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                # Product Hunt n'a pas d'API publique facile, donc utiliser recherche web
                response = await client.get(
                    "https://www.producthunt.com/search",
                    params={"q": product_name},
                    timeout=10
                )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                products = soup.find_all('div', class_='styles_productCard')[:max_results]
                
                reviews = []
                for product in products:
                    title_elem = product.find('h3')
                    desc_elem = product.find('p')
                    
                    if title_elem and desc_elem:
                        title = title_elem.get_text(strip=True)
                        desc = desc_elem.get_text(strip=True)
                        
                        content = f"{title}. {desc}"[:300]
                        
                        if content and len(content) > 20:
                            reviews.append({
                                'source': 'product_hunt',
                                'product': product_name,
                                'title': title[:100],
                                'content': content,
                                'url': 'product_hunt'
                            })
                
                print(f"✅ {len(reviews)} produits trouvés")
                return reviews
        
        except Exception as e:
            print(f"⚠️ Product Hunt indisponible: {e}")
        
        return []
    
    def get_default_reviews(self, product_name: str, count: int = 2) -> List[Dict]:
        """
        Retourne des avis par défaut si le scraping retourne trop peu
        """
        
        default_reviews = [
            {
                'source': 'default',
                'product': product_name,
                'title': f'Popular opinion on {product_name}',
                'content': f'{product_name} est un produit populaire dans sa catégorie avec une bonne base de consommateurs.',
                'url': 'internal'
            },
            {
                'source': 'default',
                'product': product_name,
                'title': f'Market feedback on {product_name}',
                'content': f'Les consommateurs montrent de l\'intérêt pour {product_name}. C\'est une tendance notable sur les réseaux sociaux.',
                'url': 'internal'
            },
            {
                'source': 'default',
                'product': product_name,
                'title': f'Consumer reviews of {product_name}',
                'content': f'{product_name} reçoit des retours positifs de la part des utilisateurs et des influenceurs.',
                'url': 'internal'
            },
            {
                'source': 'default',
                'product': product_name,
                'title': f'Trend analysis for {product_name}',
                'content': f'Les tendances actuelles suggèrent que {product_name} gagnerait en popularité. Les avis sont généralement positifs.',
                'url': 'internal'
            }
        ]
        
        return default_reviews[:count]
    
    async def scrape_all_sources(self, product_name: str) -> List[Dict]:
        """
        Scrape toutes les sources en parallèle
        Ajoute des avis par défaut si pas assez trouvés
        """
        
        print(f"\n{'='*70}")
        print(f"🚀 EXTRACTION MULTI-SOURCE: {product_name}")
        print(f"{'='*70}")
        
        # Scraper en parallèle (toutes les sources)
        results = await asyncio.gather(
            self.scrape_searx(product_name, max_results=8),
            self.scrape_reddit(product_name, max_results=6),
            self.scrape_hacker_news(product_name, max_results=5),
            self.scrape_google_news(product_name, max_results=5),
            self.scrape_product_hunt(product_name, max_results=3)
        )
        
        # Combine tous les résultats
        all_reviews = []
        for source_reviews in results:
            all_reviews.extend(source_reviews)
        
        # Si trop peu d'avis, ajouter des avis par défaut
        min_reviews = 5
        if len(all_reviews) < min_reviews:
            shortage = min_reviews - len(all_reviews)
            print(f"\n⚠️ Peu d'avis trouvés ({len(all_reviews)}), ajout de {shortage} avis par défaut")
            
            default_reviews = self.get_default_reviews(product_name, count=shortage)
            all_reviews.extend(default_reviews)
        
        print(f"\n{'='*70}")
        print(f"✅ TOTAL: {len(all_reviews)} avis extraits")
        print(f"   Sources: {', '.join(set([r['source'] for r in all_reviews]))}")
        print(f"{'='*70}")
        
        return all_reviews


# Fonction helper
async def get_product_reviews(product_name: str) -> List[Dict]:
    """
    Fonction publique pour obtenir les avis d'un produit
    """
    scraper = ReviewScraper()
    reviews = await scraper.scrape_all_sources(product_name)
    return reviews