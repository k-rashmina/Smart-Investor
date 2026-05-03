"""
Fundamental Analyst Agent — Student 3's Agent

A corporate fundamentals expert that evaluates the financial
health of a company using key fundamental metrics.
This is the third agent in the sequential pipeline.
"""

from crewai import Agent, LLM
from src.tools.fundamental_tool import fetch_fundamental_data
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


def create_fundamental_analyst() -> Agent:
    """
    Create and return the Fundamental Analyst agent.

    This agent specializes in balance sheet analysis, valuation
    metrics, profitability assessment, and growth projections
    for publicly traded companies.

    Returns:
        A configured CrewAI Agent instance with the fundamentals
        data tool bound.
    """
    llm = LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
    )

    return Agent(
        role="Corporate Fundamentals Expert",
        goal=(
            "Evaluate the financial health and intrinsic value of the company "
            "by analyzing key fundamental metrics including valuation ratios, "
            "profitability margins, growth rates, and balance sheet strength."
        ),
        backstory=(
            "You are a CFA charterholder with 12+ years of experience in equity "
            "research at a top investment bank. You specialize in fundamental "
            "analysis — reading balance sheets, income statements, and cash flow "
            "statements to assess a company's true worth. You compare metrics "
            "against industry benchmarks and historical averages. Your analysis "
            "is thorough, unbiased, and always backed by specific numbers."
        ),
        tools=[fetch_fundamental_data],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
