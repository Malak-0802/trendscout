from crewai import Agent, Task
from langchain_community.llms import Ollama
from config.settings import settings
from config.prompts import REPORT_GENERATOR_PROMPT

class ReportGeneratorAgent:
    def __init__(self):
        self.llm = Ollama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.5
        )
        self.agent = Agent(
            role="Report Generator",
            goal="Generate professional fashion trend reports",
            backstory="Expert at writing trend analysis reports",
            llm=self.llm,
            verbose=True
        )
    
    def generate_report(self, product: str, analysis: dict) -> str:
        report = f"# Trend Analysis: {product}\n\n"
        report += f"**Sentiment**: {analysis.get('sentiment_score', 0)}/100\n"
        report += f"**Verdict**: {analysis.get('verdict', 'MONITOR')}\n"
        return report