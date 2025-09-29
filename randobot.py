#!/usr/bin/env python3
"""Randobot: random-entry Backtrader demo with Telegram alerts and CSV/state persistence."""
import os
import json
import time
import random
import threading
from datetime import datetime
import yfinance as yf
import backtrader as bt

STATE_FILE = 'randobot_state.json'
TRADES_FILE = 'randobot_trades.csv'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not (TELEGRAM_TOKEN and TELEGRAM_CHAT_ID):
    raise RuntimeError('Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in environment')


def send_telegram(msg: str):
    def _worker(text):
        try:
            import requests
            url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
            payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text}
            try:
                requests.post(url, json=payload, timeout=4)
            except Exception:
                pass
        except Exception:
            pass

    t = threading.Thread(target=_worker, args=(msg,), daemon=True)
    t.start()


def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {'last_trade': None, 'running_pnl': 0.0}


def save_state(s):
    with open(STATE_FILE, 'w') as f:
        json.dump(s, f)


class RandomStrat(bt.Strategy):
    def __init__(self):
        self.state = load_state()
        self.order = None
        self.entry_info = None
        self._sell_next = False

    def next(self):
        # 5% chance to enter long 10 shares at close
        if not self.position and random.random() < 0.05:
            size = 10
            price = self.data.close[0]
            self.order = self.buy(size=size)
            # record entry for messaging
            self.entry_info = {'date_in': str(self.data.datetime.date(0)), 'shares': size, 'entry': float(price)}
        # if a sell was scheduled after a buy, execute it now (market)
        elif self._sell_next and self.position:
            try:
                # sell entire position on this bar
                self.sell(exectype=bt.Order.Market, size=int(self.position.size))
            except Exception:
                try:
                    self.close()
                except Exception:
                    pass
            self._sell_next = False

    def notify_order(self, order):
        if order.status in [bt.Order.Completed]:
            if order.isbuy():
                # send entry Telegram
                try:
                    msg = f"RANDOM LONG {int(order.executed.size)} SPY @ {order.executed.price:.2f}"
                    send_telegram(msg)
                except Exception:
                    pass
                # schedule a market sell on the next bar
                try:
                    self._sell_next = True
                except Exception:
                    self._sell_next = False
            elif order.issell():
                try:
                    msg = f"RANDO TRADE CLOSED {order.executed.size} @ {order.executed.price:.2f}"
                    send_telegram(msg)
                except Exception:
                    pass

    def notify_trade(self, trade):
        if trade.isclosed:
            try:
                date_in = self.entry_info.get('date_in') if self.entry_info else ''
                date_out = str(self.data.datetime.date(0))
                # prefer trade.size if provided by backtrader; otherwise fallback to recorded entry shares
                try:
                    shares_val = getattr(trade, 'size', None)
                    if shares_val is None:
                        shares_val = (self.entry_info.get('shares') if self.entry_info else None)
                    shares = int(shares_val) if shares_val is not None else 0
                except Exception:
                    shares = 0
                entry = float(self.entry_info.get('entry')) if self.entry_info else 0.0
                exitp = float(trade.price) if hasattr(trade, 'price') else 0.0
                pnl = float(trade.pnl)
                # append to CSV
                write_header = not os.path.exists(TRADES_FILE)
                with open(TRADES_FILE, 'a', newline='') as f:
                    if write_header:
                        f.write('date_in,date_out,shares,entry,exit,pnl\n')
                    f.write(f"{date_in},{date_out},{shares},{entry},{exitp},{pnl}\n")
                # update state
                s = self.state
                s['last_trade'] = {'date_in': date_in, 'date_out': date_out, 'pnl': pnl}
                s['running_pnl'] = float(s.get('running_pnl', 0.0)) + pnl
                save_state(s)
                # send telegram summary
                try:
                    send_telegram(f"RANDO TRADE CLOSED {pnl:+.1f} $")
                except Exception:
                    pass
            except Exception:
                pass


def main():
    DAYS = 60
    df = yf.download('SPY', period=f'{DAYS}d', interval='1d', auto_adjust=True)
    df.dropna(inplace=True)
    # normalize column names like the main script did
    new_cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            new_cols.append(str(c[0]).lower())
        else:
            new_cols.append(str(c).lower())
    df.columns = new_cols
    if 'adj close' in df.columns and 'close' not in df.columns:
        df['close'] = df['adj close']
    for req in ('open','high','low','close','volume'):
        if req not in df.columns:
            raise RuntimeError(f'missing required column from data: {req}')
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    cerebro.adddata(data)
    cerebro.addstrategy(RandomStrat)
    cerebro.run()


if __name__ == '__main__':
    main()
