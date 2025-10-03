"""
Forex Bot GUI Module
Tkinter-based graphical user interface for the forex trading bot.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading


class ForexBotGUI:
    """
    Tkinter GUI for Forex Trading Bot.
    Includes user inputs, status display, and AI chat interface.
    """
    
    def __init__(self, bot_controller):
        """
        Initialize GUI.
        
        Args:
            bot_controller: Reference to main bot controller
        """
        self.bot = bot_controller
        self.root = tk.Tk()
        self.root.title("AI Forex Trading Bot")
        self.root.geometry("1000x700")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Trading Configuration
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuration")
        self.setup_config_tab(config_frame)
        
        # Tab 2: Dashboard
        dashboard_frame = ttk.Frame(notebook)
        notebook.add(dashboard_frame, text="Dashboard")
        self.setup_dashboard_tab(dashboard_frame)
        
        # Tab 3: AI Chat
        chat_frame = ttk.Frame(notebook)
        notebook.add(chat_frame, text="AI Assistant")
        self.setup_chat_tab(chat_frame)
        
        # Tab 4: Logs
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="Logs")
        self.setup_logs_tab(logs_frame)
        
    def setup_config_tab(self, parent):
        """Setup configuration tab."""
        # Trading pairs
        ttk.Label(parent, text="Trading Pairs:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.pairs_entry = ttk.Entry(parent, width=40)
        self.pairs_entry.insert(0, "EUR/USD,GBP/USD,USD/JPY")
        self.pairs_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Short MA
        ttk.Label(parent, text="Short MA Period:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.short_ma_entry = ttk.Entry(parent, width=20)
        self.short_ma_entry.insert(0, "50")
        self.short_ma_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # Long MA
        ttk.Label(parent, text="Long MA Period:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.long_ma_entry = ttk.Entry(parent, width=20)
        self.long_ma_entry.insert(0, "200")
        self.long_ma_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        # Timeframe
        ttk.Label(parent, text="Timeframe:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.timeframe_var = tk.StringVar(value="1h")
        timeframe_combo = ttk.Combobox(parent, textvariable=self.timeframe_var, values=["5m", "15m", "30m", "1h", "4h", "1d"], width=17)
        timeframe_combo.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        # Risk per trade
        ttk.Label(parent, text="Risk per Trade (%):", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.risk_entry = ttk.Entry(parent, width=20)
        self.risk_entry.insert(0, "1.0")
        self.risk_entry.grid(row=4, column=1, sticky='w', padx=10, pady=5)
        
        # Stop loss
        ttk.Label(parent, text="Stop Loss (%):", font=('Arial', 10, 'bold')).grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.sl_entry = ttk.Entry(parent, width=20)
        self.sl_entry.insert(0, "1.0")
        self.sl_entry.grid(row=5, column=1, sticky='w', padx=10, pady=5)
        
        # Take profit
        ttk.Label(parent, text="Take Profit (%):", font=('Arial', 10, 'bold')).grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.tp_entry = ttk.Entry(parent, width=20)
        self.tp_entry.insert(0, "2.0")
        self.tp_entry.grid(row=6, column=1, sticky='w', padx=10, pady=5)
        
        # Max drawdown
        ttk.Label(parent, text="Max Drawdown (%):", font=('Arial', 10, 'bold')).grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.drawdown_entry = ttk.Entry(parent, width=20)
        self.drawdown_entry.insert(0, "10.0")
        self.drawdown_entry.grid(row=7, column=1, sticky='w', padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="Start Bot", command=self.start_bot, width=15)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Bot", command=self.stop_bot, state='disabled', width=15)
        self.stop_btn.pack(side='left', padx=5)
        
        self.save_config_btn = ttk.Button(button_frame, text="Save Config", command=self.save_config, width=15)
        self.save_config_btn.pack(side='left', padx=5)
        
    def setup_dashboard_tab(self, parent):
        """Setup dashboard tab."""
        # Account info frame
        account_frame = ttk.LabelFrame(parent, text="Account Information", padding=10)
        account_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(account_frame, text="Balance:").grid(row=0, column=0, sticky='w')
        self.balance_label = ttk.Label(account_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.balance_label.grid(row=0, column=1, sticky='w', padx=10)
        
        ttk.Label(account_frame, text="Open Positions:").grid(row=1, column=0, sticky='w')
        self.positions_label = ttk.Label(account_frame, text="0")
        self.positions_label.grid(row=1, column=1, sticky='w', padx=10)
        
        ttk.Label(account_frame, text="Daily P&L:").grid(row=2, column=0, sticky='w')
        self.pnl_label = ttk.Label(account_frame, text="$0.00")
        self.pnl_label.grid(row=2, column=1, sticky='w', padx=10)
        
        # Positions frame
        positions_frame = ttk.LabelFrame(parent, text="Open Positions", padding=10)
        positions_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for positions
        columns = ('Symbol', 'Side', 'Size', 'Entry', 'Current', 'P&L')
        self.positions_tree = ttk.Treeview(positions_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=100)
        
        self.positions_tree.pack(fill='both', expand=True)
        
        # Recent trades frame
        trades_frame = ttk.LabelFrame(parent, text="Recent Trades", padding=10)
        trades_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Time', 'Symbol', 'Side', 'Size', 'Entry', 'Exit', 'P&L')
        self.trades_tree = ttk.Treeview(trades_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.trades_tree.heading(col, text=col)
            self.trades_tree.column(col, width=100)
        
        self.trades_tree.pack(fill='both', expand=True)
        
        # Status bar
        self.status_label = ttk.Label(parent, text="Status: Idle", relief='sunken')
        self.status_label.pack(fill='x', side='bottom', padx=10, pady=5)
        
    def setup_chat_tab(self, parent):
        """Setup AI chat tab."""
        # Chat history
        chat_frame = ttk.LabelFrame(parent, text="AI Assistant Chat", padding=10)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20)
        self.chat_display.pack(fill='both', expand=True)
        self.chat_display.config(state='disabled')
        
        # Input frame
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(input_frame, text="Your question:").pack(side='left', padx=5)
        
        self.chat_input = ttk.Entry(input_frame)
        self.chat_input.pack(side='left', fill='x', expand=True, padx=5)
        self.chat_input.bind('<Return>', lambda e: self.send_chat_message())
        
        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_chat_message)
        self.send_btn.pack(side='left', padx=5)
        
        # Quick actions
        quick_frame = ttk.Frame(parent)
        quick_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(quick_frame, text="Quick queries:").pack(side='left', padx=5)
        
        ttk.Button(quick_frame, text="Analyze Portfolio", 
                  command=lambda: self.quick_query("Analyze my current portfolio")).pack(side='left', padx=2)
        ttk.Button(quick_frame, text="Risk Assessment", 
                  command=lambda: self.quick_query("Assess the risk of my positions")).pack(side='left', padx=2)
        ttk.Button(quick_frame, text="Suggestions", 
                  command=lambda: self.quick_query("What are your suggestions for my trading?")).pack(side='left', padx=2)
        
    def setup_logs_tab(self, parent):
        """Setup logs tab."""
        log_frame = ttk.LabelFrame(parent, text="System Logs", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_display = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_display.pack(fill='both', expand=True)
        
        # Clear logs button
        clear_btn = ttk.Button(parent, text="Clear Logs", command=self.clear_logs)
        clear_btn.pack(pady=5)
        
    def start_bot(self):
        """Start the trading bot."""
        try:
            # Get configuration from GUI
            config = self.get_config()
            
            # Start bot in separate thread
            threading.Thread(target=self.bot.start, args=(config,), daemon=True).start()
            
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.update_status("Bot started")
            self.log_message("Bot started with configuration")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")
    
    def stop_bot(self):
        """Stop the trading bot."""
        try:
            self.bot.stop()
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.update_status("Bot stopped")
            self.log_message("Bot stopped by user")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop bot: {str(e)}")
    
    def save_config(self):
        """Save configuration."""
        try:
            config = self.get_config()
            self.bot.save_configuration(config)
            messagebox.showinfo("Success", "Configuration saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def get_config(self):
        """Get configuration from GUI inputs."""
        return {
            'pairs': [p.strip() for p in self.pairs_entry.get().split(',')],
            'short_ma': int(self.short_ma_entry.get()),
            'long_ma': int(self.long_ma_entry.get()),
            'timeframe': self.timeframe_var.get(),
            'risk_per_trade': float(self.risk_entry.get()) / 100,
            'stop_loss_pct': float(self.sl_entry.get()) / 100,
            'take_profit_pct': float(self.tp_entry.get()) / 100,
            'max_drawdown': float(self.drawdown_entry.get()) / 100
        }
    
    def send_chat_message(self):
        """Send message to AI assistant."""
        message = self.chat_input.get().strip()
        if not message:
            return
        
        self.append_chat(f"You: {message}\n")
        self.chat_input.delete(0, tk.END)
        
        # Get AI response in separate thread
        threading.Thread(target=self._get_ai_response, args=(message,), daemon=True).start()
    
    def _get_ai_response(self, message):
        """Get AI response (run in thread)."""
        try:
            response = self.bot.query_ai(message)
            self.append_chat(f"AI: {response}\n\n")
        except Exception as e:
            self.append_chat(f"AI: Error - {str(e)}\n\n")
    
    def quick_query(self, query):
        """Send a quick query."""
        self.chat_input.delete(0, tk.END)
        self.chat_input.insert(0, query)
        self.send_chat_message()
    
    def append_chat(self, text):
        """Append text to chat display."""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, text)
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
    
    def update_status(self, status):
        """Update status bar."""
        self.status_label.config(text=f"Status: {status}")
    
    def log_message(self, message):
        """Add message to logs."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_display.see(tk.END)
    
    def clear_logs(self):
        """Clear log display."""
        self.log_display.delete(1.0, tk.END)
    
    def update_dashboard(self, data):
        """Update dashboard with new data."""
        # Update account info
        if 'balance' in data:
            self.balance_label.config(text=f"${data['balance']:.2f}")
        
        if 'positions_count' in data:
            self.positions_label.config(text=str(data['positions_count']))
        
        if 'daily_pnl' in data:
            pnl = data['daily_pnl']
            color = 'green' if pnl >= 0 else 'red'
            self.pnl_label.config(text=f"${pnl:.2f}", foreground=color)
        
        # Update positions tree
        if 'positions' in data:
            self.positions_tree.delete(*self.positions_tree.get_children())
            for pos in data['positions']:
                self.positions_tree.insert('', 'end', values=pos)
        
        # Update trades tree
        if 'recent_trades' in data:
            self.trades_tree.delete(*self.trades_tree.get_children())
            for trade in data['recent_trades'][-10:]:  # Last 10 trades
                self.trades_tree.insert('', 'end', values=trade)
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
