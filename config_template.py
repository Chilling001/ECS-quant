"""
Configuration template for Forex Trading Bot.
Copy this file to config.py and fill in your actual credentials.
DO NOT commit config.py to version control!
"""

# OANDA API Configuration
OANDA_API_KEY = "your_oanda_api_key_here"
OANDA_ACCOUNT_ID = "your_oanda_account_id_here"
OANDA_PRACTICE = True  # Set to True for practice/paper trading account

# OpenAI Configuration
OPENAI_API_KEY = "your_openai_api_key_here"

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"

# Trading Parameters (defaults - can be overridden in GUI)
DEFAULT_FOREX_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY"]
DEFAULT_SHORT_MA = 50  # Short moving average period
DEFAULT_LONG_MA = 200  # Long moving average period
DEFAULT_TIMEFRAME = "1h"  # 1-hour candles
DEFAULT_RISK_PER_TRADE = 0.01  # 1% risk per trade
DEFAULT_STOP_LOSS_PCT = 0.01  # 1% below entry
DEFAULT_TAKE_PROFIT_PCT = 0.02  # 2% above entry
DEFAULT_MAX_DRAWDOWN = 0.10  # 10% maximum drawdown threshold
