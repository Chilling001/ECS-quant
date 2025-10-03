# Streamlit Dashboard Guide

## Overview

The Forex Trading Bot now features a modern web-based dashboard built with Streamlit, replacing the legacy Tkinter desktop interface. This provides a better user experience with real-time updates, modern design, and browser-based access.

## Quick Start

### Method 1: Using the Helper Script (Recommended)
```bash
python run_dashboard.py
```

### Method 2: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## Features

### 1. Dashboard Page
The main dashboard provides real-time monitoring of your trading bot:

- **Account Metrics**
  - Current balance
  - Number of open positions
  - Daily profit/loss (color-coded)
  
- **Open Positions Table**
  - Symbol, side, size
  - Entry and current prices
  - Unrealized P&L
  
- **Recent Trades Table**
  - Trade history with timestamps
  - Entry/exit prices
  - Realized P&L

- **Auto-Refresh**: Dashboard updates every 5 seconds when bot is running

### 2. Configuration Page
Configure all trading parameters:

- **Trading Pairs**: Comma-separated list (e.g., EUR/USD,GBP/USD,USD/JPY)
- **Moving Averages**: Short and long MA periods
- **Timeframe**: 5m, 15m, 30m, 1h, 4h, 1d
- **Risk Management**:
  - Risk per trade (%)
  - Stop loss (%)
  - Take profit (%)
  - Maximum drawdown (%)

**Controls**:
- 💾 Save Configuration: Persist settings
- ▶️ Start Bot: Initialize and start trading
- ⏹️ Stop Bot: Gracefully stop trading

### 3. AI Assistant Page
Interact with the AI trading assistant:

- **Quick Queries**: One-click buttons for common questions
  - 📊 Analyze Portfolio
  - ⚠️ Risk Assessment
  - 💡 Get Suggestions
  
- **Chat Interface**: Ask custom questions
  - Portfolio analysis
  - Risk evaluation
  - Trading strategy advice
  - Market insights
  
- **Chat History**: View conversation history
- **Clear Chat**: Reset conversation

### 4. Logs Page
View system logs and activity:

- Real-time log display
- Timestamps for all events
- Export logs to file
- Clear logs button

## Advantages Over Tkinter

### Modern Web Interface
- **Browser-based**: Access from any device on your network
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional design with metrics and cards
- **No Installation Issues**: No Tkinter dependencies required

### Better User Experience
- **Real-time Updates**: Dashboard auto-refreshes during bot operation
- **Color Coding**: Visual indicators for profit/loss
- **Intuitive Navigation**: Sidebar with clear page selection
- **Better Layouts**: Organized columns and sections

### Enhanced Features
- **Export Functionality**: Download logs as text files
- **Session Management**: Maintains state across page refreshes
- **Quick Actions**: One-click buttons for common tasks
- **Better Error Handling**: Clear error messages and warnings

### Development Benefits
- **Easier Maintenance**: Simpler code structure
- **Hot Reloading**: Changes reflect immediately during development
- **Better Debugging**: Browser dev tools available
- **Extensible**: Easy to add new features and widgets

## Migration from Tkinter

If you were using the old Tkinter GUI:

### Old Way (Tkinter)
```bash
python forex_bot.py
```

### New Way (Streamlit)
```bash
streamlit run streamlit_app.py
# or
python run_dashboard.py
```

### Still Need Tkinter?
You can still use the legacy Tkinter interface:
```bash
python forex_bot.py --gui
```

## Configuration Tips

1. **Start Conservative**: Use low risk percentages (0.5-1%)
2. **Practice First**: Always use OANDA practice account initially
3. **Monitor Regularly**: Check dashboard frequently during trading
4. **Save Configs**: Use the save button to persist your settings
5. **Review Logs**: Check logs page for errors or warnings

## Troubleshooting

### Port Already in Use
If port 8501 is already occupied:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Browser Doesn't Open
Manually navigate to:
```
http://localhost:8501
```

### Configuration Not Loading
1. Ensure `config.py` exists (copy from `config_template.py`)
2. Check that API keys are correctly set
3. Review logs page for initialization errors

### Bot Won't Start
1. Click "Initialize Bot" first
2. Check API credentials in configuration
3. Verify OANDA practice account is active
4. Review error messages in logs

## Keyboard Shortcuts

When the Streamlit app is running:

- `Ctrl + C` (in terminal): Stop the Streamlit server
- `R`: Rerun the app (from browser)
- `C`: Clear cache (from browser menu)

## Performance Notes

- **Auto-refresh**: Only active on Dashboard page when bot is running
- **Chat History**: Limited to recent messages to conserve memory
- **Logs**: Automatically limited to last 100 entries
- **Session State**: Persists within browser session

## Security Notes

1. **Local Access Only**: By default, accessible only on localhost
2. **No Authentication**: Anyone with network access can view dashboard
3. **Sensitive Data**: Config file with API keys is not exposed through UI
4. **Safe Defaults**: Bot uses practice mode unless explicitly configured

## Advanced Usage

### Running on a Server
To make dashboard accessible from other machines:
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

⚠️ **Warning**: This exposes the dashboard to your network. Use with caution.

### Custom Port
```bash
streamlit run streamlit_app.py --server.port 8080
```

### Headless Mode (No Browser)
```bash
streamlit run streamlit_app.py --server.headless true
```

## Support

For issues or questions:
1. Check the logs page in the dashboard
2. Review console output where Streamlit is running
3. Refer to README.md for general bot configuration
4. Check OANDA and OpenAI API status

## Future Enhancements

Potential additions to the Streamlit dashboard:
- [ ] Performance charts and visualizations
- [ ] Trade history export
- [ ] Backtesting interface
- [ ] Strategy comparison tools
- [ ] Real-time price charts
- [ ] Alert configuration
- [ ] Multi-user authentication
