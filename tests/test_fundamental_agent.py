"""
Fundamental Analyst Agent — Evaluation Tests (Student 3)

Uses property-based testing and LLM-as-a-Judge to validate that
the Fundamental Analyst agent produces accurate financial metrics
from real company data without hallucination.
"""

import pytest
from src.tools.fundamental_tool import fetch_fundamental_data


class TestFundamentalTool:
    """Property-based tests for the Fundamental Data tool."""

    def test_valid_ticker_returns_data(self) -> None:
        """Test that a valid ticker returns fundamental data."""
        result: str = fetch_fundamental_data.run(ticker="AAPL")
        assert "FUNDAMENTAL ANALYSIS DATA" in result
        assert "VALUATION METRICS" in result
        assert "P/E Ratio" in result

    def test_invalid_ticker_returns_error(self) -> None:
        """Test that an invalid ticker returns a meaningful error."""
        result: str = fetch_fundamental_data.run(ticker="INVALIDTICKER123")
        assert "error" in result.lower() or "no fundamental data" in result.lower()

    def test_output_contains_all_sections(self) -> None:
        """Test that all required fundamental sections are present."""
        result: str = fetch_fundamental_data.run(ticker="MSFT")
        required_sections: list[str] = [
            "COMPANY OVERVIEW",
            "VALUATION METRICS",
            "EARNINGS",
            "REVENUE & GROWTH",
            "PROFITABILITY",
            "FINANCIAL HEALTH",
        ]
        for section in required_sections:
            assert section in result, f"Missing section: {section}"

    def test_market_cap_is_formatted(self) -> None:
        """Test that market cap is formatted with dollar sign and suffix."""
        result: str = fetch_fundamental_data.run(ticker="AAPL")
        # Apple's market cap should contain T (trillion) or B (billion)
        assert "$" in result, "Market cap should be dollar-formatted"


class TestFundamentalAgentWithJudge:
    """LLM-as-a-Judge evaluation for the Fundamental Analyst agent."""

    def test_llm_judges_fundamental_output(self, llm_judge) -> None:
        """
        Use the LLM as a judge to evaluate the accuracy and
        completeness of the fundamental analysis output.
        """
        tool_output: str = fetch_fundamental_data.run(ticker="AAPL")

        judge_prompt: str = f"""
You are an expert evaluator of financial fundamental analysis reports.

Evaluate the following Fundamental Analysis output and answer with ONLY
'PASS' or 'FAIL' followed by a brief reason.

Criteria for PASS:
1. Contains real company name and sector information
2. Includes P/E ratio (a reasonable number, not N/A for a major company)
3. Includes revenue figures with proper formatting (e.g., $XXB)
4. Includes profit margin percentages
5. Includes debt-to-equity and cash flow information
6. Data appears reasonable for a real publicly traded company

OUTPUT TO EVALUATE:
{tool_output}

Your verdict (PASS or FAIL):
"""
        response: str = llm_judge.call(messages=[{"role": "user", "content": judge_prompt}])
        assert "PASS" in response.upper(), f"LLM Judge failed: {response}"
