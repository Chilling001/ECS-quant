"""
Main Forex Trading Bot
Orchestrates all components: broker, strategy, AI, Telegram, and GUI.
"""
import os
import json
import time
import threading
from datetime import datetime
from broker_connector import OANDAConnector
from forex_strategy import MovingAverageCrossoverStrategy
from ai_manager import AIPortfolioManager
from telegram_notifier import TelegramNotifier

# Try to import config, otherwise use defaults
try:
    import config
    OANDA_API_KEY = config.OANDA_API_KEY
    OANDA_ACCOUNT_ID = config.OANDA_ACCOUNT_ID
    OANDA_PRACTICE = config.OANDA_PRACTICE
    OPENAI_API_KEY = config.OPENAI_API_KEY
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID = config.TELEGRAM_CHAT_ID
except ImportError:
    print("Warning: config.py not found. Using environment variables or defaults.")
    OANDA_API_KEY = os.getenv('OANDA_API_KEY', '')
    OANDA_ACCOUNT_ID = os.getenv('OANDA_ACCOUNT_ID', '')
    OANDA_PRACTICE = os.getenv('OANDA_PRACTICE', 'True').lower() == 'true'
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')


class ForexTradingBot:
    """
    Main Forex Trading Bot Controller.
    Manages trading logic, AI analysis, and notifications.
    """
    
    def __init__(self):
        """Initialize the trading bot."""
        self.running = False
        self.config = {}
        self.positions = {}
        self.trades = []
        self.daily_pnl = 0.0
        
        # Initialize components
        self.broker = None
        self.strategy = None
        self.ai_manager = None
        self.telegram = None
        
        # State file
        self.state_file = 'forex_bot_state.json'
        self.state = self.load_state()
        
        # Thread for market updates
        self.update_thread = None
        
    def initialize_components(self):
        """Initialize all bot components."""
        try:
            # Broker connection
            if OANDA_API_KEY and OANDA_ACCOUNT_ID:
                self.broker = OANDAConnector(
                    OANDA_API_KEY,
                    OANDA_ACCOUNT_ID,
                    OANDA_PRACTICE
                )
                print("✓ Broker connected")
            else:
                print("⚠ Warning: OANDA credentials not configured")
            
            # Strategy
            self.strategy = MovingAverageCrossoverStrategy()
            print("✓ Strategy initialized")
            
            # AI Manager
            if OPENAI_API_KEY:
                self.ai_manager = AIPortfolioManager(OPENAI_API_KEY)
                print("✓ AI Manager initialized")
            else:
                print("⚠ Warning: OpenAI API key not configured")
            
            # Telegram notifier
            if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
                print("✓ Telegram notifier initialized")
            else:
                print("⚠ Warning: Telegram credentials not configured")
            
            return True
        except Exception as e:
            print(f"✗ Error initializing components: {e}")
            return False
    
    def start(self, config=None):
        """
        Start the trading bot.
        
        Args:
            config: Trading configuration dict
        """
        if config:
            self.config = config
        else:
            self.config = self.get_default_config()
        
        print("\n" + "=" * 50)
        print("Starting Forex Trading Bot")
        print("=" * 50)
        
        # Initialize components if not already done
        if not self.broker or not self.strategy:
            if not self.initialize_components():
                print("Failed to initialize bot components")
                return
        
        # Update strategy parameters
        self.strategy.short_ma = self.config.get('short_ma', 50)
        self.strategy.long_ma = self.config.get('long_ma', 200)
        self.strategy.risk_per_trade = self.config.get('risk_per_trade', 0.01)
        self.strategy.stop_loss_pct = self.config.get('stop_loss_pct', 0.01)
        self.strategy.take_profit_pct = self.config.get('take_profit_pct', 0.02)
        
        print(f"Trading Pairs: {', '.join(self.config.get('pairs', []))}")
        print(f"Timeframe: {self.config.get('timeframe', '1h')}")
        print(f"Strategy: {self.strategy.get_strategy_summary()}")
        print("=" * 50 + "\n")
        
        # Send startup notification
        if self.telegram:
            self.telegram.send_alert('info', 'Forex Trading Bot started')
        
        # Start trading loop
        self.running = True
        self.update_thread = threading.Thread(target=self.trading_loop, daemon=True)
        self.update_thread.start()
        
        print("Bot is now running...")
    
    def stop(self):
        """Stop the trading bot."""
        print("\nStopping Forex Trading Bot...")
        self.running = False
        
        if self.telegram:
            self.telegram.send_alert('info', 'Forex Trading Bot stopped')
        
        self.save_state()
        print("Bot stopped.")
    
    def trading_loop(self):
        """Main trading loop (runs in separate thread)."""
        while self.running:
            try:
                self.process_trading_logic()
                
                # Sleep based on timeframe
                sleep_time = self.get_sleep_time()
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"Error in trading loop: {e}")
                time.sleep(60)  # Wait 1 minute on error
    
    def process_trading_logic(self):
        """Process trading logic for all pairs."""
        if not self.broker:
            return
        
        pairs = self.config.get('pairs', ['EUR/USD'])
        timeframe = self.config.get('timeframe', '1h')
        
        for pair in pairs:
            try:
                # Fetch current data
                df = self.broker.get_ohlcv(pair, timeframe, limit=250)
                
                if df.empty or len(df) < self.strategy.long_ma:
                    continue
                
                # Calculate indicators and signals
                df = self.strategy.calculate_indicators(df)
                signal = self.strategy.get_current_signal(df)
                
                current_price = df['close'].iloc[-1]
                
                # Check if we have a position
                positions = self.broker.get_positions()
                has_position = pair in positions
                
                if has_position:
                    # Manage existing position
                    position = positions[pair]
                    entry_price = position.get('entryPrice', 0)
                    side = position.get('side', 'long')
                    
                    # Check exit conditions
                    should_exit, reason = self.strategy.check_exit_conditions(
                        df, entry_price, side
                    )
                    
                    if should_exit:
                        print(f"Exiting {pair}: {reason}")
                        self.close_position(pair, reason)
                
                else:
                    # Look for entry signal
                    if signal == 1:  # Buy signal
                        print(f"Buy signal for {pair} at {current_price:.5f}")
                        self.open_position(pair, 'buy', current_price, df)
                    
                    elif signal == -1:  # Sell signal
                        print(f"Sell signal for {pair} at {current_price:.5f}")
                        self.open_position(pair, 'sell', current_price, df)
                
            except Exception as e:
                print(f"Error processing {pair}: {e}")
                continue
        
        # Periodic AI analysis
        if self.should_run_ai_analysis():
            self.run_ai_analysis()
    
    def open_position(self, pair, side, entry_price, df):
        """
        Open a new position.
        
        Args:
            pair: Trading pair
            side: 'buy' or 'sell'
            entry_price: Entry price
            df: DataFrame with current data
        """
        if not self.broker:
            return
        
        try:
            # Get account balance
            balance_info = self.broker.get_balance()
            balance = balance_info.get('free', 0)
            
            # Calculate position size
            stop_loss = self.strategy.calculate_stop_loss(entry_price, 'long' if side == 'buy' else 'short')
            position_size = self.strategy.calculate_position_size(balance, entry_price, stop_loss)
            
            if position_size <= 0:
                print(f"Position size too small for {pair}")
                return
            
            # Calculate take profit
            take_profit = self.strategy.calculate_take_profit(entry_price, 'long' if side == 'buy' else 'short')
            
            # Execute order
            order = self.broker.create_market_order(pair, side, position_size)
            
            if order:
                # Send notifications
                if self.telegram:
                    self.telegram.send_trade_entry(
                        pair, side, position_size, entry_price, stop_loss, take_profit
                    )
                
                # Log trade
                self.log_trade({
                    'timestamp': datetime.now().isoformat(),
                    'symbol': pair,
                    'side': side,
                    'size': position_size,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'status': 'open'
                })
                
                print(f"Position opened: {side} {position_size} {pair} @ {entry_price:.5f}")
                
        except Exception as e:
            print(f"Error opening position for {pair}: {e}")
    
    def close_position(self, pair, reason=""):
        """
        Close an existing position.
        
        Args:
            pair: Trading pair
            reason: Reason for closing
        """
        if not self.broker:
            return
        
        try:
            # Get position details
            positions = self.broker.get_positions()
            if pair not in positions:
                return
            
            position = positions[pair]
            
            # Close position
            result = self.broker.close_position(pair)
            
            if result:
                # Calculate P&L (simplified)
                entry_price = position.get('entryPrice', 0)
                current_price = self.broker.get_ticker(pair)['last'] if self.broker.get_ticker(pair) else 0
                size = position.get('contracts', 0)
                
                pnl = (current_price - entry_price) * size
                
                # Send notifications
                if self.telegram:
                    self.telegram.send_trade_exit(
                        pair, position.get('side', 'long'), size, current_price, pnl
                    )
                
                # Log trade
                self.log_trade({
                    'timestamp': datetime.now().isoformat(),
                    'symbol': pair,
                    'exit_price': current_price,
                    'pnl': pnl,
                    'reason': reason,
                    'status': 'closed'
                })
                
                self.daily_pnl += pnl
                
                print(f"Position closed: {pair}, P&L: ${pnl:.2f}, Reason: {reason}")
                
        except Exception as e:
            print(f"Error closing position for {pair}: {e}")
    
    def should_run_ai_analysis(self):
        """Check if it's time to run AI analysis."""
        last_analysis = self.state.get('last_ai_analysis', 0)
        current_time = time.time()
        
        # Run analysis every hour
        return (current_time - last_analysis) > 3600
    
    def run_ai_analysis(self):
        """Run AI portfolio analysis."""
        if not self.ai_manager or not self.broker:
            return
        
        try:
            account_info = self.broker.get_account_info()
            positions = self.broker.get_positions()
            
            analysis = self.ai_manager.analyze_portfolio(
                account_info, positions, self.trades[-10:]
            )
            
            print(f"\n--- AI Analysis ---\n{analysis}\n" + "-" * 50 + "\n")
            
            # Send to Telegram
            if self.telegram:
                self.telegram.send_ai_insight(analysis)
            
            # Update state
            self.state['last_ai_analysis'] = time.time()
            self.save_state()
            
        except Exception as e:
            print(f"Error running AI analysis: {e}")
    
    def query_ai(self, message):
        """
        Query AI assistant.
        
        Args:
            message: User message
            
        Returns:
            AI response
        """
        if not self.ai_manager:
            return "AI Manager not initialized"
        
        try:
            # Get context
            context = {}
            if self.broker:
                context['account'] = self.broker.get_account_info()
                context['positions'] = self.broker.get_positions()
            
            response = self.ai_manager.chat_query(message, context)
            return response
        except Exception as e:
            return f"Error querying AI: {str(e)}"
    
    def get_sleep_time(self):
        """Get sleep time based on timeframe."""
        timeframe = self.config.get('timeframe', '1h')
        
        timeframe_map = {
            '5m': 30,    # Check every 30 seconds
            '15m': 60,   # Check every minute
            '30m': 120,  # Check every 2 minutes
            '1h': 300,   # Check every 5 minutes
            '4h': 600,   # Check every 10 minutes
            '1d': 1800   # Check every 30 minutes
        }
        
        return timeframe_map.get(timeframe, 300)
    
    def get_default_config(self):
        """Get default configuration."""
        return {
            'pairs': ['EUR/USD', 'GBP/USD', 'USD/JPY'],
            'short_ma': 50,
            'long_ma': 200,
            'timeframe': '1h',
            'risk_per_trade': 0.01,
            'stop_loss_pct': 0.01,
            'take_profit_pct': 0.02,
            'max_drawdown': 0.10
        }
    
    def save_configuration(self, config):
        """Save configuration to state."""
        self.config = config
        self.state['config'] = config
        self.save_state()
    
    def log_trade(self, trade_data):
        """Log trade to history."""
        self.trades.append(trade_data)
        
        # Keep only last 100 trades in memory
        if len(self.trades) > 100:
            self.trades = self.trades[-100:]
    
    def load_state(self):
        """Load bot state from file."""
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {
                'last_ai_analysis': 0,
                'config': {},
                'trades': []
            }
    
    def save_state(self):
        """Save bot state to file."""
        try:
            self.state['trades'] = self.trades[-50:]  # Save last 50 trades
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def get_dashboard_data(self):
        """Get data for dashboard display."""
        data = {
            'balance': 0,
            'positions_count': 0,
            'daily_pnl': self.daily_pnl,
            'positions': [],
            'recent_trades': []
        }
        
        if self.broker:
            balance_info = self.broker.get_balance()
            data['balance'] = balance_info.get('total', 0)
            
            positions = self.broker.get_positions()
            data['positions_count'] = len(positions)
            
            # Format positions for display
            for symbol, pos in positions.items():
                data['positions'].append((
                    symbol,
                    pos.get('side', 'N/A'),
                    pos.get('contracts', 0),
                    pos.get('entryPrice', 0),
                    pos.get('currentPrice', 0),
                    pos.get('unrealizedPL', 0)
                ))
        
        # Format recent trades
        for trade in self.trades[-10:]:
            if trade.get('status') == 'closed':
                data['recent_trades'].append((
                    trade.get('timestamp', ''),
                    trade.get('symbol', ''),
                    trade.get('side', ''),
                    trade.get('size', 0),
                    trade.get('entry_price', 0),
                    trade.get('exit_price', 0),
                    trade.get('pnl', 0)
                ))
        
        return data


def main():
    """Main entry point."""
    print("=" * 60)
    print("AI-Powered Forex Trading Bot")
    print("=" * 60)
    print("\nInitializing bot...")
    
    # Create bot instance
    bot = ForexTradingBot()
    
    # Initialize components
    if not bot.initialize_components():
        print("\nFailed to initialize. Please check your configuration.")
        print("Make sure to:")
        print("1. Copy config_template.py to config.py")
        print("2. Fill in your API keys and credentials")
        return
    
    print("\nBot initialized successfully!")
    print("Starting GUI...")
    
    # Import and start GUI
    try:
        from forex_gui import ForexBotGUI
        gui = ForexBotGUI(bot)
        gui.run()
    except ImportError as e:
        print(f"\nGUI not available: {e}")
        print("Running in console mode...")
        
        # Console mode
        bot.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutdown signal received")
            bot.stop()


if __name__ == '__main__':
    main()
