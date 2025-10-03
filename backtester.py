"""
Backtesting Module
Backtest forex strategies using historical OANDA data with Backtrader.
"""
import backtrader as bt
import pandas as pd
from datetime import datetime
import math


class ForexStrategy(bt.Strategy):
    """
    Backtrader strategy for forex trading with moving average crossover.
    """
    
    params = (
        ('short_ma', 50),
        ('long_ma', 200),
        ('risk_per_trade', 0.01),
        ('stop_loss_pct', 0.01),
        ('take_profit_pct', 0.02),
    )
    
    def __init__(self):
        """Initialize strategy."""
        # Moving averages
        self.sma_short = bt.indicators.SMA(self.data.close, period=self.p.short_ma)
        self.sma_long = bt.indicators.SMA(self.data.close, period=self.p.long_ma)
        
        # Crossover indicator
        self.crossover = bt.indicators.CrossOver(self.sma_short, self.sma_long)
        
        # Track orders and positions
        self.order = None
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        
        # Statistics
        self.trades = []
        
    def log(self, txt, dt=None):
        """Log messages."""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')
    
    def notify_order(self, order):
        """Notification when order is executed."""
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.5f}')
                self.entry_price = order.executed.price
                self.stop_loss = self.entry_price * (1 - self.p.stop_loss_pct)
                self.take_profit = self.entry_price * (1 + self.p.take_profit_pct)
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.5f}')
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None
    
    def notify_trade(self, trade):
        """Notification when trade is closed."""
        if trade.isclosed:
            self.log(f'TRADE CLOSED, P&L: Gross ${trade.pnl:.2f}, Net ${trade.pnlcomm:.2f}')
            
            self.trades.append({
                'date': self.datas[0].datetime.date(0),
                'pnl': trade.pnl,
                'pnl_net': trade.pnlcomm
            })
    
    def next(self):
        """Strategy logic executed on each bar."""
        # Skip if order is pending
        if self.order:
            return
        
        # Check if we are in the market
        if not self.position:
            # Entry signal: short MA crosses above long MA
            if self.crossover > 0:
                # Calculate position size based on risk
                cash = self.broker.getcash()
                entry_price = self.data.close[0]
                stop_loss = entry_price * (1 - self.p.stop_loss_pct)
                risk_per_unit = entry_price - stop_loss
                
                if risk_per_unit > 0:
                    risk_amount = cash * self.p.risk_per_trade
                    size = math.floor(risk_amount / risk_per_unit)
                    
                    if size > 0:
                        self.log(f'BUY CREATE, Price: {entry_price:.5f}, Size: {size}')
                        self.order = self.buy(size=size)
        else:
            # Exit conditions
            current_price = self.data.close[0]
            
            # Stop loss hit
            if self.stop_loss and current_price <= self.stop_loss:
                self.log(f'STOP LOSS HIT at {current_price:.5f}')
                self.order = self.close()
            
            # Take profit hit
            elif self.take_profit and current_price >= self.take_profit:
                self.log(f'TAKE PROFIT HIT at {current_price:.5f}')
                self.order = self.close()
            
            # Reverse signal: short MA crosses below long MA
            elif self.crossover < 0:
                self.log(f'REVERSE SIGNAL, Closing at {current_price:.5f}')
                self.order = self.close()


