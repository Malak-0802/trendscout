from crewai import Agent, Task
from langchain_community.llms import Ollama
from config.settings import settings
from config.prompts import TREND_PREDICTOR_PROMPT

class TrendPredictorAgent:
    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=settings.OLLAMA_TEMPERATURE
        )
        self.agent = Agent(
            role="Trend Predictor",
            goal="Predict trend adoption and lifespan",
            backstory="Expert at predicting fashion trends",
            llm=self.llm,
            verbose=True
        )
    
    def predict_trend(self, product: str, sentiment: float) -> dict:
        return {
            "verdict": "ADOPT",
            "lifespan_months": 12,
            "adoption_rate": 72
        }