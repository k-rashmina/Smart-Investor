"""
Sentiment Analyst Agent — Student 2's Agent

A financial news sentiment specialist that analyzes recent
news headlines to gauge market sentiment for a stock.
This is the second agent in the sequential pipeline.
"""

from crewai import Agent, LLM
from src.tools.sentiment_tool import scrape_stock_news
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


def create_sentiment_analyst() -> Agent:
    """
    Create and return the Sentiment Analyst agent.

    This agent specializes in natural language processing of
    financial news, detecting bullish and bearish signals from
    headlines and market commentary.

    Returns:
        A configured CrewAI Agent instance with the news
        scraper tool bound.
    """
    llm = LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
    )

    return Agent(
        role="Financial News Sentiment Specialist",
        goal=(
            "Analyze recent news headlines and market commentary to determine "
            "the overall market sentiment (Bullish, Bearish, or Neutral) for "
            "the given stock, providing a confidence score and key drivers."
        ),
        backstory=(
            "You are an expert in natural language processing specialized in "
            "financial media analysis. You have spent a decade at a leading "
            "hedge fund analyzing news flow to predict short-term price movements. "
            "You can detect subtle sentiment shifts in headlines that most analysts "
            "miss. You always classify sentiment with a confidence percentage and "
            "cite specific headlines as evidence."
        ),
        tools=[scrape_stock_news],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
