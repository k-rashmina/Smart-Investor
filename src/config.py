"""
Smart Investor Swarm — Configuration Module

Centralizes all LLM, logging, and application settings.
Loads environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ─── Ollama LLM Configuration ───────────────────────────────────────
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

# ─── Application Paths ──────────────────────────────────────────────
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
REPORTS_DIR: Path = PROJECT_ROOT / os.getenv("REPORTS_DIR", "reports")

# Ensure the reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ─── Logging ─────────────────────────────────────────────────────────
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
