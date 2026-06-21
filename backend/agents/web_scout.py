from crewai import Agent, Task
from langchain_community.llms import Ollama
from config.settings import settings
from config.prompts import WEB_SCOUT_PROMPT

class WebScoutAgent:
    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=settings.OLLAMA_TEMPERATURE
        )
        self.agent = Agent(
            role="Fashion Web Scout",
            goal="Scrape web data on fashion trends",
            backstory="Expert at finding fashion trends on the web",
            llm=self.llm,
            verbose=True
        )
    
    def scout_trend(self, product_name: str) -> dict:
        return {"product": product_name, "status": "scouting"}