# 🚀 Smart Investor Swarm

A locally-hosted **Multi-Agent System (MAS)** that automates comprehensive stock investment research using AI agents powered by **Ollama** and orchestrated by **CrewAI**.

This project leverages a sequential pipeline of four specialized AI agents to analyze stock data, gauge market sentiment, evaluate fundamentals, and generate a professional investment report with actionable recommendations (Buy/Hold/Sell).

---

## 📋 Table of Contents
1. [Overview](#-overview)
2. [Architecture](#%EF%B8%8F-architecture)
3. [Tech Stack](#%EF%B8%8F-tech-stack)
4. [Prerequisites](#-prerequisites)
5. [Installation & Setup](#-installation--setup)
6. [Configuration](#%EF%B8%8F-configuration)
7. [Running the System](#-running-the-system)
8. [Running Tests](#-running-tests)
9. [Troubleshooting](#%EF%B8%8F-troubleshooting)
10. [Project Structure](#-project-structure)

---

## 📋 Overview

The **Smart Investor Swarm** takes a single stock ticker (e.g., `AAPL`, `GOOGL`) and orchestrates a team of 4 AI agents to perform a deep-dive analysis. Each agent builds upon the findings of the previous one, ensuring a cohesive and comprehensive final report.

---

## 🏗️ Architecture

The system uses a **sequential workflow** where context flows from one agent to the next:

```
User Input (ticker: "AAPL")
    │
    ▼
┌────────────────────────────────────┐
│ Agent 1: Technical Data Collector  │  ← yfinance tool (SMA, RSI, MACD)
└──────────────┬─────────────────────┘
               │ context passed
               ▼
┌────────────────────────────────────┐
│ Agent 2: Sentiment Analyst         │  ← News scraper tool (BeautifulSoup)
└──────────────┬─────────────────────┘
               │ context passed
               ▼
┌────────────────────────────────────┐
│ Agent 3: Fundamental Analyst       │  ← yfinance fundamentals tool
└──────────────┬─────────────────────┘
               │ context passed
               ▼
┌────────────────────────────────────┐
│ Agent 4: Portfolio Strategist      │  ← Report writer tool (Markdown)
└────────────────────────────────────┘
               │
               ▼
        📄 Final Report (./reports/)
```

### The 4 Specialized Agents:
1. **Technical Analyst**: Fetches and analyzes historical price data, SMA, RSI, and MACD.
2. **Sentiment Analyst**: Scrapes recent news headlines and evaluates market sentiment.
3. **Fundamental Analyst**: Evaluates balance sheets, income statements, and valuation metrics.
4. **Portfolio Strategist**: Synthesizes all data into a final report with a Buy/Hold/Sell rating.

---

## 🛠️ Tech Stack

- **Orchestration**: [CrewAI](https://github.com/crewAIInc/crewAI)
- **Local LLM**: [Ollama](https://ollama.ai/) (Default: `llama3.2` or `qwen2.5`)
- **Data Sources**: `yfinance` (Financials), `requests` + `BeautifulSoup4` (News)
- **Testing**: `pytest` + LLM-as-a-Judge methodology

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.10 or higher**
2. **Ollama** (Download from [ollama.com](https://ollama.com))

---

## 🚀 Installation & Setup

Follow these steps to get the project running locally:

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd smart-investor-swarm
```

### 2. Set Up a Virtual Environment
**On Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Ollama and Pull the Model
Make sure the Ollama application is running in the background, then pull the required model:

```bash
ollama pull llama3.2
```
*(Optional: If you prefer using `qwen2.5`, run `ollama pull qwen2.5` and update the `.env` file accordingly).*

---

## 🛠️ Configuration

The project uses a `.env` file for configuration. A default one is provided, but you can modify it if needed.

**File:** `.env`
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Application Settings
LOG_LEVEL=INFO
REPORTS_DIR=./reports
```

---

## 📈 Running the System

To run the full multi-agent analysis for a specific stock ticker, use:

```bash
python main.py <TICKER>
```

**Example:**
```bash
python main.py MSFT
```

The execution will print logs to the console and save a detailed Markdown report in the `./reports/` directory.

---

## 🧪 Running Tests

The project includes both standard unit tests and **LLM-as-a-Judge** evaluations to verify agent behavior.

Ensure Ollama is running before executing tests.

**Run all tests:**
```bash
pytest tests/ -v
```

**Run tests for a specific agent:**
```bash
pytest tests/test_technical_agent.py -v
```

---

## 🛠️ Troubleshooting

### 1. Connection Refused to Ollama
**Error:** `Failed to establish a new connection: [Errno 111] Connection refused`
- **Fix:** Ensure the Ollama application is running on your machine. Check if `http://localhost:11434` is accessible in your browser.

### 2. Model Not Found
**Error:** `model 'llama3.2' not found, try pulling it first`
- **Fix:** Run `ollama pull llama3.2` in your terminal.

### 3. Rate Limits / yfinance Issues
- **Fix:** `yfinance` sometimes gets blocked if queried too frequently. Wait a few minutes or switch networks if data retrieval fails consistently.

---

## 📁 Project Structure

```
smart-investor-swarm/
├── main.py                         # Application Entry Point
├── requirements.txt                # Python Dependencies
├── .env                            # Configuration File
├── src/
│   ├── config.py                   # Environment & Path Loader
│   ├── crew.py                     # CrewAI Assembly & Execution
│   ├── agents/                     # Agent Definitions
│   ├── tasks/                      # CrewAI Task Definitions
│   ├── tools/                      # Custom Python Tools
│   └── utils/                      # Logging & Utilities
├── tests/                          # Test Suites & LLM Judges
└── reports/                        # Generated Investment Reports
```

---

## 📄 License

This project is for educational purposes only. **This is not financial advice.** Use at your own risk.