class ForexBacktester:
    """
    Backtester for forex strategies using historical data.
    """
    
    def __init__(self):
        """Initialize backtester."""
        self.cerebro = None
        self.results = {}
        
    def prepare_data(self, df):
        """
        Prepare DataFrame for Backtrader.
        
        Args:
            df: DataFrame with OHLCV data (timestamp as index)
            
        Returns:
            Backtrader data feed
        """
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Create Backtrader data feed
        data = bt.feeds.PandasData(dataname=df)
        return data
    
    def run_backtest(self, data_df, initial_cash=10000, short_ma=50, long_ma=200,
                     risk_per_trade=0.01, stop_loss_pct=0.01, take_profit_pct=0.02):
        """
        Run backtest with given parameters.
        
        Args:
            data_df: DataFrame with OHLCV data
            initial_cash: Initial capital
            short_ma: Short MA period
            long_ma: Long MA period
            risk_per_trade: Risk per trade (fraction)
            stop_loss_pct: Stop-loss percentage
            take_profit_pct: Take-profit percentage
            
        Returns:
            dict with backtest results
        """
        # Initialize Cerebro
        self.cerebro = bt.Cerebro()
        
        # Add data
        data = self.prepare_data(data_df)
        self.cerebro.adddata(data)
        
        # Add strategy
        self.cerebro.addstrategy(
            ForexStrategy,
            short_ma=short_ma,
            long_ma=long_ma,
            risk_per_trade=risk_per_trade,
            stop_loss_pct=stop_loss_pct,
            take_profit_pct=take_profit_pct
        )
        
        # Set broker parameters
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=0.0001)  # 0.01% commission (typical for forex)
        
        # Add analyzers
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        
        # Run backtest
        print(f"Starting Portfolio Value: ${self.cerebro.broker.getvalue():.2f}")
        
        strategies = self.cerebro.run()
        strategy = strategies[0]
        
        final_value = self.cerebro.broker.getvalue()
        print(f"Final Portfolio Value: ${final_value:.2f}")
        
        # Extract results
        self.results = {
            'initial_value': initial_cash,
            'final_value': final_value,
            'profit': final_value - initial_cash,
            'return_pct': ((final_value - initial_cash) / initial_cash) * 100,
            'sharpe_ratio': strategy.analyzers.sharpe.get_analysis().get('sharperatio', 0),
            'max_drawdown': strategy.analyzers.drawdown.get_analysis().get('max', {}).get('drawdown', 0),
            'total_trades': strategy.analyzers.trades.get_analysis().get('total', {}).get('total', 0),
            'won_trades': strategy.analyzers.trades.get_analysis().get('won', {}).get('total', 0),
            'lost_trades': strategy.analyzers.trades.get_analysis().get('lost', {}).get('total', 0),
        }
        
        # Calculate win rate
        total = self.results['total_trades']
        if total > 0:
            self.results['win_rate'] = (self.results['won_trades'] / total) * 100
        else:
            self.results['win_rate'] = 0
        
        return self.results
    
    def print_results(self):
        """Print backtest results."""
        if not self.results:
            print("No backtest results available")
            return
        
        print("\n" + "=" * 50)
        print("BACKTEST RESULTS")
        print("=" * 50)
        print(f"Initial Capital:    ${self.results['initial_value']:.2f}")
        print(f"Final Value:        ${self.results['final_value']:.2f}")
        print(f"Total Profit:       ${self.results['profit']:.2f}")
        print(f"Return:             {self.results['return_pct']:.2f}%")
        print(f"Max Drawdown:       {self.results['max_drawdown']:.2f}%")
        print(f"Sharpe Ratio:       {self.results['sharpe_ratio']:.3f}")
        print("-" * 50)
        print(f"Total Trades:       {self.results['total_trades']}")
        print(f"Winning Trades:     {self.results['won_trades']}")
        print(f"Losing Trades:      {self.results['lost_trades']}")
        print(f"Win Rate:           {self.results['win_rate']:.2f}%")
        print("=" * 50 + "\n")
    
    def plot_results(self):
        """Plot backtest results."""
        if self.cerebro:
            self.cerebro.plot(style='candlestick')


def run_sample_backtest(broker_connector, symbol='EUR/USD', timeframe='1h'):
    """
    Run a sample backtest with historical data from OANDA.
    
    Args:
        broker_connector: OANDAConnector instance
        symbol: Trading pair
        timeframe: Timeframe for data
    """
    print(f"Fetching historical data for {symbol}...")
    df = broker_connector.get_ohlcv(symbol, timeframe, limit=500)
    
    if df.empty:
        print("Failed to fetch data")
        return
    
    print(f"Data fetched: {len(df)} candles from {df.index[0]} to {df.index[-1]}")
    
    # Run backtest
    backtester = ForexBacktester()
    results = backtester.run_backtest(df, initial_cash=10000)
    backtester.print_results()
    
    return results
