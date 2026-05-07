"""
Technical Analysis Tool — Student 1's Custom Tool

Fetches historical stock price data and computes key technical indicators
using the yfinance library. This tool provides the Technical Data Collector
agent with quantitative market data for analysis.

Indicators computed:
    - Simple Moving Averages (SMA 20, SMA 50)
    - Relative Strength Index (RSI 14-period)
    - MACD (12, 26, 9)
    - Average Daily Volume
    - 52-week High/Low
    - Price change percentages (1-week, 1-month, 3-month)
"""

from crewai.tools import tool
from typing import Any
import yfinance as yf
import pandas as pd
from src.utils.logger import get_logger, log_tool_call

logger = get_logger("Tool:TechnicalData")


def _compute_rsi(series: pd.Series, period: int = 14) -> float:
    """
    Compute the Relative Strength Index (RSI) for a price series.

    The RSI measures the speed and magnitude of recent price changes
    to evaluate overbought or oversold conditions.

    Args:
        series: A pandas Series of closing prices.
        period: The lookback period for RSI calculation. Defaults to 14.

    Returns:
        The RSI value as a float between 0 and 100.
        Returns 50.0 if insufficient data is available.
    """
    if len(series) < period + 1:
        return 50.0

    delta: pd.Series = series.diff()
    gain: pd.Series = delta.where(delta > 0, 0.0)
    loss: pd.Series = (-delta).where(delta < 0, 0.0)

    avg_gain: float = gain.rolling(window=period, min_periods=period).mean().iloc[-1]
    avg_loss: float = loss.rolling(window=period, min_periods=period).mean().iloc[-1]

    if avg_loss == 0:
        return 100.0

    rs: float = avg_gain / avg_loss
    rsi: float = 100.0 - (100.0 / (1.0 + rs))
    return round(rsi, 2)


def _compute_macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> dict[str, float]:
    """
    Compute the MACD (Moving Average Convergence Divergence) indicator.

    Args:
        series: A pandas Series of closing prices.
        fast: Fast EMA period. Defaults to 12.
        slow: Slow EMA period. Defaults to 26.
        signal: Signal line EMA period. Defaults to 9.

    Returns:
        A dictionary with keys 'macd_line', 'signal_line', and 'histogram'.
    """
    if len(series) < slow + signal:
        return {"macd_line": 0.0, "signal_line": 0.0, "histogram": 0.0}

    ema_fast: pd.Series = series.ewm(span=fast, adjust=False).mean()
    ema_slow: pd.Series = series.ewm(span=slow, adjust=False).mean()
    macd_line: pd.Series = ema_fast - ema_slow
    signal_line: pd.Series = macd_line.ewm(span=signal, adjust=False).mean()
    histogram: pd.Series = macd_line - signal_line

    return {
        "macd_line": round(float(macd_line.iloc[-1]), 4),
        "signal_line": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(float(histogram.iloc[-1]), 4),
    }


@tool("Fetch Stock Technical Data")
def fetch_stock_technical_data(ticker: str) -> str:
    """
    Fetch 6 months of historical stock data and compute technical indicators.

    This tool retrieves price history from Yahoo Finance and calculates
    SMA (20/50), RSI (14), MACD (12,26,9), volume trends, 52-week
    high/low, and short-term price change percentages.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'MSFT').

    Returns:
        A formatted string containing all technical analysis data,
        or an error message if the ticker is invalid.
    """
    logger.info(f"Fetching technical data for ticker: {ticker}")

    try:
        stock: yf.Ticker = yf.Ticker(ticker.strip().upper())
        hist: pd.DataFrame = stock.history(period="6mo")

        if hist.empty:
            error_msg: str = f"No data found for ticker '{ticker}'. Please verify the symbol."
            logger.error(error_msg)
            return error_msg

        close: pd.Series = hist["Close"]
        current_price: float = round(float(close.iloc[-1]), 2)

        # ─── Simple Moving Averages ──────────────────────────────
        sma_20: float = round(float(close.rolling(window=20).mean().iloc[-1]), 2)
        sma_50: float = round(float(close.rolling(window=50).mean().iloc[-1]), 2)

        # ─── RSI ─────────────────────────────────────────────────
        rsi: float = _compute_rsi(close)

        # ─── MACD ────────────────────────────────────────────────
        macd: dict[str, float] = _compute_macd(close)

        # ─── Volume ──────────────────────────────────────────────
        avg_volume: int = int(hist["Volume"].mean())
        recent_volume: int = int(hist["Volume"].iloc[-5:].mean())

        # ─── 52-Week Range ───────────────────────────────────────
        high_52w: float = round(float(close.max()), 2)
        low_52w: float = round(float(close.min()), 2)

        # ─── Price Changes ───────────────────────────────────────
        pct_1w: float = round(((current_price - float(close.iloc[-6])) / float(close.iloc[-6])) * 100, 2) if len(close) >= 6 else 0.0
        pct_1m: float = round(((current_price - float(close.iloc[-22])) / float(close.iloc[-22])) * 100, 2) if len(close) >= 22 else 0.0
        pct_3m: float = round(((current_price - float(close.iloc[-66])) / float(close.iloc[-66])) * 100, 2) if len(close) >= 66 else 0.0

        # ─── Trend Signal ────────────────────────────────────────
        trend: str = "BULLISH" if sma_20 > sma_50 else "BEARISH"
        rsi_signal: str = (
            "OVERBOUGHT" if rsi > 70
            else "OVERSOLD" if rsi < 30
            else "NEUTRAL"
        )

        result: str = f"""
=== TECHNICAL ANALYSIS DATA FOR {ticker.upper()} ===

CURRENT PRICE: ${current_price}

MOVING AVERAGES:
  - SMA 20 (Short-term): ${sma_20}
  - SMA 50 (Medium-term): ${sma_50}
  - Trend Signal: {trend} (SMA 20 {'above' if sma_20 > sma_50 else 'below'} SMA 50)

RSI (14-period): {rsi}
  - Signal: {rsi_signal}

MACD (12, 26, 9):
  - MACD Line: {macd['macd_line']}
  - Signal Line: {macd['signal_line']}
  - Histogram: {macd['histogram']}
  - Signal: {'BULLISH' if macd['histogram'] > 0 else 'BEARISH'} crossover

VOLUME:
  - Average Daily Volume (6mo): {avg_volume:,}
  - Recent 5-day Avg Volume: {recent_volume:,}
  - Volume Trend: {'INCREASING' if recent_volume > avg_volume else 'DECREASING'}

PRICE RANGE (6-month):
  - 6-Month High: ${high_52w}
  - 6-Month Low: ${low_52w}
  - Current vs High: {round(((current_price - high_52w) / high_52w) * 100, 2)}%

PRICE CHANGES:
  - 1-Week Change: {pct_1w}%
  - 1-Month Change: {pct_1m}%
  - 3-Month Change: {pct_3m}%
"""

        log_tool_call(logger, "fetch_stock_technical_data", {"ticker": ticker}, result)
        return result

    except Exception as e:
        error_msg = f"Error fetching technical data for '{ticker}': {str(e)}"
        logger.error(error_msg)
        return error_msg
