"""
Forex Strategy Module
Implements Moving Average Crossover Strategy for forex trading.
"""
import pandas as pd
import numpy as np
from datetime import datetime


class MovingAverageCrossoverStrategy:
    """
    Moving Average Crossover Strategy for Forex.
    
    Strategy Rules:
    - Buy when short MA crosses above long MA
    - Sell when short MA crosses below long MA
    - 1% risk per trade
    - Stop-loss at 1% below entry
    - Take-profit at 2% above entry
    """
    
    def __init__(self, short_ma=50, long_ma=200, risk_per_trade=0.01, 
                 stop_loss_pct=0.01, take_profit_pct=0.02):
        """
        Initialize strategy parameters.
        
        Args:
            short_ma: Short moving average period (default: 50)
            long_ma: Long moving average period (default: 200)
            risk_per_trade: Risk per trade as percentage (default: 0.01 = 1%)
            stop_loss_pct: Stop-loss percentage (default: 0.01 = 1%)
            take_profit_pct: Take-profit percentage (default: 0.02 = 2%)
        """
        self.short_ma = short_ma
        self.long_ma = long_ma
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
        self.signals = {}
        self.positions = {}
        
    def calculate_indicators(self, df):
        """
        Calculate moving averages and generate signals.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with indicators and signals
        """
        if df is None or len(df) < self.long_ma:
            return df
        
        # Calculate Simple Moving Averages
        df['sma_short'] = df['close'].rolling(window=self.short_ma).mean()
        df['sma_long'] = df['close'].rolling(window=self.long_ma).mean()
        
        # Generate signals: 1 for buy, -1 for sell, 0 for hold
        df['signal'] = 0
        
        # Buy signal: short MA crosses above long MA
        df.loc[(df['sma_short'] > df['sma_long']) & 
               (df['sma_short'].shift(1) <= df['sma_long'].shift(1)), 'signal'] = 1
        
        # Sell signal: short MA crosses below long MA
        df.loc[(df['sma_short'] < df['sma_long']) & 
               (df['sma_short'].shift(1) >= df['sma_long'].shift(1)), 'signal'] = -1
        
        return df
    
    def get_current_signal(self, df):
        """
        Get the most recent trading signal.
        
        Args:
            df: DataFrame with indicators
            
        Returns:
            Signal: 1 (buy), -1 (sell), 0 (hold)
        """
        if df is None or len(df) == 0:
            return 0
        
        return df['signal'].iloc[-1]
    
    def calculate_position_size(self, balance, entry_price, stop_loss_price):
        """
        Calculate position size based on risk management.
        
        Args:
            balance: Account balance
            entry_price: Entry price for the trade
            stop_loss_price: Stop-loss price
            
        Returns:
            Position size in units
        """
        if stop_loss_price >= entry_price:
            return 0
        
        risk_amount = balance * self.risk_per_trade
        risk_per_unit = entry_price - stop_loss_price
        
        if risk_per_unit <= 0:
            return 0
        
        position_size = risk_amount / risk_per_unit
        return position_size
    
    def calculate_stop_loss(self, entry_price, side='long'):
        """
        Calculate stop-loss price.
        
        Args:
            entry_price: Entry price
            side: 'long' or 'short'
            
        Returns:
            Stop-loss price
        """
        if side == 'long':
            return entry_price * (1 - self.stop_loss_pct)
        else:
            return entry_price * (1 + self.stop_loss_pct)
    
    def calculate_take_profit(self, entry_price, side='long'):
        """
        Calculate take-profit price.
        
        Args:
            entry_price: Entry price
            side: 'long' or 'short'
            
        Returns:
            Take-profit price
        """
        if side == 'long':
            return entry_price * (1 + self.take_profit_pct)
        else:
            return entry_price * (1 - self.take_profit_pct)
    
    def check_exit_conditions(self, df, position_entry_price, position_side):
        """
        Check if exit conditions are met.
        
        Args:
            df: DataFrame with current data
            position_entry_price: Entry price of position
            position_side: 'long' or 'short'
            
        Returns:
            tuple: (should_exit, reason)
        """
        if df is None or len(df) == 0:
            return False, ""
        
        current_price = df['close'].iloc[-1]
        stop_loss = self.calculate_stop_loss(position_entry_price, position_side)
        take_profit = self.calculate_take_profit(position_entry_price, position_side)
        
        # Check stop-loss
        if position_side == 'long' and current_price <= stop_loss:
            return True, "Stop-loss hit"
        elif position_side == 'short' and current_price >= stop_loss:
            return True, "Stop-loss hit"
        
        # Check take-profit
        if position_side == 'long' and current_price >= take_profit:
            return True, "Take-profit hit"
        elif position_side == 'short' and current_price <= take_profit:
            return True, "Take-profit hit"
        
        # Check reverse signal
        current_signal = self.get_current_signal(df)
        if position_side == 'long' and current_signal == -1:
            return True, "Reverse signal (sell)"
        elif position_side == 'short' and current_signal == 1:
            return True, "Reverse signal (buy)"
        
        return False, ""
    
    def get_strategy_summary(self):
        """Get a summary of strategy parameters."""
        return {
            'name': 'Moving Average Crossover',
            'short_ma': self.short_ma,
            'long_ma': self.long_ma,
            'risk_per_trade': f"{self.risk_per_trade * 100}%",
            'stop_loss': f"{self.stop_loss_pct * 100}%",
            'take_profit': f"{self.take_profit_pct * 100}%"
        }
