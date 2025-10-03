"""
Broker Connector Module
Handles connection to OANDA broker via CCXT library for forex trading.
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time


class OANDAConnector:
    """Connects to OANDA broker using CCXT library."""
    
    def __init__(self, api_key, account_id, practice=True):
        """
        Initialize OANDA connection.
        
        Args:
            api_key: OANDA API key
            account_id: OANDA account ID
            practice: True for practice account, False for live
        """
        self.api_key = api_key
        self.account_id = account_id
        self.practice = practice
        
        # Initialize CCXT OANDA exchange
        self.exchange = ccxt.oanda({
            'apiKey': api_key,
            'accountId': account_id,
            'practice': practice,
        })
        
        self.positions = {}
        self.orders = []
        
    def get_balance(self):
        """Get account balance."""
        try:
            balance = self.exchange.fetch_balance()
            return {
                'total': balance.get('total', {}).get('USD', 0),
                'free': balance.get('free', {}).get('USD', 0),
                'used': balance.get('used', {}).get('USD', 0)
            }
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {'total': 0, 'free': 0, 'used': 0}
    
    def get_positions(self):
        """Get current open positions."""
        try:
            positions = self.exchange.fetch_positions()
            self.positions = {pos['symbol']: pos for pos in positions if pos['contracts'] != 0}
            return self.positions
        except Exception as e:
            print(f"Error fetching positions: {e}")
            return {}
    
    def get_ohlcv(self, symbol, timeframe='1h', limit=500):
        """
        Fetch OHLCV (candlestick) data for a forex pair.
        
        Args:
            symbol: Trading pair (e.g., 'EUR/USD')
            timeframe: Timeframe (e.g., '1h', '4h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Fetch OHLCV data
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
        except Exception as e:
            print(f"Error fetching OHLCV data for {symbol}: {e}")
            return pd.DataFrame()
    
    def create_market_order(self, symbol, side, amount):
        """
        Create a market order.
        
        Args:
            symbol: Trading pair (e.g., 'EUR/USD')
            side: 'buy' or 'sell'
            amount: Order size (in base currency units)
            
        Returns:
            Order info dict
        """
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            self.orders.append(order)
            print(f"Market order created: {side} {amount} {symbol}")
            return order
        except Exception as e:
            print(f"Error creating market order: {e}")
            return None
    
    def create_limit_order(self, symbol, side, amount, price):
        """
        Create a limit order.
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Order size
            price: Limit price
            
        Returns:
            Order info dict
        """
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            self.orders.append(order)
            print(f"Limit order created: {side} {amount} {symbol} @ {price}")
            return order
        except Exception as e:
            print(f"Error creating limit order: {e}")
            return None
    
    def create_stop_loss_order(self, symbol, side, amount, stop_price):
        """
        Create a stop-loss order.
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell' (opposite of position)
            amount: Order size
            stop_price: Stop price
            
        Returns:
            Order info dict
        """
        try:
            params = {'stopPrice': stop_price}
            order = self.exchange.create_order(symbol, 'stop', side, amount, stop_price, params)
            self.orders.append(order)
            print(f"Stop-loss order created: {side} {amount} {symbol} @ {stop_price}")
            return order
        except Exception as e:
            print(f"Error creating stop-loss order: {e}")
            return None
    
    def cancel_order(self, order_id, symbol):
        """Cancel an order."""
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            print(f"Order {order_id} cancelled")
            return result
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return None
    
    def close_position(self, symbol):
        """Close a position entirely."""
        try:
            positions = self.get_positions()
            if symbol in positions:
                pos = positions[symbol]
                side = 'sell' if pos['side'] == 'long' else 'buy'
                amount = abs(pos['contracts'])
                return self.create_market_order(symbol, side, amount)
            else:
                print(f"No open position for {symbol}")
                return None
        except Exception as e:
            print(f"Error closing position: {e}")
            return None
    
    def get_ticker(self, symbol):
        """Get current ticker/price for a symbol."""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching ticker for {symbol}: {e}")
            return None
    
    def get_account_info(self):
        """Get detailed account information."""
        try:
            balance = self.get_balance()
            positions = self.get_positions()
            
            return {
                'balance': balance,
                'positions': positions,
                'account_id': self.account_id,
                'practice': self.practice,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching account info: {e}")
            return {}
