"""
Unified Test Configuration — Shared Fixtures

Provides shared pytest fixtures for all agent tests, including
a reusable Ollama LLM judge for LLM-as-a-Judge evaluations.
"""

import pytest
from crewai import LLM
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


@pytest.fixture(scope="session")
def llm_judge() -> LLM:
    """
    Create a shared LLM instance for LLM-as-a-Judge evaluations.

    This fixture is session-scoped so the model is only loaded once
    across all test files for efficiency.

    Returns:
        A configured LLM instance pointing to the local Ollama server.
    """
    return LLM(
        model=f"ollama/{OLLAMA_MODEL}",
        base_url=OLLAMA_BASE_URL,
    )
