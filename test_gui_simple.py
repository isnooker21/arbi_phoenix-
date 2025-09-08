#!/usr/bin/env python3
"""
🔥 Simple GUI Test
Test tkinter GUI without complex dependencies
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

class SimplePhoenixGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 Arbi Phoenix Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # Status variables
        self.connection_status = tk.StringVar(value="Disconnected")
        self.trading_status = tk.StringVar(value="Stopped")
        
        self.create_gui()
    
    def create_gui(self):
        """Create the GUI"""
        # Header
        header = tk.Frame(self.root, bg='#2b2b2b', height=80)
        header.pack(fill='x', padx=10, pady=5)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🔥 ARBI PHOENIX DASHBOARD", 
                        bg='#2b2b2b', fg='#ff6b35',
                        font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text="The Ultimate Immortal Forex Trading System",
                           bg='#2b2b2b', fg='#ffffff',
                           font=('Arial', 10))
        subtitle.pack()
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg='#2b2b2b', height=100)
        control_frame.pack(fill='x', padx=10, pady=5)
        control_frame.pack_propagate(False)
        
        # Connection row
        conn_frame = tk.Frame(control_frame, bg='#2b2b2b')
        conn_frame.pack(fill='x', pady=(5, 0))
        
        self.connect_btn = tk.Button(conn_frame, text="🔗 Connect Broker",
                                    command=self.connect_broker,
                                    bg='#0066cc', fg='white',
                                    font=('Arial', 10, 'bold'), width=18)
        self.connect_btn.pack(side='left', padx=5)
        
        self.disconnect_btn = tk.Button(conn_frame, text="❌ Disconnect",
                                       command=self.disconnect_broker,
                                       bg='#666666', fg='white',
                                       font=('Arial', 10, 'bold'), width=15)
        self.disconnect_btn.pack(side='left', padx=5)
        
        status_label = tk.Label(conn_frame, textvariable=self.connection_status,
                               bg='#2b2b2b', fg='#ffff00',
                               font=('Arial', 10, 'bold'))
        status_label.pack(side='left', padx=20)
        
        # Trading row
        trade_frame = tk.Frame(control_frame, bg='#2b2b2b')
        trade_frame.pack(fill='x', pady=(5, 5))
        
        self.start_btn = tk.Button(trade_frame, text="🚀 Start Trading",
                                  command=self.start_trading,
                                  bg='#00aa00', fg='white',
                                  font=('Arial', 11, 'bold'), width=15)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(trade_frame, text="🛑 Stop Trading",
                                 command=self.stop_trading,
                                 bg='#aa0000', fg='white',
                                 font=('Arial', 11, 'bold'), width=15)
        self.stop_btn.pack(side='left', padx=5)
        
        trading_label = tk.Label(trade_frame, textvariable=self.trading_status,
                                bg='#2b2b2b', fg='#00ff00',
                                font=('Arial', 11, 'bold'))
        trading_label.pack(side='left', padx=20)
        
        # Status Panel
        status_frame = tk.LabelFrame(self.root, text="📊 System Status",
                                    bg='#2b2b2b', fg='#ffffff',
                                    font=('Arial', 12, 'bold'))
        status_frame.pack(fill='x', padx=10, pady=5)
        
        # Status items
        status_items = [
            "Account Balance: $10,000.00",
            "Total Profit: $0.00", 
            "Opportunities Found: 0",
            "Opportunities Executed: 0",
            "Success Rate: 0.0%",
            "Active Positions: 0"
        ]
        
        for i, item in enumerate(status_items):
            row = i // 3
            col = i % 3
            label = tk.Label(status_frame, text=item,
                           bg='#2b2b2b', fg='#00ff00',
                           font=('Arial', 10))
            label.grid(row=row, column=col, sticky='w', padx=10, pady=5)
        
        # Log Panel
        log_frame = tk.LabelFrame(self.root, text="📝 Activity Log",
                                 bg='#2b2b2b', fg='#ffffff',
                                 font=('Arial', 12, 'bold'))
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15,
                                                 bg='#1e1e1e', fg='#ffffff',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initial log
        self.log_message("🔥 Arbi Phoenix Dashboard initialized")
        self.log_message("✅ GUI components loaded successfully")
        self.log_message("📊 Ready for broker connection")
    
    def log_message(self, message):
        """Add message to log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
    
    def connect_broker(self):
        """Connect to broker"""
        self.log_message("🔗 Connecting to broker...")
        self.connection_status.set("Connecting...")
        self.connect_btn.config(state='disabled')
        
        def connect():
            time.sleep(2)  # Simulate connection
            self.log_message("✅ Broker connected successfully")
            self.connection_status.set("Connected")
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='normal')
        
        threading.Thread(target=connect, daemon=True).start()
    
    def disconnect_broker(self):
        """Disconnect from broker"""
        self.log_message("❌ Disconnecting from broker...")
        self.connection_status.set("Disconnecting...")
        self.disconnect_btn.config(state='disabled')
        
        def disconnect():
            time.sleep(1)  # Simulate disconnection
            self.log_message("✅ Broker disconnected")
            self.connection_status.set("Disconnected")
            self.connect_btn.config(state='normal')
            self.disconnect_btn.config(state='normal')
            
            # Stop trading if running
            if self.trading_status.get() == "Running":
                self.log_message("🛑 Stopping trading due to disconnection...")
                self.trading_status.set("Stopped")
        
        threading.Thread(target=disconnect, daemon=True).start()
    
    def start_trading(self):
        """Start trading"""
        if self.connection_status.get() != "Connected":
            self.log_message("❌ Please connect to broker first!")
            messagebox.showwarning("Connection Required", 
                                 "Please connect to broker before starting trading!")
            return
        
        self.log_message("🚀 Starting trading system...")
        self.trading_status.set("Starting...")
        self.start_btn.config(state='disabled')
        
        def start():
            time.sleep(1)  # Simulate startup
            self.log_message("✅ Trading system started")
            self.log_message("🔍 Scanning for arbitrage opportunities...")
            self.trading_status.set("Running")
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='normal')
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_trading(self):
        """Stop trading"""
        self.log_message("🛑 Stopping trading system...")
        self.trading_status.set("Stopping...")
        self.stop_btn.config(state='disabled')
        
        def stop():
            time.sleep(1)  # Simulate shutdown
            self.log_message("✅ Trading system stopped")
            self.trading_status.set("Stopped")
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='normal')
        
        threading.Thread(target=stop, daemon=True).start()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    print("🔥 Testing Simple Phoenix GUI...")
    print("=" * 50)
    
    try:
        gui = SimplePhoenixGUI()
        print("✅ GUI created successfully!")
        print("🖥️ Opening GUI window...")
        gui.run()
        print("✅ GUI test completed")
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
