"""
Smart Investor Swarm — Main Entry Point

Run this script to analyze any stock ticker using the multi-agent system.

Usage:
    python main.py AAPL
    python main.py GOOGL
    python main.py MSFT
"""

import sys
import time
from datetime import datetime
from src.crew import build_crew
from src.config import REPORTS_DIR
from src.utils.logger import get_logger, LOG_FILE

logger = get_logger("Main")


def main() -> None:
    """
    Main entry point for the Smart Investor Swarm.

    Reads the stock ticker from command-line arguments,
    builds the crew, and kicks off the analysis pipeline.
    """
    # ─── Parse Arguments ─────────────────────────────────────────
    if len(sys.argv) < 2:
        print("\n╔══════════════════════════════════════════════════╗")
        print("║       🚀 Smart Investor Swarm                   ║")
        print("║       Multi-Agent Stock Analysis System          ║")
        print("╠══════════════════════════════════════════════════╣")
        print("║                                                  ║")
        print("║  Usage:  python main.py <TICKER>                 ║")
        print("║                                                  ║")
        print("║  Examples:                                       ║")
        print("║    python main.py AAPL                           ║")
        print("║    python main.py GOOGL                          ║")
        print("║    python main.py MSFT                           ║")
        print("║    python main.py TSLA                           ║")
        print("║                                                  ║")
        print("╚══════════════════════════════════════════════════╝\n")
        sys.exit(1)

    ticker: str = sys.argv[1].strip().upper()

    # ─── Banner ──────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  🚀 SMART INVESTOR SWARM")
    print("  Multi-Agent Stock Analysis System")
    print("=" * 60)
    print(f"  📈 Analyzing: {ticker}")
    print(f"  📝 Log File:  {LOG_FILE}")
    print("=" * 60 + "\n")

    logger.info(f"Starting Smart Investor Swarm for ticker: {ticker}")
    start_time: float = time.time()

    # ─── Build & Run Crew ────────────────────────────────────────
    try:
        crew = build_crew(ticker)
        result = crew.kickoff()

        elapsed: float = round(time.time() - start_time, 2)

        # ─── Final Report Save ─────────────────────────────────────────
        # We officially save the raw Markdown result directly here instead of 
        # relying on the fragile LLM JSON tool-calling.
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORTS_DIR / f"{ticker}_investment_report_{timestamp}.md"
        try:
            report_file.write_text(str(result), encoding="utf-8")
            logger.info(f"Final report saved to {report_file}")
        except Exception as write_err:
            logger.error(f"Failed to write final report: {write_err}")

        print("\n" + "=" * 60)
        print("  ✅ ANALYSIS COMPLETE")
        print("=" * 60)
        print(f"  ⏱️  Total Time: {elapsed} seconds")
        print(f"  📝 Log File: {LOG_FILE}")
        print(f"  📁 Check ./reports/ for the full report")
        print("=" * 60)

        logger.info(f"Analysis completed in {elapsed} seconds")
        logger.info(f"Final output:\n{result}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        logger.warning("Analysis interrupted by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        print("Check the log file for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
