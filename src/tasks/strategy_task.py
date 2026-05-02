"""
Strategy Synthesis Task — Task 4

Defines the task for the Portfolio Strategist agent.
This is the final task in the sequential pipeline.
It receives context from all three previous tasks and
produces the final investment recommendation.
"""

from crewai import Task, Agent


def create_strategy_task(agent: Agent, ticker: str) -> Task:
    """
    Create the strategy synthesis task.

    This task instructs the Portfolio Strategist to combine all
    prior analyses into a comprehensive investment report with
    a clear Buy/Hold/Sell recommendation, then save it to a file.

    Args:
        agent: The Portfolio Strategist agent to assign this task to.
        ticker: The stock ticker symbol to analyze.

    Returns:
        A configured CrewAI Task instance.
    """
    return Task(
        description=(
            f"Synthesize all research and produce a final investment report for '{ticker}'.\n\n"
            f"You have received analyses from three specialist agents:\n"
            f"1. Technical Analysis — price trends, indicators, momentum\n"
            f"2. Sentiment Analysis — news sentiment and market perception\n"
            f"3. Fundamental Analysis — financial health and valuation\n\n"
            f"STEPS:\n"
            f"1. Review all three analyses carefully\n"
            f"2. Identify where the analyses agree and disagree\n"
            f"3. Weigh the evidence to form a final recommendation\n"
            f"4. Write a comprehensive report in Markdown format\n\n"
            f"REPORT STRUCTURE (use this exact Markdown structure):\n"
            f"## Executive Summary\n"
            f"Brief 2-3 sentence overview with the recommendation.\n\n"
            f"## Technical Analysis Summary\n"
            f"Key findings from the technical analyst.\n\n"
            f"## Sentiment Analysis Summary\n"
            f"Key findings from the sentiment analyst.\n\n"
            f"## Fundamental Analysis Summary\n"
            f"Key findings from the fundamental analyst.\n\n"
            f"## Investment Recommendation\n"
            f"**Recommendation:** BUY / HOLD / SELL\n"
            f"**Confidence Level:** High / Medium / Low\n"
            f"**Time Horizon:** Short-term / Medium-term / Long-term\n\n"
            f"## Risk Factors\n"
            f"Key risks to be aware of.\n\n"
            f"CONSTRAINTS:\n"
            f"- Your recommendation MUST be one of: BUY, HOLD, or SELL\n"
            f"- You MUST cite specific data points from each analysis\n"
            f"- Be balanced — acknowledge both bullish and bearish factors"
        ),
        expected_output=(
            "A comprehensive investment report saved to a file, containing:\n"
            "1. Executive summary with clear BUY/HOLD/SELL recommendation\n"
            "2. Technical analysis summary with key indicators cited\n"
            "3. Sentiment analysis summary with sentiment rating\n"
            "4. Fundamental analysis summary with key metrics\n"
            "5. Final recommendation with confidence level and time horizon\n"
            "6. Risk factors\n"
            "7. Confirmation that the report was saved to a file"
        ),
        agent=agent,
    )
