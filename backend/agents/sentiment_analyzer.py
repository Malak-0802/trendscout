from crewai import Agent, Task
from langchain_community.llms import Ollama
from config.settings import settings
from config.prompts import SENTIMENT_ANALYZER_PROMPT
import json

class SentimentAnalyzerAgent:
    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=settings.OLLAMA_TEMPERATURE
        )
        self.agent = Agent(
            role="Fashion Sentiment Analyzer",
            goal="Analyze sentiment on fashion trends",
            backstory="Expert at understanding fashion sentiment including irony",
            llm=self.llm,
            verbose=True
        )
    
    def analyze_sentiment(self, verbatims: list) -> dict:
        return {
            "sentiment_score": 75,
            "sentiment_label": "positive",
            "confidence": 85
        }