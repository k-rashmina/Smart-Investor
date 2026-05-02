"""
Smart Investor Swarm — Crew Orchestration

Defines the CrewAI Crew that orchestrates all 4 agents in a
sequential pipeline. Each agent's output is automatically passed
as context to the next agent, ensuring global state preservation.

Pipeline:
    Technical Analyst → Sentiment Analyst → Fundamental Analyst → Portfolio Strategist
"""

from crewai import Crew, Process

from src.agents.technical_analyst import create_technical_analyst
from src.agents.sentiment_analyst import create_sentiment_analyst
from src.agents.fundamental_analyst import create_fundamental_analyst
from src.agents.strategist import create_strategist

from src.tasks.technical_task import create_technical_task
from src.tasks.sentiment_task import create_sentiment_task
from src.tasks.fundamental_task import create_fundamental_task
from src.tasks.strategy_task import create_strategy_task

from src.utils.logger import get_logger

logger = get_logger("Crew:SmartInvestor")


def build_crew(ticker: str) -> Crew:
    """
    Build and return the Smart Investor Swarm crew.

    Creates all 4 agents and their corresponding tasks, then
    assembles them into a sequential CrewAI pipeline. Each task
    receives the output of all previous tasks as context.

    Args:
        ticker: The stock ticker symbol to analyze (e.g., 'AAPL').

    Returns:
        A configured CrewAI Crew ready to be kicked off.
    """
    logger.info(f"Building Smart Investor Swarm crew for ticker: {ticker}")

    # ─── Create Agents ───────────────────────────────────────────
    technical_analyst = create_technical_analyst()
    sentiment_analyst = create_sentiment_analyst()
    fundamental_analyst = create_fundamental_analyst()
    strategist = create_strategist()

    logger.info("All 4 agents created successfully")

    # ─── Create Tasks ────────────────────────────────────────────
    technical_task = create_technical_task(technical_analyst, ticker)
    sentiment_task = create_sentiment_task(sentiment_analyst, ticker)
    fundamental_task = create_fundamental_task(fundamental_analyst, ticker)
    strategy_task = create_strategy_task(strategist, ticker)

    # ─── Wire Context: each task receives prior outputs ──────────
    sentiment_task.context = [technical_task]
    fundamental_task.context = [technical_task, sentiment_task]
    strategy_task.context = [technical_task, sentiment_task, fundamental_task]

    logger.info("All 4 tasks created with context chain wired")

    # ─── Assemble Crew ───────────────────────────────────────────
    crew = Crew(
        agents=[
            technical_analyst,
            sentiment_analyst,
            fundamental_analyst,
            strategist,
        ],
        tasks=[
            technical_task,
            sentiment_task,
            fundamental_task,
            strategy_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    logger.info("Crew assembled — ready for kickoff")
    return crew
