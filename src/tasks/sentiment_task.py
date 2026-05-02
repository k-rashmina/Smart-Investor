"""
Sentiment Analysis Task — Task 2

Defines the task for the Sentiment Analyst agent.
This is the second task in the sequential pipeline.
It receives context from the Technical Analysis task.
"""

from crewai import Task, Agent


def create_sentiment_task(agent: Agent, ticker: str) -> Task:
    """
    Create the sentiment analysis task.

    This task instructs the Sentiment Analyst to scrape and
    analyze recent news headlines for the given stock ticker,
    producing a sentiment assessment with confidence score.

    Args:
        agent: The Sentiment Analyst agent to assign this task to.
        ticker: The stock ticker symbol to analyze.

    Returns:
        A configured CrewAI Task instance.
    """
    return Task(
        description=(
            f"Analyze the market sentiment for stock '{ticker}'.\n\n"
            f"STEPS:\n"
            f"1. Use your 'Scrape Stock News Headlines' tool with ticker '{ticker}'\n"
            f"2. Analyze each headline for positive, negative, or neutral sentiment\n"
            f"3. Identify the dominant sentiment across all headlines\n"
            f"4. Note any particularly impactful news (earnings, lawsuits, product launches)\n"
            f"5. Assign a confidence score (0-100%) to your assessment\n\n"
            f"CONSTRAINTS:\n"
            f"- Cite specific headlines as evidence for your sentiment assessment\n"
            f"- Consider the technical analysis context from the previous agent\n"
            f"- If news scraping fails, use your general knowledge but note this clearly\n"
            f"- Always provide a quantified confidence score"
        ),
        expected_output=(
            "A structured sentiment analysis report containing:\n"
            "1. Overall Sentiment: BULLISH / BEARISH / NEUTRAL\n"
            "2. Confidence Score: X%\n"
            "3. Key bullish headlines/factors (if any)\n"
            "4. Key bearish headlines/factors (if any)\n"
            "5. Notable news events affecting the stock\n"
            "6. How sentiment aligns with or diverges from technical analysis"
        ),
        agent=agent,
    )
