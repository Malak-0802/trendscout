from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Ollama Config
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2:13b"
    OLLAMA_TEMPERATURE: float = 0.7
    
    # API Config
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"
    API_DEBUG: bool = True
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    
    # Scraping
    SCRAPER_TIMEOUT: int = 10
    SCRAPER_RETRY: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()