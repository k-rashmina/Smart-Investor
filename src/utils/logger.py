"""
Smart Investor Swarm — AgentOps Logger

Provides structured logging and observability for all agent interactions.
Logs agent inputs, tool calls, outputs, and errors with timestamps
to both the console and a log file for post-execution analysis.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from src.config import PROJECT_ROOT, LOG_LEVEL


# ─── Log File Setup ─────────────────────────────────────────────────
LOG_DIR: Path = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE: Path = LOG_DIR / f"swarm_run_{_timestamp}.log"


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger instance.

    Each logger writes to both stdout (colored) and a persistent log file.
    This satisfies the LLMOps/AgentOps observability requirement.

    Args:
        name: The name for the logger (typically __name__ or agent name).

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # ─── Console Handler ─────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_fmt = logging.Formatter(
        "\033[36m%(asctime)s\033[0m | \033[33m%(name)-30s\033[0m | "
        "%(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)

    # ─── File Handler ────────────────────────────────────────────
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_agent_action(
    logger: logging.Logger,
    agent_name: str,
    action: str,
    detail: str,
) -> None:
    """
    Log a structured agent action for observability.

    Args:
        logger: The logger instance to use.
        agent_name: Name of the agent performing the action.
        action: Type of action (e.g., 'TOOL_CALL', 'OUTPUT', 'ERROR').
        detail: Description or data of the action.
    """
    logger.info(f"[{agent_name}] {action}: {detail}")


def log_tool_call(
    logger: logging.Logger,
    tool_name: str,
    inputs: dict,
    output: str,
) -> None:
    """
    Log a tool invocation with its inputs and output.

    Args:
        logger: The logger instance to use.
        tool_name: Name of the tool being called.
        inputs: Dictionary of input parameters.
        output: The tool's return value (truncated for readability).
    """
    truncated_output = output[:500] + "..." if len(output) > 500 else output
    logger.info(
        f"[TOOL:{tool_name}] Inputs: {inputs} | Output: {truncated_output}"
    )
