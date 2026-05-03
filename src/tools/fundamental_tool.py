"""
Fundamental Analysis Tool — Student 3's Custom Tool

Fetches key fundamental financial metrics for a given stock ticker
using yfinance. The Fundamental Analyst agent uses this data to
evaluate the financial health and valuation of a company.

Metrics retrieved:
    - Market Capitalization
    - P/E Ratio (Trailing & Forward)
    - Earnings Per Share (EPS)
    - Revenue & Revenue Growth
    - Profit Margins
    - Debt-to-Equity Ratio
    - Free Cash Flow
    - Return on Equity (ROE)
    - Dividend Yield
"""

from crewai.tools import tool
from typing import Any, Optional
import yfinance as yf
from src.utils.logger import get_logger, log_tool_call

logger = get_logger("Tool:FundamentalData")


def _safe_get(info: dict[str, Any], key: str, default: str = "N/A") -> Any:
    """
    Safely retrieve a value from the stock info dictionary.

    Args:
        info: The yfinance stock info dictionary.
        key: The key to look up.
        default: Default value if key is missing. Defaults to 'N/A'.

    Returns:
        The value associated with the key, or the default value.
    """
    value: Any = info.get(key)
    return value if value is not None else default


def _format_large_number(value: Any) -> str:
    """
    Format a large number into a human-readable string (e.g., 2.5T, 150B, 3.2M).

    Args:
        value: The numeric value to format.

    Returns:
        A formatted string with appropriate suffix (T/B/M/K).
    """
    if value == "N/A" or value is None:
        return "N/A"

    try:
        num: float = float(value)
        if abs(num) >= 1e12:
            return f"${num / 1e12:.2f}T"
        elif abs(num) >= 1e9:
            return f"${num / 1e9:.2f}B"
        elif abs(num) >= 1e6:
            return f"${num / 1e6:.2f}M"
        elif abs(num) >= 1e3:
            return f"${num / 1e3:.2f}K"
        else:
            return f"${num:.2f}"
    except (ValueError, TypeError):
        return "N/A"


def _format_percentage(value: Any) -> str:
    """
    Format a decimal value as a percentage string.

    Args:
        value: The decimal value (e.g., 0.25 for 25%).

    Returns:
        A formatted percentage string (e.g., '25.00%').
    """
    if value == "N/A" or value is None:
        return "N/A"

    try:
        return f"{float(value) * 100:.2f}%"
    except (ValueError, TypeError):
        return "N/A"


@tool("Fetch Fundamental Financial Data")
def fetch_fundamental_data(ticker: str) -> str:
    """
    Fetch key fundamental financial metrics for a stock from Yahoo Finance.

    Retrieves comprehensive financial data including valuation metrics
    (P/E, P/B), profitability metrics (margins, ROE), growth metrics
    (revenue growth), and financial health indicators (debt-to-equity,
    free cash flow).

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT').

    Returns:
        A formatted string containing all fundamental analysis data,
        or an error message if the ticker is invalid.
    """
    ticker = ticker.strip().upper()
    logger.info(f"Fetching fundamental data for ticker: {ticker}")

    try:
        stock: yf.Ticker = yf.Ticker(ticker)
        info: dict[str, Any] = stock.info

        if not info or info.get("regularMarketPrice") is None:
            error_msg: str = (
                f"No fundamental data found for ticker '{ticker}'. "
                "Please verify the symbol."
            )
            logger.error(error_msg)
            return error_msg

        # ─── Extract Metrics ─────────────────────────────────────
        company_name: str = _safe_get(info, "longName", ticker)
        sector: str = _safe_get(info, "sector")
        industry: str = _safe_get(info, "industry")

        market_cap: str = _format_large_number(_safe_get(info, "marketCap"))
        enterprise_value: str = _format_large_number(_safe_get(info, "enterpriseValue"))

        pe_trailing: Any = _safe_get(info, "trailingPE")
        pe_forward: Any = _safe_get(info, "forwardPE")
        pb_ratio: Any = _safe_get(info, "priceToBook")
        peg_ratio: Any = _safe_get(info, "pegRatio")

        eps_trailing: Any = _safe_get(info, "trailingEps")
        eps_forward: Any = _safe_get(info, "forwardEps")

        revenue: str = _format_large_number(_safe_get(info, "totalRevenue"))
        revenue_growth: str = _format_percentage(_safe_get(info, "revenueGrowth"))
        earnings_growth: str = _format_percentage(_safe_get(info, "earningsGrowth"))

        gross_margin: str = _format_percentage(_safe_get(info, "grossMargins"))
        operating_margin: str = _format_percentage(_safe_get(info, "operatingMargins"))
        profit_margin: str = _format_percentage(_safe_get(info, "profitMargins"))

        debt_to_equity: Any = _safe_get(info, "debtToEquity")
        current_ratio: Any = _safe_get(info, "currentRatio")
        free_cash_flow: str = _format_large_number(_safe_get(info, "freeCashflow"))

        roe: str = _format_percentage(_safe_get(info, "returnOnEquity"))
        roa: str = _format_percentage(_safe_get(info, "returnOnAssets"))

        dividend_yield: str = _format_percentage(_safe_get(info, "dividendYield"))
        payout_ratio: str = _format_percentage(_safe_get(info, "payoutRatio"))

        # ─── Format Output ───────────────────────────────────────
        result: str = f"""
=== FUNDAMENTAL ANALYSIS DATA FOR {ticker} ===

COMPANY OVERVIEW:
  - Name: {company_name}
  - Sector: {sector}
  - Industry: {industry}
  - Market Cap: {market_cap}
  - Enterprise Value: {enterprise_value}

VALUATION METRICS:
  - P/E Ratio (Trailing): {pe_trailing}
  - P/E Ratio (Forward): {pe_forward}
  - Price-to-Book (P/B): {pb_ratio}
  - PEG Ratio: {peg_ratio}

EARNINGS:
  - EPS (Trailing): ${eps_trailing}
  - EPS (Forward): ${eps_forward}
  - Earnings Growth: {earnings_growth}

REVENUE & GROWTH:
  - Total Revenue: {revenue}
  - Revenue Growth (YoY): {revenue_growth}

PROFITABILITY:
  - Gross Margin: {gross_margin}
  - Operating Margin: {operating_margin}
  - Net Profit Margin: {profit_margin}
  - Return on Equity (ROE): {roe}
  - Return on Assets (ROA): {roa}

FINANCIAL HEALTH:
  - Debt-to-Equity Ratio: {debt_to_equity}
  - Current Ratio: {current_ratio}
  - Free Cash Flow: {free_cash_flow}

DIVIDENDS:
  - Dividend Yield: {dividend_yield}
  - Payout Ratio: {payout_ratio}

INSTRUCTIONS FOR FUNDAMENTAL ANALYSIS:
Evaluate the company's financial health based on:
1. Valuation: Is the stock overvalued/undervalued vs peers?
2. Growth: Are revenue and earnings growing?
3. Profitability: Are margins healthy and improving?
4. Financial Health: Is the debt manageable?
5. Shareholder Returns: Is the dividend sustainable?
"""

        log_tool_call(logger, "fetch_fundamental_data", {"ticker": ticker}, result)
        return result

    except Exception as e:
        error_msg = f"Error fetching fundamental data for '{ticker}': {str(e)}"
        logger.error(error_msg)
        return error_msg
