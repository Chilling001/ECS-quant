# Streamlit Dashboard Guide

## Overview

The ECS-quant trading bot now includes a modern **Streamlit web dashboard** (`app.py`) that replaces the traditional Tkinter GUI with a web-based interface accessible from any browser.

## Features

### 🎛️ Configuration Sidebar
- **Trading Pairs**: Configure multiple forex pairs (comma-separated)
- **Strategy Parameters**: 
  - Short MA Period (10-500)
  - Long MA Period (50-500)
  - Timeframe selection (5m, 15m, 30m, 1h, 4h, 1d)
- **Risk Management**:
  - Risk per Trade (%)
  - Stop Loss (%)
  - Take Profit (%)
  - Max Drawdown slider (1-50%)
- **Control Buttons**:
  - ▶️ Start Bot
  - ⏹️ Stop Bot
  - 💾 Save Config

### 📊 Main Dashboard

#### Account Overview
Four key metrics displayed at the top:
- **Balance**: Current account balance
- **Open Positions**: Number of active trades
- **Daily P&L**: Profit/Loss for the day (with color coding)
- **Status**: Bot running status (🟢 Running / 🔴 Stopped)

#### Position & Trade Tables
- **Open Positions**: Real-time table showing:
  - Symbol, Side, Size, Entry, Current Price, P&L
- **Recent Trades**: Historical trades table showing:
  - Time, Symbol, Side, Size, Entry, Exit, P&L

#### 🤖 AI Portfolio Manager
- **Quick Action Buttons**:
  - 📊 Analyze Portfolio
  - ⚠️ Risk Assessment
  - 💡 Suggestions
- **Interactive Chat**: Chat with AI assistant about your portfolio
- **Chat History**: View entire conversation with the AI

#### 📝 System Logs
- Expandable section showing recent activity
- Timestamped log entries
- Clear Logs button

## Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your API keys:
```bash
cp config_template.py config.py
# Edit config.py with your API keys
```

### Running the Dashboard

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Alternative: Console Mode

If you prefer the original Tkinter GUI or console mode:
```bash
python forex_bot.py
```

## Features Comparison

| Feature | Streamlit Dashboard | Tkinter GUI |
|---------|-------------------|-------------|
| Web-based | ✅ Yes | ❌ No |
| Mobile-friendly | ✅ Yes | ❌ No |
| Modern UI | ✅ Yes | ⚠️ Basic |
| Auto-refresh | ✅ Yes (5s) | ⚠️ Manual |
| Easy deployment | ✅ Yes | ❌ Desktop only |
| Configuration | ✅ Sidebar | ✅ Tab |
| Dashboard | ✅ Metrics + Tables | ✅ Tables |
| AI Chat | ✅ Modern chat UI | ✅ Text area |
| Logs | ✅ Expandable | ✅ Tab |

## Usage Tips

### Starting the Bot
1. Configure your trading pairs and parameters in the sidebar
2. Adjust risk management settings as needed
3. Click "▶️ Start Bot" to begin trading
4. Monitor the Account Overview metrics for real-time status

### Interacting with AI
1. Use quick action buttons for common queries
2. Type custom questions in the chat input
3. Chat history is preserved during your session
4. AI has context of your account, positions, and trades

### Monitoring Activity
1. Expand "📝 System Logs" to see recent activity
2. Dashboard auto-refreshes every 5 seconds when bot is running
3. Tables update automatically with new positions and trades
4. Use "Clear Logs" to reset the log view

### Saving Configuration
1. Adjust parameters in the sidebar
2. Click "💾 Save Config" to persist your settings
3. Configuration is loaded automatically on next startup

## Technical Details

### Session State Management
The dashboard uses Streamlit's `session_state` to manage:
- Bot instance (single instance per session)
- Bot running status
- Log messages (last 100 entries)
- Chat history (full conversation)
- Last update timestamp for auto-refresh

### Auto-Refresh
When the bot is running, the dashboard automatically refreshes every 5 seconds to display:
- Updated account metrics
- New positions
- Recent trades
- Fresh logs

### Backend Integration
The dashboard integrates seamlessly with the existing `ForexTradingBot` class:
- All backend logic remains unchanged
- Trading, AI, and notification systems work identically
- State persistence continues to use `forex_bot_state.json`

## Deployment

### Local Network Access
Share dashboard with devices on your network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices at `http://YOUR_IP:8501`

### Cloud Deployment
Deploy to Streamlit Cloud for remote access:
1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Deploy with one click

**Note**: Ensure API keys are configured via Streamlit secrets for cloud deployment.

## Troubleshooting

### Dashboard Won't Start
- Check that Streamlit is installed: `pip install streamlit`
- Verify all dependencies: `pip install -r requirements.txt`
- Check for port conflicts (default: 8501)

### Bot Won't Start
- Verify API credentials in `config.py`
- Check logs for initialization errors
- Ensure broker/AI/Telegram components are configured

### UI Not Updating
- Check that bot is running (Status: 🟢 Running)
- Wait for auto-refresh (5 seconds)
- Manually refresh browser if needed
- Check System Logs for errors

## Support

For issues or questions:
- Check `README.md` for general documentation
- Review `QUICKSTART.md` for setup guidance
- Open an issue on GitHub
- Contact the development team

---

**Enjoy trading with the new Streamlit dashboard! 📈🤖**
