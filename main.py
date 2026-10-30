import time
import math
import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

SYMBOLS = ['BNBUSDT', 'ETHUSDT', 'BTCUSDT']
# Android ෆෝන් එක ඇතුළේ App එක ක්‍රැෂ් නොවී සේව් වෙන්න:
if os.environ.get('ANDROID_ARGUMENT'):
    from android.storage import app_storage_path
    LOG_FILE = os.path.join(app_storage_path(), "crypto_signals_log.txt")
else:
    LOG_FILE = "crypto_signals_log.txt"
update_interval = 2.0  
clock_event = None     
simulated_history = {}
last_signals = {}

def initialize_market_history():
    global simulated_history, last_signals
    simulated_history = {}
    last_signals = {symbol: "INITIAL" for symbol in SYMBOLS}
    for s in SYMBOLS:
        base_p = 600.0 if 'BNB' in s else (2500.0 if 'ETH' in s else 95000.0)
        simulated_history[s] = [base_p + random.uniform(-10, 10) for _ in range(50)]

initialize_market_history()

def get_live_market_data(symbol):
    if symbol not in simulated_history:
        base_p = 600.0 if 'BNB' in symbol else (2500.0 if 'ETH' in symbol else 95000.0)
        simulated_history[symbol] = [base_p + random.uniform(-10, 10) for _ in range(50)]
    history = simulated_history[symbol]
    last_price = history[-1]
    change_pct = random.uniform(-0.0015, 0.0015) 
    new_price = last_price * (1 + change_pct)
    history.append(new_price)
    if len(history) > 100:
        history.pop(0)
    simulated_history[symbol] = history
    return new_price, history

def calculate_ema(prices, period):
    if len(prices) < period: return None
    k = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price * k) + (ema * (1 - k))
    return ema

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1: return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(change if change > 0 else 0)
        losses.append(abs(change) if change < 0 else 0)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0: return 100
    return 100 - (100 / (1 + (avg_gain / avg_loss)))

def log_signal_to_file(timestamp, symbol, price, rsi, signal, tp, sl):
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 2 * 1024 * 1024:
        try: os.remove(LOG_FILE)
        except: pass
    log_entry = f"[{timestamp}] ASSET: {symbol} | PRICE: {price:.2f} | RSI: {rsi:.2f} | SIGNAL: {signal} | TP: {tp:.2f} | SL: {sl:.2f}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file: file.write(log_entry)
    except: pass

