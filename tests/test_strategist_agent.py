"""
Portfolio Strategist Agent — Evaluation Tests (Student 4)

Uses property-based testing and LLM-as-a-Judge to validate that
the Portfolio Strategist agent produces well-structured investment
reports with clear, justified recommendations.
"""

import pytest
from pathlib import Path
from src.tools.report_tool import write_report_to_file
from src.config import REPORTS_DIR


class TestReportTool:
    """Property-based tests for the Report Writer tool."""

    def test_writes_report_file(self) -> None:
        """Test that the tool successfully writes a Markdown file."""
        sample_report: str = (
            "## Executive Summary\n"
            "This is a test report.\n\n"
            "## Recommendation\n"
            "**BUY** with high confidence."
        )
        result: str = write_report_to_file.run(
            ticker="TEST",
            report_content=sample_report,
        )
        assert "successfully saved" in result.lower() or "✅" in result

    def test_report_file_exists_after_write(self) -> None:
        """Test that the report file exists on disk after writing."""
        sample_report: str = "## Test\nThis is a test."
        write_report_to_file.run(ticker="TESTEXIST", report_content=sample_report)

        # Check that at least one TESTEXIST report exists
        reports: list[Path] = list(REPORTS_DIR.glob("TESTEXIST_*.md"))
        assert len(reports) > 0, "Report file should exist on disk"

        # Clean up test files
        for report in reports:
            report.unlink()

    def test_report_contains_header(self) -> None:
        """Test that the written report contains the standard header."""
        sample_report: str = "## Test Content\nSample analysis."
        write_report_to_file.run(ticker="TESTHDR", report_content=sample_report)

        reports: list[Path] = list(REPORTS_DIR.glob("TESTHDR_*.md"))
        assert len(reports) > 0

        content: str = reports[0].read_text(encoding="utf-8")
        assert "Investment Research Report" in content
        assert "Smart Investor Swarm" in content
        assert "Disclaimer" in content

        # Clean up
        for report in reports:
            report.unlink()


class TestStrategistAgentWithJudge:
    """LLM-as-a-Judge evaluation for the Portfolio Strategist agent."""

    def test_llm_judges_report_quality(self, llm_judge) -> None:
        """
        Use the LLM as a judge to evaluate a sample synthesized
        investment report for quality and completeness.
        """
        sample_report: str = """
## Executive Summary
Based on comprehensive analysis, AAPL shows strong technical momentum
with bullish moving averages, positive market sentiment, and solid
fundamentals. Recommendation: BUY.

## Technical Analysis Summary
- Current Price: $195.50
- SMA 20 ($192.30) above SMA 50 ($188.75) = BULLISH
- RSI at 62 = Neutral zone, room to grow
- MACD histogram positive = Bullish momentum

## Sentiment Analysis Summary
- Overall Sentiment: BULLISH (75% confidence)
- Positive headlines around new product launches
- No significant negative news events

## Fundamental Analysis Summary
- P/E Ratio: 28.5 (slightly above sector average)
- Revenue Growth: 8.2% YoY
- Net Profit Margin: 25.3%
- Free Cash Flow: $105B
- Debt-to-Equity: 1.52 (manageable)

## Investment Recommendation
**Recommendation:** BUY
**Confidence Level:** High
**Time Horizon:** Medium-term (6-12 months)

## Risk Factors
1. Global economic slowdown could impact consumer spending
2. Regulatory risks in international markets
3. High valuation relative to sector peers
"""

        judge_prompt: str = f"""
You are an expert evaluator of investment research reports.

Evaluate the following Investment Report and answer with ONLY
'PASS' or 'FAIL' followed by a brief reason.

Criteria for PASS:
1. Contains an Executive Summary with a clear recommendation
2. Includes Technical Analysis with specific indicator values
3. Includes Sentiment Analysis with sentiment direction
4. Includes Fundamental Analysis with financial metrics
5. Has a clear BUY/HOLD/SELL recommendation
6. Lists risk factors
7. The recommendation is justified by the analysis sections

REPORT TO EVALUATE:
{sample_report}

Your verdict (PASS or FAIL):
"""
        response: str = llm_judge.call(messages=[{"role": "user", "content": judge_prompt}])
        assert "PASS" in response.upper(), f"LLM Judge failed: {response}"
