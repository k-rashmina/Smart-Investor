"""
Technical Data Collector Agent — Student 1's Agent

A senior technical analyst agent that fetches and analyzes
historical stock price data and technical indicators.
This is the first agent in the sequential pipeline.
"""

from crewai import Agent, LLM
from src.tools.technical_tool import fetch_stock_technical_data
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


def create_technical_analyst() -> Agent:
    """
    Create and return the Technical Data Collector agent.

    This agent specializes in quantitative technical analysis,
    using price charts, moving averages, RSI, and MACD to
    identify trends and momentum signals.

    Returns:
        A configured CrewAI Agent instance with the technical
        analysis tool bound.
    """
    llm = LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
    )

    return Agent(
        role="Senior Technical Analyst",
        goal=(
            "Fetch and analyze historical stock price data and technical "
            "indicators to identify trends, momentum, and key support/resistance "
            "levels for the given stock ticker."
        ),
        backstory=(
            "You are a veteran quantitative analyst with 15+ years of experience "
            "at top Wall Street firms. You specialize in reading price charts and "
            "identifying trends through technical indicators like Moving Averages, "
            "RSI, and MACD. You are methodical, data-driven, and never make "
            "claims without supporting numerical evidence. Your analysis is always "
            "structured and precise."
        ),
        tools=[fetch_stock_technical_data],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
