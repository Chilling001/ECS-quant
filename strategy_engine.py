"""
Strategy Engine Module
Implements trading strategy with yfinance data fetching and OpenAI integration for Streamlit app.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from openai import OpenAI


class StrategyEngine:
    """
    Trading strategy engine using yfinance for data and OpenAI for AI advice.
    """
    
    def __init__(self):
        """Initialize the strategy engine."""
        self.client = None
        self.initialize_openai()
        
    def initialize_openai(self):
        """Initialize OpenAI client from Streamlit secrets."""
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                st.warning("OpenAI API key not found in secrets. AI features will be limited.")
        except Exception as e:
            st.warning(f"Could not initialize OpenAI: {e}")
            self.client = None
    
    def get_market_data(self, symbol, period="1d", interval="1m"):
        """
        Fetch market data using yfinance.
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            period: Data period (e.g., '1d', '5d', '1mo')
            interval: Data interval (e.g., '1m', '5m', '1h')
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            df = yf.download(symbol, period=period, interval=interval, progress=False)
            if df.empty:
                return None
            
            # Normalize column names
            df.columns = [col.lower() if isinstance(col, str) else col for col in df.columns]
            return df
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def calculate_indicators(self, df, short_ma=20, long_ma=50):
        """
        Calculate moving averages and trading signals.
        
        Args:
            df: DataFrame with OHLCV data
            short_ma: Short moving average period
            long_ma: Long moving average period
            
        Returns:
            DataFrame with indicators
        """
        if df is None or len(df) < long_ma:
            return df
        
        df['sma_short'] = df['close'].rolling(window=short_ma).mean()
        df['sma_long'] = df['close'].rolling(window=long_ma).mean()
        
        # Generate signals
        df['signal'] = 0
        df.loc[(df['sma_short'] > df['sma_long']) & 
               (df['sma_short'].shift(1) <= df['sma_long'].shift(1)), 'signal'] = 1  # Buy
        df.loc[(df['sma_short'] < df['sma_long']) & 
               (df['sma_short'].shift(1) >= df['sma_long'].shift(1)), 'signal'] = -1  # Sell
        
        return df
    
    def get_current_price(self, symbol):
        """
        Get the current price for a symbol.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Current price or None
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            st.error(f"Error getting price for {symbol}: {e}")
            return None
    
    def get_ai_advice(self, symbol, price, signal, account_balance, positions):
        """
        Get AI trading advice from OpenAI.
        
        Args:
            symbol: Trading symbol
            price: Current price
            signal: Trading signal (1=buy, -1=sell, 0=hold)
            account_balance: Current account balance
            positions: Current positions
            
        Returns:
            AI advice string
        """
        if not self.client:
            return "AI advice unavailable (no API key configured)"
        
        signal_text = "BUY" if signal == 1 else "SELL" if signal == -1 else "HOLD"
        
        prompt = f"""
As a trading advisor, analyze this situation:
- Symbol: {symbol}
- Current Price: ${price:.2f}
- Signal: {signal_text}
- Account Balance: ${account_balance:.2f}
- Open Positions: {len(positions)}

Provide brief advice (2-3 sentences) on whether to execute this trade.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert trading advisor. Provide concise, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting AI advice: {str(e)}"
    
    def run_strategy(self, symbol, levels=3, drawdown_pct=5):
        """
        Run the trading strategy for a symbol.
        
        Args:
            symbol: Trading symbol
            levels: Number of levels for strategy
            drawdown_pct: Drawdown percentage threshold
            
        Returns:
            Dictionary with strategy results and recommendations
        """
        # Fetch market data
        df = self.get_market_data(symbol, period="1d", interval="1m")
        
        if df is None or df.empty:
            return {
                'success': False,
                'error': f'Could not fetch data for {symbol}',
                'symbol': symbol
            }
        
        # Calculate indicators
        df = self.calculate_indicators(df, short_ma=20, long_ma=50)
        
        if df is None or len(df) == 0:
            return {
                'success': False,
                'error': 'Not enough data for analysis',
                'symbol': symbol
            }
        
        # Get current signal and price
        current_signal = df['signal'].iloc[-1] if 'signal' in df.columns else 0
        current_price = df['close'].iloc[-1] if 'close' in df.columns else 0
        
        # Get account info from session state
        account_balance = st.session_state.get('account_balance', 10000)
        positions = st.session_state.get('positions', {})
        
        # Get AI advice
        ai_advice = self.get_ai_advice(symbol, current_price, current_signal, 
                                       account_balance, positions)
        
        # Log activity
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'price': current_price,
            'signal': current_signal,
            'ai_advice': ai_advice
        }
        
        if 'logs' not in st.session_state:
            st.session_state.logs = []
        st.session_state.logs.append(log_entry)
        
        # Place mock trade if signal exists
        trade_placed = False
        if current_signal != 0:
            trade_placed = self.place_mock_trade(symbol, current_signal, current_price, levels)
        
        return {
            'success': True,
            'symbol': symbol,
            'price': current_price,
            'signal': current_signal,
            'ai_advice': ai_advice,
            'trade_placed': trade_placed,
            'data': df
        }
    
    def place_mock_trade(self, symbol, signal, price, levels):
        """
        Place a mock trade and update session state.
        
        Args:
            symbol: Trading symbol
            signal: Trading signal (1=buy, -1=sell)
            price: Current price
            levels: Number of levels
            
        Returns:
            True if trade was placed
        """
        if 'orders' not in st.session_state:
            st.session_state.orders = []
        
        if 'positions' not in st.session_state:
            st.session_state.positions = {}
        
        # Calculate order size based on levels
        account_balance = st.session_state.get('account_balance', 10000)
        order_size = int((account_balance * 0.1) / price)  # 10% of balance per trade
        
        order = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'side': 'BUY' if signal == 1 else 'SELL',
            'quantity': order_size,
            'price': price,
            'status': 'FILLED',
            'levels': levels
        }
        
        st.session_state.orders.append(order)
        
        # Update positions
        if symbol not in st.session_state.positions:
            st.session_state.positions[symbol] = {
                'quantity': 0,
                'avg_price': 0
            }
        
        current_pos = st.session_state.positions[symbol]
        if signal == 1:  # Buy
            total_quantity = current_pos['quantity'] + order_size
            total_cost = (current_pos['quantity'] * current_pos['avg_price']) + (order_size * price)
            current_pos['quantity'] = total_quantity
            current_pos['avg_price'] = total_cost / total_quantity if total_quantity > 0 else price
        else:  # Sell
            current_pos['quantity'] -= order_size
            if current_pos['quantity'] <= 0:
                del st.session_state.positions[symbol]
        
        return True
    
    def chat_with_ai(self, user_message):
        """
        Chat with AI Portfolio Manager.
        
        Args:
            user_message: User's message
            
        Returns:
            AI response
        """
        if not self.client:
            return "AI chat unavailable (no API key configured)"
        
        try:
            # Get context from session state
            account_balance = st.session_state.get('account_balance', 10000)
            positions = st.session_state.get('positions', {})
            
            context = f"""
Current Portfolio Context:
- Balance: ${account_balance:.2f}
- Open Positions: {len(positions)}
- Positions: {', '.join(positions.keys()) if positions else 'None'}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert AI Portfolio Manager. Provide helpful trading and investment advice."},
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in AI chat: {str(e)}"
