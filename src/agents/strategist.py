"""
Portfolio Strategist Agent — Student 4's Agent

A chief investment strategist that synthesizes all research
(technical, sentiment, and fundamental) into a final actionable
investment recommendation. This is the final agent in the pipeline.
"""

from crewai import Agent, LLM
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


def create_strategist() -> Agent:
    """
    Create and return the Portfolio Strategist agent.

    This agent combines all prior analyses into a comprehensive
    investment recommendation with a clear Buy/Hold/Sell verdict,
    risk assessment, and confidence level.

    Returns:
        A configured CrewAI Agent instance with the report
        writer tool bound.
    """
    llm = LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
    )

    return Agent(
        role="Chief Investment Strategist",
        goal=(
            "Synthesize all research from the technical analyst, sentiment "
            "analyst, and fundamental analyst into a comprehensive, actionable "
            "investment report with a clear BUY, HOLD, or SELL recommendation."
        ),
        backstory=(
            "You are a senior portfolio manager at a leading asset management firm "
            "with 20+ years of experience managing multi-billion dollar portfolios. "
            "You excel at synthesizing diverse data sources — technical charts, "
            "market sentiment, and company financials — into clear, decisive "
            "investment recommendations. You always weigh risks against potential "
            "returns and provide a confidence level for your recommendations. "
            "Your reports are structured, professional, and actionable."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
