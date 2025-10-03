# AI-Powered Forex Trading Bot

An advanced AI-powered forex trading bot built with Python, featuring automated trading with the OANDA broker, OpenAI GPT integration for portfolio analysis, and real-time Telegram notifications. Inspired by Roman Paolucci's "How to Build an AI Trading Bot in Python" but specifically adapted for forex markets with paper trading support.

## 🌟 Features

- **Automated Forex Trading**: Connect to OANDA's v20 API via CCXT for real-time forex trading
- **Moving Average Crossover Strategy**: Implements 50/200 SMA crossover strategy on 1-hour candles
- **AI Portfolio Manager**: OpenAI GPT integration provides real-time portfolio analysis and trading suggestions
- **Risk Management**: 1% risk per trade, automatic stop-loss (1% below entry) and take-profit (2% above entry)
- **Telegram Notifications**: Receive instant trade alerts, P&L updates, and AI insights
- **Interactive GUI**: Tkinter-based interface for configuration, monitoring, and AI chat
- **Backtesting**: Test strategies on historical OANDA data using Backtrader
- **Modular Architecture**: Separate modules for broker connection, strategy, AI, notifications, and GUI
- **Paper Trading**: Safe practice trading with OANDA demo accounts (no real money required)

## 📋 Prerequisites

