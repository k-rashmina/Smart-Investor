"""
Technical Analyst Agent — Evaluation Tests (Student 1)

Uses property-based testing and LLM-as-a-Judge to validate that
the Technical Analyst agent produces accurate, well-structured
technical analysis output without hallucination.
"""

import pytest
from src.tools.technical_tool import fetch_stock_technical_data


class TestTechnicalTool:
    """Property-based tests for the Technical Analysis tool."""

    def test_valid_ticker_returns_data(self) -> None:
        """Test that a valid ticker returns technical analysis data."""
        result: str = fetch_stock_technical_data.run(ticker="AAPL")
        assert "TECHNICAL ANALYSIS DATA" in result
        assert "CURRENT PRICE" in result
        assert "SMA 20" in result
        assert "RSI" in result
        assert "MACD" in result

    def test_invalid_ticker_returns_error(self) -> None:
        """Test that an invalid ticker returns a meaningful error."""
        result: str = fetch_stock_technical_data.run(ticker="INVALIDTICKER123")
        assert "error" in result.lower() or "no data" in result.lower()

    def test_output_contains_all_indicators(self) -> None:
        """Test that all required technical indicators are present."""
        result: str = fetch_stock_technical_data.run(ticker="MSFT")
        required_sections: list[str] = [
            "MOVING AVERAGES",
            "RSI",
            "MACD",
            "VOLUME",
            "PRICE RANGE",
            "PRICE CHANGES",
        ]
        for section in required_sections:
            assert section in result, f"Missing section: {section}"

    def test_output_contains_numerical_values(self) -> None:
        """Test that the output contains actual numbers, not placeholders."""
        result: str = fetch_stock_technical_data.run(ticker="GOOGL")
        assert "$" in result, "Output should contain dollar-formatted prices"


class TestTechnicalAgentWithJudge:
    """LLM-as-a-Judge evaluation for the Technical Analyst agent."""

    def test_llm_judges_output_quality(self, llm_judge) -> None:
        """
        Use the LLM as a judge to evaluate the quality of
        the technical analysis output.
        """
        # Get the tool output
        tool_output: str = fetch_stock_technical_data.run(ticker="AAPL")

        # Ask the LLM to judge the output
        judge_prompt: str = f"""
You are an expert evaluator of financial analysis reports.

Evaluate the following Technical Analysis output and answer with ONLY
'PASS' or 'FAIL' followed by a brief reason.

CRITICAL: Evaluate STRICTLY based on the Criteria for PASS listed below. 
Do NOT invent new criteria, and do NOT fail the output for missing metrics not explicitly mentioned here.
Note: For MACD data, having 'Histogram' or 'MACD Line' or any MACD components is sufficient.

Criteria for PASS:
1. Contains actual numerical price data (not placeholders)
2. Includes moving average values (SMA 20, SMA 50)
3. Includes RSI value between 0 and 100
4. Includes MACD data (e.g., MACD Line, Signal Line, Histogram)
5. Provides a clear trend signal (BULLISH or BEARISH)

OUTPUT TO EVALUATE:
{tool_output}

Your verdict (PASS or FAIL):
"""
        response: str = llm_judge.call(messages=[{"role": "user", "content": judge_prompt}])
        assert "PASS" in response.upper(), f"LLM Judge failed: {response}"
