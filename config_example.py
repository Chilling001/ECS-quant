"""
Example configuration file showing all available options.
This demonstrates how to configure the forex trading bot.

IMPORTANT: Copy this to config.py and fill in your real credentials.
DO NOT commit config.py to version control!
"""

# =============================================================================
# BROKER CONFIGURATION - OANDA
# =============================================================================

# OANDA API credentials
# Get these from: https://www.oanda.com/us-en/trading/demo-account/
OANDA_API_KEY = "your_oanda_api_key_here"
OANDA_ACCOUNT_ID = "your_oanda_account_id_here"

# Practice mode (STRONGLY RECOMMENDED)
# Set to True for paper trading (fake money, no risk)
# Set to False for live trading (real money, high risk)
OANDA_PRACTICE = True  # ⚠️ Keep True until you're VERY confident

# =============================================================================
# AI CONFIGURATION - OpenAI
# =============================================================================

# OpenAI API key for GPT integration
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY = "sk-your_openai_api_key_here"

# AI Model selection (optional - defaults to gpt-3.5-turbo)
# Options: "gpt-3.5-turbo", "gpt-4" (gpt-4 is more expensive but better)
OPENAI_MODEL = "gpt-3.5-turbo"

# =============================================================================
# TELEGRAM CONFIGURATION
# =============================================================================

# Telegram bot token and chat ID
# Create bot: https://t.me/botfather
# Get chat ID: https://api.telegram.org/bot<TOKEN>/getUpdates
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"

# Enable/disable Telegram notifications
TELEGRAM_ENABLED = True

# =============================================================================
# TRADING CONFIGURATION
# =============================================================================

# Default forex pairs to trade
# Can be overridden in GUI
# Examples: EUR/USD, GBP/USD, USD/JPY, EUR/GBP, AUD/USD, etc.
DEFAULT_FOREX_PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY"
]

# =============================================================================
# STRATEGY PARAMETERS
# =============================================================================

# Moving Average periods
# Short MA should be less than Long MA
# Common combinations:
#   - 50/200 (default, long-term)
#   - 20/50 (medium-term)
#   - 10/20 (short-term)
DEFAULT_SHORT_MA = 50
DEFAULT_LONG_MA = 200

# Timeframe for candles
# Options: "5m", "15m", "30m", "1h", "4h", "1d"
# Note: Higher timeframes need more data history
DEFAULT_TIMEFRAME = "1h"  # 1-hour candles

# =============================================================================
# RISK MANAGEMENT
# =============================================================================

# Risk per trade as decimal (0.01 = 1%)
# NEVER use more than 2% per trade
# Conservative: 0.5-1%
# Moderate: 1-2%
# Aggressive: 2%+ (NOT RECOMMENDED)
DEFAULT_RISK_PER_TRADE = 0.01  # 1% risk per trade

# Stop-loss percentage (decimal)
# Distance below entry for long trades
# Example: 0.01 = 1% stop-loss
DEFAULT_STOP_LOSS_PCT = 0.01  # 1% stop-loss

# Take-profit percentage (decimal)
# Distance above entry for long trades
# Should be at least 1.5x the stop-loss for good risk/reward
# Example: 0.02 = 2% take-profit (1:2 risk/reward)
DEFAULT_TAKE_PROFIT_PCT = 0.02  # 2% take-profit

# Maximum drawdown threshold (decimal)
# Bot will alert if account drops this much from peak
# Example: 0.10 = 10% maximum drawdown
DEFAULT_MAX_DRAWDOWN = 0.10  # 10% max drawdown

# =============================================================================
# ADVANCED SETTINGS (Optional)
# =============================================================================

# Update frequency (seconds)
# How often to check for new signals
# Lower = more frequent checks, higher CPU usage
# Higher = less frequent checks, might miss opportunities
UPDATE_FREQUENCY = 60  # Check every 60 seconds

# AI analysis frequency (seconds)
# How often to run AI portfolio analysis
# Recommendation: Every 1-4 hours (3600-14400 seconds)
AI_ANALYSIS_FREQUENCY = 3600  # Every hour

# Maximum concurrent positions
# Limits how many pairs can be traded simultaneously
# Helps prevent over-exposure
MAX_POSITIONS = 3

# Minimum balance to trade
# Bot will not open new positions if balance falls below this
# Set to 0 to disable
MIN_BALANCE = 1000.0  # Minimum $1000

# =============================================================================
# BACKTESTING CONFIGURATION
# =============================================================================

# Initial capital for backtesting
BACKTEST_INITIAL_CAPITAL = 10000.0

# Commission/spread (decimal)
# Typical forex spread: 0.0001 to 0.0003 (1-3 pips)
BACKTEST_COMMISSION = 0.0001  # 1 pip

# Historical data limit
# Number of candles to fetch for backtesting
BACKTEST_DATA_LIMIT = 500

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Enable debug logging
DEBUG_MODE = False

# Log file location (None for no file logging)
LOG_FILE = "forex_bot.log"

# =============================================================================
# GUI CONFIGURATION
# =============================================================================

# Window size (width, height)
GUI_WINDOW_SIZE = (1000, 700)

# Theme/style (if applicable)
GUI_THEME = "default"

# Auto-refresh dashboard interval (seconds)
GUI_REFRESH_INTERVAL = 5

# =============================================================================
# EXAMPLE CONFIGURATIONS FOR DIFFERENT TRADING STYLES
# =============================================================================

# CONSERVATIVE TRADER:
# DEFAULT_RISK_PER_TRADE = 0.005  # 0.5%
# DEFAULT_STOP_LOSS_PCT = 0.01    # 1%
# DEFAULT_TAKE_PROFIT_PCT = 0.03  # 3% (1:3 risk/reward)
# MAX_POSITIONS = 2
# DEFAULT_TIMEFRAME = "4h"

# MODERATE TRADER:
# DEFAULT_RISK_PER_TRADE = 0.01   # 1%
# DEFAULT_STOP_LOSS_PCT = 0.01    # 1%
# DEFAULT_TAKE_PROFIT_PCT = 0.02  # 2% (1:2 risk/reward)
# MAX_POSITIONS = 3
# DEFAULT_TIMEFRAME = "1h"

# AGGRESSIVE TRADER (NOT RECOMMENDED FOR BEGINNERS):
# DEFAULT_RISK_PER_TRADE = 0.02   # 2%
# DEFAULT_STOP_LOSS_PCT = 0.015   # 1.5%
# DEFAULT_TAKE_PROFIT_PCT = 0.03  # 3% (1:2 risk/reward)
# MAX_POSITIONS = 5
# DEFAULT_TIMEFRAME = "30m"

# =============================================================================
# NOTES
# =============================================================================

# 1. Always test with OANDA_PRACTICE = True first
# 2. Backtest your strategy before going live
# 3. Never risk more than you can afford to lose
# 4. Use stop-losses on EVERY trade
# 5. Diversify across multiple pairs
# 6. Monitor your bot regularly
# 7. Review AI suggestions but make your own decisions
# 8. Keep your API keys secret and secure
# 9. Rotate keys regularly
# 10. Start with small amounts even in live trading

# =============================================================================
# GETTING HELP
# =============================================================================

# Documentation: README.md
# Quick Start: QUICKSTART.md
# Issues: https://github.com/Chilling001/ECS-quant/issues
# Demo: python demo.py