- Python 3.8 or higher
- OANDA practice (demo) account - [Sign up for free](https://www.oanda.com/us-en/trading/demo-account/)
- OpenAI API key - [Get one here](https://platform.openai.com/api-keys)
- Telegram Bot Token - [Create bot with BotFather](https://core.telegram.org/bots#6-botfather)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Chilling001/ECS-quant.git
cd ECS-quant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `ccxt` - Connect to OANDA broker
- `backtrader` - Backtesting framework
- `pandas` - Data manipulation
- `openai` - AI integration
- `python-telegram-bot` - Telegram notifications
- `tkinter` - GUI (included with Python)
- Other dependencies listed in `requirements.txt`

### 3. Configure API Keys

Copy the configuration template and add your credentials:

```bash
cp config_template.py config.py
```

Edit `config.py` with your actual API keys:

```python
# OANDA API Configuration
OANDA_API_KEY = "your_oanda_api_key_here"
OANDA_ACCOUNT_ID = "your_oanda_account_id_here"
OANDA_PRACTICE = True  # Keep True for paper trading

# OpenAI Configuration
OPENAI_API_KEY = "your_openai_api_key_here"

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"
```

**⚠️ Important**: Never commit `config.py` to version control! It contains your secrets.

## 🔑 Getting Your API Keys

### OANDA API Keys (Free Practice Account)

1. Go to [OANDA Practice Account Registration](https://www.oanda.com/us-en/trading/demo-account/)
2. Sign up for a free practice account
3. Log in to your account
4. Go to "Manage API Access"
5. Generate a Personal Access Token
6. Copy your Account ID and API Token

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Create a new secret key
5. Copy and save it securely (you won't see it again)

### Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided
4. Get your Chat ID by:
   - Send a message to your bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Look for `"chat":{"id":YOUR_CHAT_ID}`

## 🎯 Usage

### Running the Bot with GUI

```bash
python forex_bot.py
```

This launches the interactive GUI where you can:
- Configure trading parameters
- Monitor positions and P&L
- Chat with the AI assistant
- View logs and activity

### Running Without GUI (Console Mode)

If tkinter is not available, the bot will run in console mode automatically.

### Configuration Options

In the GUI Configuration tab, you can set:

- **Trading Pairs**: e.g., `EUR/USD,GBP/USD,USD/JPY`
- **Short MA Period**: Default 50
- **Long MA Period**: Default 200
- **Timeframe**: `5m`, `15m`, `30m`, `1h`, `4h`, `1d`
- **Risk per Trade**: Default 1%
- **Stop Loss**: Default 1%
- **Take Profit**: Default 2%
- **Max Drawdown**: Default 10%

## 🧪 Backtesting

Run backtests on historical data:

```python
from backtester import ForexBacktester
from broker_connector import OANDAConnector

# Initialize connector
broker = OANDAConnector(api_key, account_id, practice=True)

# Fetch historical data
df = broker.get_ohlcv('EUR/USD', '1h', limit=500)

# Run backtest
backtester = ForexBacktester()
results = backtester.run_backtest(
    df,
    initial_cash=10000,
    short_ma=50,
    long_ma=200,
    risk_per_trade=0.01,
    stop_loss_pct=0.01,
    take_profit_pct=0.02
)

backtester.print_results()
```

## 📊 Strategy Details

### Moving Average Crossover Strategy

**Entry Signals:**
- **Buy**: When 50-period SMA crosses above 200-period SMA
- **Sell**: When 50-period SMA crosses below 200-period SMA

**Exit Conditions:**
- Stop-loss hit (1% below entry for longs)
- Take-profit hit (2% above entry for longs)
- Reverse signal (opposite crossover)

**Risk Management:**
- Maximum 1% risk per trade
- Position sizing based on account balance and stop-loss distance
- No over-leveraging protection
- Maximum drawdown monitoring

## 🤖 AI Integration

The bot uses OpenAI GPT-3.5-turbo as an AI portfolio manager to:

- Analyze risk exposure and diversification
- Evaluate position sizing
- Provide trading suggestions
- Answer questions about forex trading
- Assess trade ideas before execution

**Example AI Queries:**
- "Analyze my current portfolio"
- "What's the risk of my positions?"
- "Should I enter EUR/USD now?"
- "Explain the moving average crossover strategy"

## 📱 Telegram Notifications

The bot sends notifications for:

- **Trade Entries**: Symbol, side, amount, entry price, stop-loss, take-profit
- **Trade Exits**: Symbol, exit price, P&L
- **AI Insights**: Portfolio analysis and suggestions
- **Alerts**: Important warnings and information
- **Daily Summary**: Balance, positions, P&L, trade count

## 🏗️ Project Structure

```
ECS-quant/
├── forex_bot.py              # Main bot orchestrator
├── broker_connector.py       # OANDA connection via CCXT
├── forex_strategy.py         # Moving average crossover strategy
├── ai_manager.py             # OpenAI GPT integration
├── telegram_notifier.py      # Telegram notifications
├── forex_gui.py              # Tkinter GUI interface
├── backtester.py             # Backtesting with Backtrader
├── config_template.py        # Configuration template
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                # This file
├── trendbot.py              # Legacy EMA crossover bot (SPY)
├── asymmetricbot.py         # Legacy asymmetric risk bot (SPXL)
└── randobot.py              # Legacy random entry bot (testing)
```

## ⚙️ Module Descriptions

### `forex_bot.py`
Main controller that orchestrates all components, manages the trading loop, and coordinates between strategy, broker, AI, and notifications.

### `broker_connector.py`
Handles connection to OANDA broker via CCXT library. Provides methods for fetching data, placing orders, managing positions, and account queries.

### `forex_strategy.py`
Implements the moving average crossover strategy with signal generation, position sizing, stop-loss/take-profit calculation, and exit condition checking.

### `ai_manager.py`
Integrates OpenAI GPT for portfolio analysis, trade evaluation, and general trading queries. Maintains conversation history and provides context-aware responses.

### `telegram_notifier.py`
Sends formatted notifications to Telegram for trade entries/exits, alerts, AI insights, and daily summaries.

### `forex_gui.py`
Tkinter-based GUI with tabs for configuration, dashboard monitoring, AI chat interface, and system logs.

### `backtester.py`
Backtesting engine using Backtrader framework. Tests strategies on historical data with performance metrics including Sharpe ratio, drawdown, win rate, and returns.

## 🔒 Security Best Practices

- **Never commit secrets**: `config.py` is in `.gitignore`
- **Use practice accounts**: Keep `OANDA_PRACTICE = True` for paper trading
- **Secure API keys**: Store them securely and rotate regularly
- **Monitor activity**: Review bot actions and set alerts
- **Start small**: Test with minimal capital even on practice accounts

## 🐛 Troubleshooting

### "Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID"
- Make sure you've created `config.py` from `config_template.py`
- Verify your Telegram credentials are correct

### "CCXT OANDA not connecting"
- Check your OANDA API key and account ID
- Ensure you're using a practice account
- Verify your OANDA account is active

### "OpenAI API Error"
- Verify your OpenAI API key is valid
- Check you have API credits available
- Ensure you're not hitting rate limits

### GUI Not Starting
- Install tkinter: `sudo apt-get install python3-tk` (Linux)
- On macOS/Windows, tkinter should be included with Python
- The bot will fall back to console mode if GUI is unavailable

## 📈 Performance Monitoring

The bot tracks:
- Account balance (real-time)
- Open positions
- Daily P&L
- Trade history
- Win/loss ratio
- Drawdown levels

View these metrics in the Dashboard tab of the GUI.

## 🛠️ Customization

### Adding New Trading Pairs

Edit the pairs list in the Configuration tab or modify `DEFAULT_FOREX_PAIRS` in `config_template.py`.

### Changing Strategy Parameters

Adjust moving average periods, risk percentages, and stop-loss/take-profit levels in the GUI Configuration tab.

### Implementing New Strategies

Extend the `MovingAverageCrossoverStrategy` class in `forex_strategy.py` or create new strategy classes following the same interface.

## 📝 Legacy Bots

This repository also includes three legacy trading bots for reference:

- **trendbot.py**: EMA crossover + ADX strategy for SPY
- **asymmetricbot.py**: Asymmetric risk strategy for SPXL (3x ETF)
- **randobot.py**: Random entry bot for testing infrastructure

These demonstrate different approaches and can be used as examples for building custom strategies.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Disclaimer

**THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.**

- Trading forex carries significant risk of loss
- Past performance does not guarantee future results
- The AI provides suggestions, not financial advice
- Always use practice accounts for testing
- Never trade with money you can't afford to lose
- Consult a licensed financial advisor before live trading

The authors and contributors are not responsible for any financial losses incurred through the use of this software.

## 📜 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by Roman Paolucci's "How to Build an AI Trading Bot in Python" YouTube tutorial
- Built with [CCXT](https://github.com/ccxt/ccxt) for broker connectivity
- [Backtrader](https://www.backtrader.com/) for backtesting framework
- [OpenAI](https://openai.com/) for AI capabilities
- [OANDA](https://www.oanda.com/) for forex market access

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

---

**Happy Trading! 🚀📈**

Remember: Start with paper trading, learn the system, and never risk more than you can afford to lose.