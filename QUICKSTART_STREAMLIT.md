# Quick Start: Streamlit Dashboard

Get up and running with the Streamlit dashboard in 5 minutes!

## Prerequisites

- Python 3.8+
- pip package manager

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

This installs:
- streamlit (web dashboard)
- pandas (data handling)
- ccxt (broker connection)
- openai (AI features)
- python-telegram-bot (notifications)
- All other dependencies

## Step 2: Configure API Keys (2 minutes)

1. Copy the configuration template:
```bash
cp config_template.py config.py
```

2. Edit `config.py` with your API keys:
```python
# OANDA API (get free practice account at oanda.com)
OANDA_API_KEY = "your_api_key"
OANDA_ACCOUNT_ID = "your_account_id"
OANDA_PRACTICE = True  # Use practice account

# OpenAI API (get at platform.openai.com)
OPENAI_API_KEY = "your_openai_key"

# Telegram (optional - get from @BotFather)
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
```

**Don't have API keys yet?** See [README.md](README.md) for detailed instructions on getting them for free.

## Step 3: Launch Dashboard (30 seconds)

```bash
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Step 4: Configure & Start Bot (1 minute)

In the sidebar:

1. **Trading Pairs**: Enter pairs like `EUR/USD,GBP/USD,USD/JPY`
2. **Strategy Parameters**: 
   - Short MA: 50
   - Long MA: 200
   - Timeframe: 1h
3. **Risk Management**:
   - Risk per Trade: 1%
   - Stop Loss: 1%
   - Take Profit: 2%
   - Max Drawdown: 10%
4. Click **"▶️ Start Bot"**

## What You'll See

### Top Metrics (Auto-updates every 5 seconds)
- **Balance**: Your account balance
- **Open Positions**: Number of active trades
- **Daily P&L**: Profit/Loss for today
- **Status**: 🟢 Running or 🔴 Stopped

### Position & Trade Tables
- **Open Positions**: Real-time view of active trades
- **Recent Trades**: History of closed trades with P&L

### AI Portfolio Manager
- Chat with AI about your portfolio
- Click quick action buttons for instant analysis
- Get trading suggestions and risk assessments

### System Logs
- Expand to see recent activity
- Bot actions, trades, and system events
- Clear logs with one click

## Common Tasks

### Change Settings While Running
1. Adjust parameters in sidebar
2. Click **"💾 Save Config"**
3. Stop and restart bot to apply changes

### Chat with AI
- Type in the chat box at the bottom
- Or click quick action buttons:
  - 📊 Analyze Portfolio
  - ⚠️ Risk Assessment
  - 💡 Suggestions

### Monitor Activity
- Expand **"📝 System Logs"** section
- Watch real-time updates every 5 seconds
- Check tables for new positions/trades

### Stop the Bot
- Click **"⏹️ Stop Bot"** in sidebar
- Status changes to 🔴 Stopped
- All positions remain open

## Tips

✅ **Start with Practice Account**
- Keep `OANDA_PRACTICE = True` in config.py
- Test strategies risk-free
- Practice accounts are completely free

✅ **Monitor the Dashboard**
- Check Status indicator (should be 🟢 Running)
- Watch Daily P&L in real-time
- Review System Logs for errors

✅ **Use AI Assistant**
- Ask questions about forex trading
- Get portfolio analysis anytime
- Request trade suggestions

✅ **Adjust Risk Settings**
- Start conservative (1% risk per trade)
- Use tight stop-losses
- Set max drawdown limit

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Dashboard won't start
```bash
# Check if port 8501 is in use
streamlit run app.py --server.port 8502
```

### Bot won't start
- Verify API keys in `config.py`
- Check OANDA credentials are correct
- Ensure practice account is active

### No data in tables
- Wait for bot to make first trade
- Check System Logs for errors
- Verify broker connection

## Need Help?

- 📖 **Full Documentation**: See [STREAMLIT_DASHBOARD.md](STREAMLIT_DASHBOARD.md)
- 🔧 **General Setup**: See [README.md](README.md)
- 🚀 **Quick Reference**: See [QUICKSTART.md](QUICKSTART.md)
- 🐛 **Issues**: Open an issue on GitHub

## Advanced: Remote Access

### Access from Other Devices on Your Network

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then visit `http://YOUR_COMPUTER_IP:8501` from any device on your network.

### Deploy to Cloud (Streamlit Cloud)

1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repository
4. Add API keys in "Secrets" section
5. Deploy!

---

**That's it! You're now running an AI-powered forex trading bot with a modern web dashboard! 🚀📈**

For questions or issues, check the documentation or open an issue on GitHub.
