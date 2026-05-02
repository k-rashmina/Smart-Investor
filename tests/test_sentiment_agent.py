"""
Sentiment Analyst Agent — Evaluation Tests (Student 2)

Uses property-based testing and LLM-as-a-Judge to validate that
the Sentiment Analyst agent produces accurate sentiment assessments
from news data without fabricating headlines.
"""

import pytest
from src.tools.sentiment_tool import scrape_stock_news


class TestSentimentTool:
    """Property-based tests for the Sentiment Scraper tool."""

    def test_valid_ticker_returns_data(self) -> None:
        """Test that a valid ticker returns news or fallback data."""
        result: str = scrape_stock_news.run(ticker="AAPL")
        # Should return either headlines or fallback instructions
        assert "NEWS" in result.upper() or "SENTIMENT" in result.upper()

    def test_invalid_ticker_returns_fallback(self) -> None:
        """Test that an invalid ticker gracefully returns fallback."""
        result: str = scrape_stock_news.run(ticker="INVALIDTICKER999")
        # Should not crash — should return fallback
        assert isinstance(result, str)
        assert len(result) > 0

    def test_output_contains_sentiment_instructions(self) -> None:
        """Test that output includes instructions for sentiment classification."""
        result: str = scrape_stock_news.run(ticker="MSFT")
        # Either real headlines or fallback should guide the agent
        has_guidance: bool = (
            "BULLISH" in result
            or "BEARISH" in result
            or "NEUTRAL" in result
            or "SENTIMENT" in result.upper()
        )
        assert has_guidance, "Output should contain sentiment guidance"


class TestSentimentAgentWithJudge:
    """LLM-as-a-Judge evaluation for the Sentiment Analyst agent."""

    def test_llm_judges_sentiment_output(self, llm_judge) -> None:
        """
        Use the LLM as a judge to evaluate the quality and
        structure of the sentiment analysis output.
        """
        tool_output: str = scrape_stock_news.run(ticker="AAPL")

        judge_prompt: str = f"""
You are an expert evaluator of data retrieval tools used for financial sentiment analysis.
    
Evaluate the following raw tool output and answer with ONLY 'PASS' or 'FAIL' followed by a brief reason.

Ensure you evaluate strictly against the criteria below. This is raw data intended for an AI agent, not a final report.
    
Criteria for PASS:
1. Contains news headlines OR a valid fallback explanation
2. Provides guidance for sentiment classification
3. Mentions BULLISH, BEARISH, or NEUTRAL as possible outcomes
4. Is relevant to stock market analysis
5. Does not contain obviously fabricated or nonsensical content

OUTPUT TO EVALUATE:
{tool_output}

Your verdict (PASS or FAIL):
"""
        response: str = llm_judge.call(messages=[{"role": "user", "content": judge_prompt}])
        assert "PASS" in response.upper(), f"LLM Judge failed: {response}"
