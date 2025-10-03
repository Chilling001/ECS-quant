# Quick Start Guide - AI Forex Trading Bot

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

**Packages installed:**
- `ccxt` - Connect to OANDA
- `pandas` - Data handling
- `backtrader` - Backtesting
- `openai` - AI integration
- `python-telegram-bot` - Notifications
- `requests` - HTTP requests

### Step 2: Get Free API Keys (3 minutes)

#### OANDA Practice Account (FREE - No Credit Card)
1. Go to: https://www.oanda.com/us-en/trading/demo-account/
2. Sign up for free practice account
3. Login → Manage API Access → Generate Personal Access Token
4. Copy your Account ID and API Token

#### OpenAI API Key (May require payment)
1. Go to: https://platform.openai.com/
2. Sign up or login
3. Go to: https://platform.openai.com/api-keys
4. Create new secret key
5. Copy and save it

#### Telegram Bot Token (FREE)
1. Open Telegram, search `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Send a message to your bot
5. Get your chat ID from: `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Step 3: Configure (1 minute)

```bash
# Copy template
cp config_template.py config.py

# Edit config.py with your API keys
# (Use any text editor)
nano config.py
```

**Paste your keys:**
```python
OANDA_API_KEY = "your_token_here"
OANDA_ACCOUNT_ID = "your_account_id_here"
OANDA_PRACTICE = True  # Keep this True!

OPENAI_API_KEY = "sk-your_key_here"

TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"
```

### Step 4: Run! (30 seconds)

```bash
python forex_bot.py
```

**That's it! The GUI will open.**

---

## 🎯 First Time Using the Bot?

### In the Configuration Tab:

1. **Trading Pairs**: Start with just `EUR/USD`
2. **Timeframe**: Keep `1h` (1 hour)
3. **Risk per Trade**: Keep `1.0%`
4. **Stop Loss**: Keep `1.0%`
5. **Take Profit**: Keep `2.0%`

### Click "Start Bot"

The bot will:
- Connect to OANDA practice account
- Start monitoring EUR/USD
- Wait for 50/200 SMA crossover signals
- Send Telegram notifications on trades

---

## 💬 Using the AI Assistant

Switch to the "AI Assistant" tab and try:

- "Explain how the moving average crossover strategy works"
- "Analyze my current portfolio"
- "What's the risk exposure right now?"
- "Should I trade EUR/USD today?"

---

## 📊 Running a Backtest

Open a Python shell:

```python
from broker_connector import OANDAConnector
from backtester import run_sample_backtest
import config

# Create connector
broker = OANDAConnector(
    config.OANDA_API_KEY,
    config.OANDA_ACCOUNT_ID,
    config.OANDA_PRACTICE
)

# Run backtest
results = run_sample_backtest(broker, 'EUR/USD', '1h')
```

---

## ⚠️ Important Notes

### Practice Account
- ALWAYS keep `OANDA_PRACTICE = True`
- Practice accounts use fake money
- Perfect for learning and testing
- No risk to real money

### API Costs
- OANDA practice: **FREE**
- Telegram: **FREE**
- OpenAI: **Paid** (but cheap for occasional use)
  - ~$0.002 per request with GPT-3.5-turbo
  - Budget ~$5 for extensive testing

### System Requirements
- Python 3.8+
- Internet connection
- ~100MB disk space
- Works on Windows, Mac, Linux

---

## 🐛 Troubleshooting

### "No module named ccxt"
```bash
pip install ccxt
```

### "Missing TELEGRAM_TOKEN"
- Make sure you created `config.py` from template
- Check your credentials are correct

### "OANDA connection failed"
- Verify API key and account ID are correct
- Make sure `OANDA_PRACTICE = True`
- Check internet connection

### GUI won't start (Linux)
```bash
sudo apt-get install python3-tk
```

### GUI won't start (still)
The bot will automatically fall back to console mode without GUI.

---

## 📚 Next Steps

### 1. Monitor Your First Trades
- Watch the Dashboard tab
- Check Telegram for notifications
- Review logs for activity

### 2. Try Different Pairs
- Add `GBP/USD,USD/JPY` to trading pairs
- See how multiple pairs trade

### 3. Optimize Strategy
- Try different MA periods (e.g., 20/50)
- Adjust risk/reward ratios
- Use shorter timeframes (30m)

### 4. Backtest Before Live
- Always backtest new strategies
- Check win rate and drawdown
- Verify risk management

### 5. Learn from AI
- Ask AI about failed trades
- Get suggestions for improvements
- Understand market conditions

---

## 🎓 Learning Resources

### Understand the Strategy
- Read README.md "Strategy Details" section
- Watch YouTube: "Moving Average Crossover Strategy"
- Practice on demo account for 1 month minimum

### Forex Basics
- Learn about pips, lots, and leverage
- Understand major currency pairs
- Study support/resistance levels

### Risk Management
- Never risk more than 1-2% per trade
- Use stop-losses on every trade
- Don't over-leverage

---

## ✅ Checklist

Before running with real money (DON'T RUSH THIS):

- [ ] Used practice account for at least 1 month
- [ ] Understand how the strategy works
- [ ] Backtested on 6+ months of data
- [ ] Practiced risk management
- [ ] Know how to read charts
- [ ] Comfortable with losses (they happen!)
- [ ] Have proper capital (never trade loan money)
- [ ] Understand tax implications
- [ ] Consulted with a financial advisor

**Remember: This is a learning tool. Start slow, practice extensively.**

---

## 🤝 Getting Help

- **Documentation**: README.md has detailed info
- **Issues**: Open issue on GitHub
- **Community**: Check existing issues for solutions

---

**Happy Learning! 📚🤖📈**
