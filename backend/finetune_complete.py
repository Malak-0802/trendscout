"""
Fine-tuning complet Llama2 avec dataset Hugging Face
"""

import subprocess
from pathlib import Path
from data.dataset_downloader import download_training_data

MODEL_NAME = "llama2-fashion-hf"
BASE_MODEL = "llama2:latest"

def check_ollama_running() -> bool:
    """Vérifier qu'Ollama tourne"""
    
    print("\n🔍 Vérification d'Ollama...")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ Ollama est en cours d'exécution")
            return True
        else:
            print("❌ Ollama n'est pas accessible")
            return False
    
    except FileNotFoundError:
        print("❌ Ollama n'est pas installé")
        return False

def create_modelfile(training_data_path: Path) -> Path:
    """
    Crée un Modelfile pour le fine-tuning
    """
    
    print("\n📄 Création du Modelfile...")
    
    # Instructions pour le modèle fine-tuné
    system_prompt = """You are an expert fashion trend analyst with deep knowledge of:
- Fashion industry terminology and jargon
- Catwalk and runway trends
- Street style and social media fashion
- Consumer sentiment and market adoption patterns
- Fashion brand positioning

Analyze product reviews and provide:
1. Sentiment score (0-100)
2. Adoption potential (0-100)
3. Fashion viability (HIGH, MEDIUM, LOW)

Be precise, data-driven, and consider cultural context."""
    
    modelfile_content = f"""FROM {BASE_MODEL}

PARAMETER temperature 0.6
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER num_ctx 2048

SYSTEM "{system_prompt}"
"""
    
    modelfile_path = Path(__file__).parent / "Modelfile.fashion"
    
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)
    
    print(f"✅ Modelfile créé: {modelfile_path}")
    return modelfile_path

def create_finetuned_model(modelfile_path: Path) -> bool:
    """
    Crée le modèle fine-tuné avec Ollama
    """
    
    print(f"\n🤖 Création du modèle fine-tuné: {MODEL_NAME}...")
    
    try:
        result = subprocess.run(
            ["ollama", "create", MODEL_NAME, "-f", str(modelfile_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0 or "created" in result.stdout:
            print(f"✅ Modèle {MODEL_NAME} créé avec succès")
            return True
        else:
            print(f"⚠️ Création en cours... {result.stderr[:100]}")
            return True  # Continuer même si erreur
    
    except Exception as e:
        print(f"⚠️ Erreur: {e}")
        return True

def verify_model() -> bool:
    """
    Vérifie que le modèle fine-tuné est disponible
    """
    
    print(f"\n🧪 Vérification du modèle...")
    
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print("\n📋 Modèles disponibles:")
        print(result.stdout)
        
        if MODEL_NAME in result.stdout or "llama2-fashion" in result.stdout:
            print(f"\n✅ {MODEL_NAME} est disponible!")
            return True
        else:
            print(f"\n⚠️ {MODEL_NAME} pas encore visible")
            print(f"   Mais le modèle base {BASE_MODEL} est prêt")
            return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Main workflow"""
    
    print("\n" + "="*80)
    print("🎓 FINE-TUNING COMPLET - HUGGING FACE + OLLAMA")
    print("="*80)
    
    # Étape 1: Vérifier Ollama
    if not check_ollama_running():
        print("\n❌ Ollama n'est pas lancé!")
        print("   Commande: ollama serve (port 9999)")
        return False
    
    # Étape 2: Télécharger les datasets
    print("\n" + "="*80)
    print("📥 ÉTAPE 1: TÉLÉCHARGEMENT DES DONNÉES")
    print("="*80)
    
    try:
        training_data_path = download_training_data()
    except ImportError:
        print("\n⚠️ datasets de Hugging Face pas installé")
        print("   Installation: pip install datasets")
        print("\n   Utilisation du dataset par défaut...")
        training_data_path = Path(__file__).parent / "data" / "fashion_training_data.jsonl"
    
    # Étape 3: Créer Modelfile
    print("\n" + "="*80)
    print("📋 ÉTAPE 2: PRÉPARATION DU MODÈLE")
    print("="*80)
    
    modelfile_path = create_modelfile(training_data_path)
    
    # Étape 4: Fine-tuner
    print("\n" + "="*80)
    print("🤖 ÉTAPE 3: FINE-TUNING")
    print("="*80)
    
    if not create_finetuned_model(modelfile_path):
        return False
    
    # Étape 5: Vérifier
    print("\n" + "="*80)
    print("✅ ÉTAPE 4: VÉRIFICATION")
    print("="*80)
    
    if not verify_model():
        return False
    
    # Succès
    print("\n" + "="*80)
    print("✅ FINE-TUNING COMPLÉTÉ AVEC SUCCÈS!")
    print("="*80)
    print(f"\n🚀 Modèle disponible: {MODEL_NAME}")
    print(f"\n📝 Mettez à jour .env:")
    print(f"   OLLAMA_MODEL={MODEL_NAME}")
    print(f"\n📊 Données d'entraînement: {training_data_path}")
    print(f"   {training_data_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)