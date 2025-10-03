# Streamlit Trading Bot

This is the Streamlit version of the AI-Powered Trading Bot.

## Features

- **Clean Streamlit Dashboard** with sidebar configuration
- **Real-time Stock Data** via yfinance
- **AI Portfolio Manager** using OpenAI GPT
- **Mock Trading** with session state management
- **Interactive UI** with account status, orders, and logs

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure OpenAI API Key:

Create `.streamlit/secrets.toml` from the example:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your OpenAI API key:
```toml
OPENAI_API_KEY = "your-actual-openai-api-key"
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

## Usage

### Sidebar Configuration
- **Trading Symbols**: Enter comma-separated stock symbols (e.g., AAPL,AMZN,GOOGL)
- **Levels**: Set the number of trading levels (1-10)
- **Drawdown %**: Set maximum drawdown percentage threshold (1-20%)

### Main Dashboard
- **Account Status**: View cash, buying power, and open positions
- **Tracked Equities**: See latest prices and place buy orders
- **Orders**: View all filled orders
- **AI Portfolio Manager**: Chat with the AI for trading advice
- **System Logs**: View recent trading activity
- **Run Bot**: Execute the trading strategy for all tracked symbols

## Components

### app.py
Main Streamlit application with the dashboard UI.

### strategy_engine.py
Trading strategy engine that:
- Fetches data using yfinance
- Calculates moving average signals
- Gets AI advice from OpenAI
- Places mock trades
- Updates session state

### ai_manager.py (Updated)
OpenAI integration using the new client API for portfolio analysis and chat.

## Mock Trading

The bot uses Streamlit session state for mock trading:
- Initial balance: $10,000
- Mock orders are tracked in session state
- No real trades are executed
- Use "Reset" button to restore initial state

## Note

This is a mock trading bot for educational purposes. It does not execute real trades.
The yfinance data is used for simulation only.
