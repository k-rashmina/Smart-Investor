"""
Technical Analysis Task — Task 1

Defines the task for the Technical Data Collector agent.
This is the first task in the sequential pipeline.
"""

from crewai import Task, Agent


def create_technical_task(agent: Agent, ticker: str) -> Task:
    """
    Create the technical analysis task.

    This task instructs the Technical Data Collector to fetch
    stock price data and compute technical indicators, then
    produce a structured analysis summary.

    Args:
        agent: The Technical Analyst agent to assign this task to.
        ticker: The stock ticker symbol to analyze.

    Returns:
        A configured CrewAI Task instance.
    """
    return Task(
        description=(
            f"Analyze the stock '{ticker}' from a technical perspective.\n\n"
            f"STEPS:\n"
            f"1. Use your 'Fetch Stock Technical Data' tool with ticker '{ticker}'\n"
            f"2. Analyze the returned data including SMA, RSI, MACD, and volume\n"
            f"3. Identify the current trend (bullish/bearish)\n"
            f"4. Note any key support/resistance levels\n"
            f"5. Provide a clear technical outlook\n\n"
            f"CONSTRAINTS:\n"
            f"- Only use data returned by your tool — do not fabricate numbers\n"
            f"- All claims must reference specific indicator values\n"
            f"- Provide a clear BULLISH/BEARISH/NEUTRAL technical verdict"
        ),
        expected_output=(
            "A structured technical analysis report containing:\n"
            "1. Current price and trend direction\n"
            "2. Moving average analysis (SMA 20 vs SMA 50)\n"
            "3. RSI reading and interpretation\n"
            "4. MACD signal interpretation\n"
            "5. Volume trend analysis\n"
            "6. Overall Technical Verdict: BULLISH / BEARISH / NEUTRAL"
        ),
        agent=agent,
    )
