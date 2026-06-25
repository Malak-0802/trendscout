"""
Télécharge les datasets de Hugging Face
"""

from datasets import load_dataset
import json
from pathlib import Path
from typing import List, Dict

class DatasetDownloader:
    """
    Télécharge et prépare les datasets fashion depuis Hugging Face
    """
    
    def __init__(self):
        self.data_dir = Path(__file__).parent
    
    def download_amazon_reviews(self, max_samples: int = 5000) -> List[Dict]:
        """
        Télécharge Amazon reviews depuis Hugging Face
        Format: product, review text, rating
        """
        
        print(f"\n📥 Téléchargement du dataset Amazon Reviews...")
        
        try:
            # Télécharge depuis Hugging Face (gratuit, open source)
            dataset = load_dataset(
                "amazon_reviews_multi", 
                "en",
                split="train[:5000]",  # 5000 premiers exemples
                trust_remote_code=True
            )
            
            print(f"✅ Dataset téléchargé: {len(dataset)} exemples")
            
            reviews = []
            for item in dataset:
                # Extrait les champs pertinents
                review_text = item.get('review_body', '')
                rating = item.get('stars', 3)
                product_name = item.get('product_category', 'Fashion')
                
                # Convertir rating (1-5) en sentiment (0-100)
                sentiment_score = int((rating / 5) * 100)
                
                if review_text and len(review_text) > 20:
                    reviews.append({
                        'product': product_name,
                        'text': review_text[:300],  # Limiter longueur
                        'sentiment': sentiment_score,
                        'rating': rating
                    })
            
            print(f"✅ {len(reviews)} reviews extraits")
            return reviews
        
        except Exception as e:
            print(f"⚠️ Erreur téléchargement: {e}")
            print(f"   Installation: pip install datasets")
            return []
    
    def download_yelp_reviews(self, max_samples: int = 3000) -> List[Dict]:
        """
        Télécharge Yelp reviews pour plus de variété
        """
        
        print(f"\n📥 Téléchargement du dataset Yelp...")
        
        try:
            dataset = load_dataset(
                "yelp_review_full",
                split="train[:3000]",
                trust_remote_code=True
            )
            
            print(f"✅ Dataset Yelp téléchargé: {len(dataset)} exemples")
            
            reviews = []
            for item in dataset:
                text = item.get('text', '')
                label = item.get('label', 2)  # 0-4 star rating
                
                # Convertir label (0-4) en sentiment (0-100)
                sentiment_score = int(((label + 1) / 5) * 100)
                
                if text and len(text) > 20:
                    reviews.append({
                        'product': 'Restaurant/Venue',
                        'text': text[:300],
                        'sentiment': sentiment_score,
                        'rating': label + 1
                    })
            
            print(f"✅ {len(reviews)} reviews Yelp extraits")
            return reviews
        
        except Exception as e:
            print(f"⚠️ Erreur Yelp: {e}")
            return []
    
    def save_as_jsonl(self, reviews: List[Dict], filename: str = "training_data.jsonl"):
        """
        Sauvegarde les reviews en format JSONL pour fine-tuning
        """
        
        filepath = self.data_dir / filename
        
        print(f"\n💾 Sauvegarde en JSONL: {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for review in reviews:
                f.write(json.dumps(review) + '\n')
        
        print(f"✅ {len(reviews)} exemples sauvegardés")
        return filepath
    
    def download_and_prepare(self) -> Path:
        """
        Télécharge tous les datasets et prépare le fichier JSONL
        """
        
        print(f"\n{'='*80}")
        print(f"📊 TÉLÉCHARGEMENT DES DATASETS HUGGING FACE")
        print(f"{'='*80}")
        
        all_reviews = []
        
        # Amazon
        amazon_reviews = self.download_amazon_reviews()
        all_reviews.extend(amazon_reviews)
        
        # Yelp (pour variété)
        yelp_reviews = self.download_yelp_reviews()
        all_reviews.extend(yelp_reviews)
        
        print(f"\n{'='*80}")
        print(f"✅ TOTAL: {len(all_reviews)} exemples combinés")
        print(f"{'='*80}")
        
        # Sauvegarder
        jsonl_path = self.save_as_jsonl(all_reviews, "fashion_training_data.jsonl")
        
        return jsonl_path


# Fonction helper
def download_training_data() -> Path:
    """
    Fonction publique pour télécharger les données d'entraînement
    """
    downloader = DatasetDownloader()
    return downloader.download_and_prepare()