"""
Fundamental Analysis Task — Task 3

Defines the task for the Fundamental Analyst agent.
This is the third task in the sequential pipeline.
It receives context from both previous tasks.
"""

from crewai import Task, Agent


def create_fundamental_task(agent: Agent, ticker: str) -> Task:
    """
    Create the fundamental analysis task.

    This task instructs the Fundamental Analyst to fetch and
    evaluate key financial metrics for the given company,
    assessing its valuation, profitability, and financial health.

    Args:
        agent: The Fundamental Analyst agent to assign this task to.
        ticker: The stock ticker symbol to analyze.

    Returns:
        A configured CrewAI Task instance.
    """
    return Task(
        description=(
            f"Analyze the fundamental financial data for stock '{ticker}'.\n\n"
            f"STEPS:\n"
            f"1. Use your 'Fetch Fundamental Financial Data' tool with ticker '{ticker}'\n"
            f"2. Evaluate the valuation metrics (P/E, P/B, PEG ratios)\n"
            f"3. Assess profitability (margins, ROE, ROA)\n"
            f"4. Analyze financial health (debt-to-equity, current ratio, free cash flow)\n"
            f"5. Review growth metrics (revenue growth, earnings growth)\n"
            f"6. Consider the findings from technical and sentiment analysis\n\n"
            f"CONSTRAINTS:\n"
            f"- Only use data returned by your tool — do not fabricate numbers\n"
            f"- Compare metrics against typical benchmarks where possible\n"
            f"- Identify both strengths and weaknesses\n"
            f"- Provide a clear STRONG/MODERATE/WEAK fundamental rating"
        ),
        expected_output=(
            "A structured fundamental analysis report containing:\n"
            "1. Company overview (sector, market cap)\n"
            "2. Valuation assessment (overvalued/fairly valued/undervalued)\n"
            "3. Profitability analysis with specific margin figures\n"
            "4. Financial health assessment\n"
            "5. Growth outlook\n"
            "6. Overall Fundamental Rating: STRONG / MODERATE / WEAK"
        ),
        agent=agent,
    )
