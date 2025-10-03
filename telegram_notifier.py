"""
Telegram Notifier Module
Sends trading notifications via Telegram bot.
"""
import threading
import requests
from datetime import datetime


class TelegramNotifier:
    """
    Send trading notifications via Telegram.
    Uses python-telegram-bot library for sending messages.
    """
    
    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message, async_send=True):
        """
        Send a message via Telegram.
        
        Args:
            message: Message text to send
            async_send: If True, send asynchronously (non-blocking)
        """
        if async_send:
            thread = threading.Thread(target=self._send_sync, args=(message,), daemon=True)
            thread.start()
        else:
            self._send_sync(message)
    
    def _send_sync(self, message):
        """Send message synchronously."""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code != 200:
                print(f"Telegram send failed: {response.status_code}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
    
    def send_trade_entry(self, symbol, side, amount, entry_price, stop_loss, take_profit):
        """
        Send trade entry notification.
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Position size
            entry_price: Entry price
            stop_loss: Stop-loss price
            take_profit: Take-profit price
        """
        emoji = "🟢" if side.lower() == 'buy' else "🔴"
        message = f"""
{emoji} <b>TRADE ENTRY</b>

<b>Symbol:</b> {symbol}
<b>Side:</b> {side.upper()}
<b>Amount:</b> {amount:.2f} units
<b>Entry:</b> {entry_price:.5f}
<b>Stop Loss:</b> {stop_loss:.5f}
<b>Take Profit:</b> {take_profit:.5f}

<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        self.send_message(message)
    
    def send_trade_exit(self, symbol, side, amount, exit_price, pnl):
        """
        Send trade exit notification.
        
        Args:
            symbol: Trading pair
            side: 'buy' or 'sell'
            amount: Position size
            exit_price: Exit price
            pnl: Profit/Loss
        """
        emoji = "✅" if pnl >= 0 else "❌"
        pnl_sign = "+" if pnl >= 0 else ""
        
        message = f"""
{emoji} <b>TRADE EXIT</b>

<b>Symbol:</b> {symbol}
<b>Side:</b> {side.upper()}
<b>Amount:</b> {amount:.2f} units
<b>Exit:</b> {exit_price:.5f}
<b>P&L:</b> {pnl_sign}${pnl:.2f}

<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        self.send_message(message)
    
    def send_alert(self, alert_type, message):
        """
        Send general alert.
        
        Args:
            alert_type: Type of alert ('info', 'warning', 'error')
            message: Alert message
        """
        emoji_map = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '🚨'
        }
        
        emoji = emoji_map.get(alert_type.lower(), 'ℹ️')
        formatted_message = f"""
{emoji} <b>{alert_type.upper()}</b>

{message}

<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        self.send_message(formatted_message)
    
    def send_daily_summary(self, balance, positions, daily_pnl, trade_count):
        """
        Send daily trading summary.
        
        Args:
            balance: Current account balance
            positions: Number of open positions
            daily_pnl: Daily profit/loss
            trade_count: Number of trades today
        """
        pnl_sign = "+" if daily_pnl >= 0 else ""
        emoji = "📈" if daily_pnl >= 0 else "📉"
        
        message = f"""
{emoji} <b>DAILY SUMMARY</b>

<b>Balance:</b> ${balance:.2f}
<b>Open Positions:</b> {positions}
<b>Daily P&L:</b> {pnl_sign}${daily_pnl:.2f}
<b>Trades Today:</b> {trade_count}

<i>{datetime.now().strftime('%Y-%m-%d')}</i>
"""
        self.send_message(message)
    
    def send_ai_insight(self, insight):
        """
        Send AI-generated insight.
        
        Args:
            insight: AI insight text
        """
        message = f"""
🤖 <b>AI PORTFOLIO INSIGHT</b>

{insight}

<i>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        self.send_message(message)