class ConfigurableCryptoBot(App):
    def build(self):
        global clock_event
        self.main_layout = BoxLayout(orientation='vertical', padding=12, spacing=8)
        self.header_label = Label(text="PRO CUSTOMIZABLE CRYPTO BOT", font_size='18sp', bold=True, size_hint_y=None, height=35, color=get_color_from_hex('#FFD700'))
        self.main_layout.add_widget(self.header_label)
        self.config_box = BoxLayout(orientation='vertical', size_hint_y=None, height=110, spacing=5)
        self.symbol_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        self.symbol_input_layout.add_widget(Label(text="Symbols:", size_hint_x=0.3, font_size='13sp'))
        self.symbol_txt = TextInput(text="BNBUSDT,ETHUSDT,BTCUSDT", multiline=False, font_size='13sp')
        self.symbol_input_layout.add_widget(self.symbol_txt)
        self.config_box.add_widget(self.symbol_input_layout)
        self.time_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        self.time_input_layout.add_widget(Label(text="Interval (s):", size_hint_x=0.3, font_size='13sp'))
        self.time_txt = TextInput(text="2.0", multiline=False, font_size='13sp')
        self.time_input_layout.add_widget(self.time_txt)
        self.config_box.add_widget(self.time_input_layout)
        self.save_btn = Button(text="Apply & Restart Settings", size_hint_y=None, height=35, background_color=get_color_from_hex('#1E88E5'), bold=True)
        self.save_btn.bind(on_press=self.apply_user_settings)
        self.config_box.add_widget(self.save_btn)
        self.main_layout.add_widget(self.config_box)
        self.monitor_label = Label(text="Connecting to data stream...", font_size='13sp', halign='left', valign='top', size_hint_y=None)
        self.monitor_label.bind(texture_size=self.monitor_label.setter('size'))
        self.monitor_scroll = ScrollView(size_hint=(1, 0.35))
        self.monitor_scroll.add_widget(self.monitor_label)
        self.main_layout.add_widget(self.monitor_scroll)
        self.log_header = Label(text="Live Trigger Logs:", font_size='13sp', bold=True, size_hint_y=None, height=20, halign='left', color=get_color_from_hex('#A9A9A9'))
        self.log_header.bind(size=self.log_header.setter('text_size'))
        self.main_layout.add_widget(self.log_header)
        self.logs_label = Label(text="No signals triggered yet.\n", font_size='12sp', halign='left', valign='top', size_hint_y=None)
        self.logs_label.bind(texture_size=self.logs_label.setter('size'))
        self.logs_scroll = ScrollView(size_hint=(1, 0.35))
        self.logs_scroll.add_widget(self.logs_label)
        self.main_layout.add_widget(self.logs_scroll)
        clock_event = Clock.schedule_interval(self.process_bot_cycle_gui, update_interval)
        return self.main_layout

    def apply_user_settings(self, instance):
        global SYMBOLS, update_interval, clock_event
        raw_symbols = self.symbol_txt.text.strip()
        if raw_symbols:
            SYMBOLS = [s.strip().upper() for s in raw_symbols.split(',') if s.strip()]
            initialize_market_history()
        try:
            new_time = float(self.time_txt.text.strip())
            if new_time > 0.1:
                update_interval = new_time
        except ValueError:
            pass
        if clock_event:
            Clock.unschedule(clock_event)
        clock_event = Clock.schedule_interval(self.process_bot_cycle_gui, update_interval)
        self.monitor_label.text = "Settings updated! Fetching data..."

    def process_bot_cycle_gui(self, dt):
        global last_signals
        timestamp = time.strftime('%H:%M:%S', time.localtime())
        display_text = f"TIME: {timestamp} | REFRESH: {update_interval}s\n"
        display_text += "------------------------------------------------------------\n"
        display_text += f" {'ASSET':<12}{'PRICE':<16}{'RSI(14)':<14}{'STATUS'}\n"
        display_text += "------------------------------------------------------------\n"
        for symbol in SYMBOLS:
            current_price, close_prices = get_live_market_data(symbol)
            ema9 = calculate_ema(close_prices, 9)
            ema21 = calculate_ema(close_prices, 21)
            rsi14 = calculate_rsi(close_prices, 14)
            if None in [ema9, ema21, rsi14]: continue
            current_condition = "NEUTRAL"
            if ema9 > ema21 and rsi14 < 65: current_condition = "BULLISH"
            elif ema9 < ema21 and rsi14 > 35: current_condition = "BEARISH"
            cond_emoji = "[N]" if current_condition == "NEUTRAL" else ("[BUY]" if current_condition == "BULLISH" else "[SELL]")
            display_name = symbol.replace("USDT", "")
            display_text += f" * {display_name:<10}${current_price:<14.2f}{rsi14:<14.1f}{cond_emoji} {current_condition}\n"
            
            if symbol not in last_signals or last_signals[symbol] == "INITIAL":
                last_signals[symbol] = current_condition
                continue
                
            if current_condition != "NEUTRAL" and current_condition != last_signals[symbol]:
                last_signals[symbol] = current_condition
                full_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                risk_amt = current_price * 0.005
                
                if current_condition == "BULLISH":
                    signal_type = "BUY"
                    tp = current_price + (risk_amt * 2)
                    sl = current_price - risk_amt
                else:
                    signal_type = "SELL"
                    tp = current_price - (risk_amt * 2)
                    sl = current_price + risk_amt
                    
                log_signal_to_file(full_timestamp, symbol, current_price, rsi14, signal_type, tp, sl)
                new_log = f"[{timestamp}] {symbol} -> {signal_type} @ {current_price:.2f} (TP: {tp:.2f}, SL: {sl:.2f})\n"
                if "No signals triggered yet" in self.logs_label.text:
                    self.logs_label.text = new_log
                else:
                    self.logs_label.text = new_log + self.logs_label.text
                    
        self.monitor_label.text = display_text

if __name__ == '__main__':
    ConfigurableCryptoBot().run()
