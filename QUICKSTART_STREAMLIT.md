# Quick Start Guide for Streamlit Trading Bot

## Installation

```bash
# Clone the repository (if not already)
git clone https://github.com/Chilling001/ECS-quant.git
cd ECS-quant

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. **Set up OpenAI API Key:**

```bash
# Copy the example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit with your API key
nano .streamlit/secrets.toml
```

Edit the file to contain:
```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key"
```

## Running the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at http://localhost:8501

## Usage Examples

### 1. Track Multiple Stocks

In the sidebar, enter symbols separated by commas:
```
AAPL,AMZN,GOOGL,MSFT,TSLA
```

### 2. Configure Strategy Parameters

- **Levels**: Number of trading levels (1-10)
- **Drawdown %**: Maximum drawdown threshold (1-20%)

### 3. Run the Trading Bot

1. Click the **"▶️ Run Bot"** button
2. The bot will:
   - Fetch latest data from yfinance
   - Calculate moving average signals
   - Get AI advice from OpenAI
   - Place mock trades if signals are present
   - Update all displays automatically

### 4. Chat with AI Portfolio Manager

Type a question like:
```
"What's your analysis of my current portfolio?"
"Should I hold or sell AAPL?"
"What are the risks in my current positions?"
```

### 5. Place Manual Orders

Click the **"📥 Buy [SYMBOL]"** buttons under Tracked Equities to place immediate buy orders.

### 6. Monitor Activity

- **Orders Table**: See all filled orders
- **System Logs**: View trading signals and AI advice
- **Account Status**: Monitor cash and positions

### 7. Reset and Start Over

Click **"🔄 Reset"** to restore the initial $10,000 balance and clear all positions.

## Code Architecture

### app.py
```python
# Main Streamlit UI
import streamlit as st
from strategy_engine import StrategyEngine

# Initialize
st.set_page_config(page_title="AI Trading Bot")
engine = StrategyEngine()

# Sidebar inputs
symbols = st.sidebar.text_input("Symbols", "AAPL,AMZN")
levels = st.sidebar.number_input("Levels", 1, 10, 3)
drawdown = st.sidebar.slider("Drawdown %", 1, 20, 5)

# Run strategy
if st.button("Run Bot"):
    for symbol in symbols.split(","):
        result = engine.run_strategy(symbol, levels, drawdown)
```

### strategy_engine.py
```python
# Trading strategy with yfinance and OpenAI
import yfinance as yf
from openai import OpenAI
import streamlit as st

class StrategyEngine:
    def __init__(self):
        # Load OpenAI client from secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=api_key)
    
    def run_strategy(self, symbol, levels, drawdown_pct):
        # Fetch data
        df = yf.download(symbol, period="1d", interval="1m")
        
        # Calculate signals
        df = self.calculate_indicators(df)
        signal = df['signal'].iloc[-1]
        
        # Get AI advice
        advice = self.get_ai_advice(symbol, ...)
        
        # Place trade if signal
        if signal != 0:
            self.place_mock_trade(symbol, signal, ...)
```

## Features Overview

| Feature | Description |
|---------|-------------|
| **Sidebar Config** | Symbols, levels, drawdown inputs |
| **Account Status** | Cash, buying power, positions |
| **Live Prices** | Real-time data via yfinance |
| **Buy Buttons** | Quick order placement |
| **Orders Table** | Order history with timestamps |
| **AI Chat** | Portfolio advice from GPT-3.5 |
| **System Logs** | Activity and signals tracking |
| **Run Bot** | Automated strategy execution |
| **Mock Trading** | Session-based simulation |

## Troubleshooting

### "OpenAI API key not found"
- Make sure `.streamlit/secrets.toml` exists
- Check that the key is correctly formatted
- Verify the key is valid on OpenAI's website

### "Could not fetch data"
- Check internet connection
- Verify symbol is correct (e.g., "AAPL" not "Apple")
- Market may be closed (yfinance returns less data)

### "Module not found"
```bash
pip install -r requirements.txt
```

## Development Mode

For local development without OpenAI:
- Comment out OpenAI calls
- Use mock AI responses
- Focus on UI and yfinance integration

## Deployment

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Add secrets in Streamlit Cloud dashboard
5. Deploy!

## Notes

- This is a **mock trading bot** - no real trades
- yfinance data is delayed/real-time based on market
- OpenAI API calls cost money (check your usage)
- Session state resets on browser refresh
