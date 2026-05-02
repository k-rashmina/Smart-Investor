"""
Sentiment Analysis Tool — Student 2's Custom Tool

Scrapes recent financial news headlines for a given stock ticker
using free public sources (Finviz). The Sentiment Analyst agent
uses this data to gauge market sentiment.

This tool uses requests + BeautifulSoup (no paid APIs required).
"""

from crewai.tools import tool
from typing import Any
import requests
from bs4 import BeautifulSoup
from src.utils.logger import get_logger, log_tool_call

logger = get_logger("Tool:SentimentScraper")

# ─── Constants ───────────────────────────────────────────────────────
FINVIZ_URL: str = "https://finviz.com/quote.ashx"
USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
MAX_HEADLINES: int = 20


@tool("Scrape Stock News Headlines")
def scrape_stock_news(ticker: str) -> str:
    """
    Scrape recent financial news headlines for a stock from Finviz.

    Retrieves up to 20 of the most recent news headlines along with
    their source and timestamp. This data is used by the Sentiment
    Analyst agent to determine overall market sentiment.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT').

    Returns:
        A formatted string containing numbered headlines with sources
        and timestamps, or an error message if scraping fails.
    """
    ticker = ticker.strip().upper()
    logger.info(f"Scraping news headlines for ticker: {ticker}")

    try:
        headers: dict[str, str] = {"User-Agent": USER_AGENT}
        params: dict[str, str] = {"t": ticker, "ty": "c", "p": "d", "b": "1"}

        response: requests.Response = requests.get(
            FINVIZ_URL,
            headers=headers,
            params=params,
            timeout=15,
        )
        response.raise_for_status()

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        # ─── Find the news table ─────────────────────────────────
        news_table = soup.find("table", {"id": "news-table"})

        if news_table is None:
            # Fallback: try to find news in alternative structure
            fallback_msg: str = _generate_fallback_news(ticker)
            logger.warning(f"News table not found for {ticker}, using fallback")
            return fallback_msg

        headlines: list[dict[str, str]] = []
        current_date: str = ""

        rows = news_table.find_all("tr")
        for row in rows[:MAX_HEADLINES]:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue

            # Parse timestamp
            timestamp_text: str = cells[0].get_text(strip=True)
            if len(timestamp_text) > 10:
                # Contains date and time
                current_date = timestamp_text
            else:
                # Only time, use last known date
                timestamp_text = f"{current_date.split(' ')[0] if current_date else 'Today'} {timestamp_text}"

            # Parse headline and source
            link_tag = cells[1].find("a")
            if link_tag:
                headline_text: str = link_tag.get_text(strip=True)
                source_tag = cells[1].find("span")
                source: str = source_tag.get_text(strip=True) if source_tag else "Unknown"

                headlines.append({
                    "timestamp": timestamp_text,
                    "headline": headline_text,
                    "source": source,
                })

        if not headlines:
            fallback_msg = _generate_fallback_news(ticker)
            logger.warning(f"No headlines parsed for {ticker}, using fallback")
            return fallback_msg

        # ─── Format output ───────────────────────────────────────
        result: str = f"\n=== RECENT NEWS HEADLINES FOR {ticker} ===\n\n"
        result += f"Total Headlines Found: {len(headlines)}\n\n"

        for i, item in enumerate(headlines, 1):
            result += (
                f"{i}. [{item['timestamp']}] {item['headline']}\n"
                f"   Source: {item['source']}\n\n"
            )

        result += (
            "\nINSTRUCTIONS FOR SENTIMENT ANALYSIS:\n"
            "Analyze each headline and classify overall sentiment as:\n"
            "- BULLISH: Majority of headlines suggest positive outlook\n"
            "- BEARISH: Majority of headlines suggest negative outlook\n"
            "- NEUTRAL: Mixed signals or no clear direction\n"
            "Provide a confidence score (0-100%) for your assessment.\n"
        )

        log_tool_call(logger, "scrape_stock_news", {"ticker": ticker}, result)
        return result

    except requests.exceptions.RequestException as e:
        logger.warning(f"Network error scraping news for {ticker}: {e}")
        return _generate_fallback_news(ticker)
    except Exception as e:
        error_msg: str = f"Error scraping news for '{ticker}': {str(e)}"
        logger.error(error_msg)
        return _generate_fallback_news(ticker)


def _generate_fallback_news(ticker: str) -> str:
    """
    Generate a fallback prompt when news scraping is unavailable.

    This ensures the agent can still perform sentiment analysis
    using its internal knowledge of the company.

    Args:
        ticker: The stock ticker symbol.

    Returns:
        A formatted string instructing the agent to use general knowledge.
    """
    return f"""
=== NEWS DATA FOR {ticker} ===

NOTE: Live news headlines could not be retrieved at this time.
This may be due to network restrictions or website rate limiting.

FALLBACK INSTRUCTIONS:
As the Sentiment Analyst, please provide your sentiment analysis based on:
1. Your general knowledge of {ticker} and its recent market performance
2. Known industry trends affecting this company
3. Any widely-reported news events about this company

Please still provide:
- Overall Sentiment: BULLISH / BEARISH / NEUTRAL
- Confidence Score: (0-100%)
- Key factors influencing your sentiment assessment
- At least 3 relevant observations about the company's market perception
"""
