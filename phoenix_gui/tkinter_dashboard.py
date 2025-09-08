#!/usr/bin/env python3
"""
🔥 ARBI PHOENIX - Tkinter Dashboard
GUI Dashboard using tkinter (built-in Python GUI)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import asyncio
import time
from datetime import datetime
from typing import Optional, Dict, Any

class PhoenixTkinterDashboard:
    """
    🔥 Phoenix Dashboard using tkinter
    
    Cross-platform GUI that works without external dependencies
    """
    
    def __init__(self, arbitrage_engine=None, recovery_system=None, profit_harvester=None):
        """Initialize tkinter dashboard"""
        self.arbitrage_engine = arbitrage_engine
        self.recovery_system = recovery_system
        self.profit_harvester = profit_harvester
        
        # GUI components
        self.root = None
        self.is_running = False
        self.update_thread = None
        
        # Status variables (will be initialized in create_gui)
        self.connection_status = None
        self.trading_status = None
        self.account_balance = None
        self.total_profit = None
        self.opportunities_found = None
        self.opportunities_executed = None
        self.success_rate = None
        self.active_positions = None
        
    def create_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("🔥 Arbi Phoenix Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize status variables after root window is created
        self.connection_status = tk.StringVar(value="Disconnected")
        self.trading_status = tk.StringVar(value="Stopped")
        self.account_balance = tk.StringVar(value="$0.00")
        self.total_profit = tk.StringVar(value="$0.00")
        self.opportunities_found = tk.StringVar(value="0")
        self.opportunities_executed = tk.StringVar(value="0")
        self.success_rate = tk.StringVar(value="0.0%")
        self.active_positions = tk.StringVar(value="0")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ff6b35',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Status.TLabel',
                       background='#2b2b2b',
                       foreground='#ffffff',
                       font=('Arial', 10))
        
        style.configure('Value.TLabel',
                       background='#2b2b2b', 
                       foreground='#00ff00',
                       font=('Arial', 12, 'bold'))
        
        # Create main layout
        self._create_header()
        self._create_control_panel()
        self._create_status_panel()
        self._create_opportunities_panel()
        self._create_positions_panel()
        self._create_log_panel()
        
        return self.root
    
    def _create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.root, bg='#2b2b2b', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🔥 ARBI PHOENIX DASHBOARD",
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="The Ultimate Immortal Forex Trading System",
                                  style='Status.TLabel')
        subtitle_label.pack()
    
    def _create_control_panel(self):
        """Create control buttons panel"""
        control_frame = tk.Frame(self.root, bg='#2b2b2b', height=80)
        control_frame.pack(fill='x', padx=10, pady=5)
        control_frame.pack_propagate(False)
        
        # Connection status
        self.connection_status = tk.StringVar(value="Disconnected")
        
        # Top row - Connection controls
        conn_frame = tk.Frame(control_frame, bg='#2b2b2b')
        conn_frame.pack(fill='x', pady=(5, 0))
        
        self.connect_button = tk.Button(conn_frame,
                                       text="🔗 Connect Broker",
                                       command=self._connect_broker,
                                       bg='#0066cc',
                                       fg='white',
                                       font=('Arial', 10, 'bold'),
                                       width=18)
        self.connect_button.pack(side='left', padx=5)
        
        self.disconnect_button = tk.Button(conn_frame,
                                          text="❌ Disconnect",
                                          command=self._disconnect_broker,
                                          bg='#666666',
                                          fg='white',
                                          font=('Arial', 10, 'bold'),
                                          width=15)
        self.disconnect_button.pack(side='left', padx=5)
        
        # Connection status label
        status_label = tk.Label(conn_frame,
                               textvariable=self.connection_status,
                               bg='#2b2b2b',
                               fg='#ffff00',
                               font=('Arial', 10, 'bold'))
        status_label.pack(side='left', padx=20)
        
        # Bottom row - Trading controls
        trade_frame = tk.Frame(control_frame, bg='#2b2b2b')
        trade_frame.pack(fill='x', pady=(5, 5))
        
        self.start_button = tk.Button(trade_frame,
                                     text="🚀 Start Trading",
                                     command=self._start_trading,
                                     bg='#00aa00',
                                     fg='white',
                                     font=('Arial', 11, 'bold'),
                                     width=15)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(trade_frame,
                                    text="🛑 Stop Trading", 
                                    command=self._stop_trading,
                                    bg='#aa0000',
                                    fg='white',
                                    font=('Arial', 11, 'bold'),
                                    width=15)
        self.stop_button.pack(side='left', padx=5)
        
        self.refresh_button = tk.Button(trade_frame,
                                       text="🔄 Refresh",
                                       command=self._refresh_data,
                                       bg='#0066cc',
                                       fg='white', 
                                       font=('Arial', 11, 'bold'),
                                       width=15)
        self.refresh_button.pack(side='left', padx=5)
    
    def _create_status_panel(self):
        """Create status information panel"""
        status_frame = tk.LabelFrame(self.root, 
                                    text="📊 System Status",
                                    bg='#2b2b2b',
                                    fg='#ffffff',
                                    font=('Arial', 12, 'bold'))
        status_frame.pack(fill='x', padx=10, pady=5)
        
        # Create grid for status items
        status_items = [
            ("Trading Status:", self.trading_status),
            ("Account Balance:", self.account_balance),
            ("Total Profit:", self.total_profit),
            ("Opportunities Found:", self.opportunities_found),
            ("Opportunities Executed:", self.opportunities_executed),
            ("Success Rate:", self.success_rate),
            ("Active Positions:", self.active_positions)
        ]
        
        for i, (label_text, var) in enumerate(status_items):
            row = i // 3
            col = (i % 3) * 2
            
            label = ttk.Label(status_frame, text=label_text, style='Status.TLabel')
            label.grid(row=row, column=col, sticky='w', padx=10, pady=5)
            
            value = ttk.Label(status_frame, textvariable=var, style='Value.TLabel')
            value.grid(row=row, column=col+1, sticky='w', padx=10, pady=5)
    
    def _create_opportunities_panel(self):
        """Create opportunities display panel"""
        opp_frame = tk.LabelFrame(self.root,
                                 text="🎯 Current Opportunities",
                                 bg='#2b2b2b',
                                 fg='#ffffff',
                                 font=('Arial', 12, 'bold'))
        opp_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for opportunities
        columns = ('Triangle', 'Profit (pips)', 'Spread Cost', 'Net Profit', 'Confidence')
        self.opp_tree = ttk.Treeview(opp_frame, columns=columns, show='headings', height=6)
        
        # Configure columns
        for col in columns:
            self.opp_tree.heading(col, text=col)
            self.opp_tree.column(col, width=150, anchor='center')
        
        # Add scrollbar
        opp_scrollbar = ttk.Scrollbar(opp_frame, orient='vertical', command=self.opp_tree.yview)
        self.opp_tree.configure(yscrollcommand=opp_scrollbar.set)
        
        self.opp_tree.pack(side='left', fill='both', expand=True)
        opp_scrollbar.pack(side='right', fill='y')
    
    def _create_positions_panel(self):
        """Create positions display panel"""
        pos_frame = tk.LabelFrame(self.root,
                                 text="📈 Active Positions", 
                                 bg='#2b2b2b',
                                 fg='#ffffff',
                                 font=('Arial', 12, 'bold'))
        pos_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create treeview for positions
        columns = ('Symbol', 'Type', 'Volume', 'Open Price', 'Current Price', 'Profit')
        self.pos_tree = ttk.Treeview(pos_frame, columns=columns, show='headings', height=6)
        
        # Configure columns
        for col in columns:
            self.pos_tree.heading(col, text=col)
            self.pos_tree.column(col, width=120, anchor='center')
        
        # Add scrollbar
        pos_scrollbar = ttk.Scrollbar(pos_frame, orient='vertical', command=self.pos_tree.yview)
        self.pos_tree.configure(yscrollcommand=pos_scrollbar.set)
        
        self.pos_tree.pack(side='left', fill='both', expand=True)
        pos_scrollbar.pack(side='right', fill='y')
    
    def _create_log_panel(self):
        """Create log display panel"""
        log_frame = tk.LabelFrame(self.root,
                                 text="📝 Activity Log",
                                 bg='#2b2b2b', 
                                 fg='#ffffff',
                                 font=('Arial', 12, 'bold'))
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create scrolled text widget for logs
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 height=8,
                                                 bg='#1e1e1e',
                                                 fg='#ffffff',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add initial log message
        self.log_message("🔥 Arbi Phoenix Dashboard initialized")
    
    def _connect_broker(self):
        """Connect to broker"""
        try:
            self.log_message("🔗 Connecting to broker...")
            self.connection_status.set("Connecting...")
            self.connect_button.config(state='disabled')
            
            # Create async task for broker connection
            threading.Thread(target=self._async_connect_broker, daemon=True).start()
                
        except Exception as e:
            self.log_message(f"❌ Error connecting to broker: {e}")
            self.connect_button.config(state='normal')
    
    def _disconnect_broker(self):
        """Disconnect from broker"""
        try:
            self.log_message("❌ Disconnecting from broker...")
            self.connection_status.set("Disconnecting...")
            self.disconnect_button.config(state='disabled')
            
            # Create async task for broker disconnection
            threading.Thread(target=self._async_disconnect_broker, daemon=True).start()
                
        except Exception as e:
            self.log_message(f"❌ Error disconnecting from broker: {e}")
            self.disconnect_button.config(state='normal')

    def _start_trading(self):
        """Start trading system"""
        try:
            # Check if broker is connected first
            if self.connection_status.get() != "Connected":
                self.log_message("❌ Please connect to broker first!")
                messagebox.showwarning("Connection Required", "Please connect to broker before starting trading!")
                return
            
            self.log_message("🚀 Starting trading system...")
            
            # Create async task for starting trading
            if self.arbitrage_engine:
                threading.Thread(target=self._async_start_trading, daemon=True).start()
                self.trading_status.set("Starting...")
                self.start_button.config(state='disabled')
            else:
                self.log_message("❌ Trading engine not available")
                
        except Exception as e:
            self.log_message(f"❌ Error starting trading: {e}")
    
    def _stop_trading(self):
        """Stop trading system"""
        try:
            self.log_message("🛑 Stopping trading system...")
            
            # Create async task for stopping trading
            if self.arbitrage_engine:
                threading.Thread(target=self._async_stop_trading, daemon=True).start()
                self.trading_status.set("Stopping...")
                self.stop_button.config(state='disabled')
            else:
                self.log_message("❌ Trading engine not available")
                
        except Exception as e:
            self.log_message(f"❌ Error stopping trading: {e}")
    
    def _refresh_data(self):
        """Refresh all data displays"""
        self.log_message("🔄 Refreshing data...")
        self._update_status()
        self._update_opportunities()
        self._update_positions()
    
    def _async_connect_broker(self):
        """Async wrapper for connecting to broker"""
        try:
            import time
            time.sleep(2)  # Simulate connection time
            
            # Check if pair_scanner exists and try to connect
            if hasattr(self, 'pair_scanner') and self.pair_scanner:
                # Try to initialize broker connection
                self.log_message("📡 Initializing broker connection...")
                # In real implementation, this would call: await self.pair_scanner.initialize()
                
            self.log_message("✅ Broker connected successfully")
            self.connection_status.set("Connected")
            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='normal')
            
        except Exception as e:
            self.log_message(f"❌ Failed to connect to broker: {e}")
            self.connection_status.set("Disconnected")
            self.connect_button.config(state='normal')
    
    def _async_disconnect_broker(self):
        """Async wrapper for disconnecting from broker"""
        try:
            import time
            time.sleep(1)  # Simulate disconnection time
            
            self.log_message("✅ Broker disconnected")
            self.connection_status.set("Disconnected")
            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='normal')
            
            # Also stop trading if running
            if self.trading_status.get() == "Running":
                self.log_message("🛑 Stopping trading due to disconnection...")
                self.trading_status.set("Stopped")
            
        except Exception as e:
            self.log_message(f"❌ Failed to disconnect from broker: {e}")
            self.disconnect_button.config(state='normal')

    def _async_start_trading(self):
        """Async wrapper for starting trading"""
        try:
            import time
            time.sleep(1)  # Simulate startup time
            
            # This would need to be implemented based on your async architecture
            self.log_message("✅ Trading system started")
            self.trading_status.set("Running")
            self.start_button.config(state='normal')
            self.stop_button.config(state='normal')
        except Exception as e:
            self.log_message(f"❌ Failed to start trading: {e}")
            self.trading_status.set("Stopped")
            self.start_button.config(state='normal')
    
    def _async_stop_trading(self):
        """Async wrapper for stopping trading"""
        try:
            import time
            time.sleep(1)  # Simulate shutdown time
            
            # This would need to be implemented based on your async architecture
            self.log_message("✅ Trading system stopped")
            self.trading_status.set("Stopped")
            self.start_button.config(state='normal')
            self.stop_button.config(state='normal')
        except Exception as e:
            self.log_message(f"❌ Failed to stop trading: {e}")
            self.stop_button.config(state='normal')
    
    def _update_status(self):
        """Update status information"""
        try:
            if self.arbitrage_engine:
                status = self.arbitrage_engine.get_status()
                
                self.trading_status.set(status.get('status', 'Unknown'))
                self.opportunities_found.set(str(status.get('opportunities_found', 0)))
                self.opportunities_executed.set(str(status.get('opportunities_executed', 0)))
                self.success_rate.set(f"{status.get('success_rate', 0):.1f}%")
                self.active_positions.set(str(status.get('active_positions', 0)))
                self.total_profit.set(f"${status.get('total_profit', 0):.2f}")
                
        except Exception as e:
            self.log_message(f"❌ Error updating status: {e}")
    
    def _update_opportunities(self):
        """Update opportunities display"""
        try:
            # Clear existing items
            for item in self.opp_tree.get_children():
                self.opp_tree.delete(item)
            
            if self.arbitrage_engine:
                opportunities = self.arbitrage_engine.get_opportunities()
                
                for opp in opportunities[:10]:  # Show top 10
                    triangle = f"{opp.pair1}-{opp.pair2}-{opp.pair3}"
                    values = (
                        triangle,
                        f"{opp.profit_pips:.1f}",
                        f"{opp.spread_cost:.1f}",
                        f"{opp.net_profit:.1f}",
                        f"{opp.confidence:.1%}"
                    )
                    self.opp_tree.insert('', 'end', values=values)
                    
        except Exception as e:
            self.log_message(f"❌ Error updating opportunities: {e}")
    
    def _update_positions(self):
        """Update positions display"""
        try:
            # Clear existing items
            for item in self.pos_tree.get_children():
                self.pos_tree.delete(item)
            
            if self.arbitrage_engine:
                positions = self.arbitrage_engine.get_positions()
                
                for pos in positions:
                    values = (
                        pos.symbol,
                        pos.type,
                        f"{pos.volume:.2f}",
                        f"{pos.open_price:.5f}",
                        f"{pos.current_price:.5f}",
                        f"${pos.profit:.2f}"
                    )
                    self.pos_tree.insert('', 'end', values=values)
                    
        except Exception as e:
            self.log_message(f"❌ Error updating positions: {e}")
    
    def log_message(self, message: str):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
        
        # Limit log size
        lines = self.log_text.get('1.0', 'end').split('\n')
        if len(lines) > 100:
            self.log_text.delete('1.0', '10.0')
    
    def start_update_loop(self):
        """Start the data update loop"""
        def update_loop():
            while self.is_running:
                try:
                    self.root.after(0, self._update_status)
                    self.root.after(0, self._update_opportunities) 
                    self.root.after(0, self._update_positions)
                    time.sleep(2)  # Update every 2 seconds
                except:
                    break
        
        self.is_running = True
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    async def start(self):
        """Start the dashboard"""
        self.create_gui()
        self.start_update_loop()
        self.log_message("🔥 Dashboard started successfully")
    
    async def stop(self):
        """Stop the dashboard"""
        self.is_running = False
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Run the GUI main loop"""
        if not self.root:
            self.create_gui()
            self.start_update_loop()
            self.log_message("🔥 Dashboard started successfully")
        
        if self.root:
            self.root.mainloop()


# Test the dashboard
if __name__ == "__main__":
    print("🔥 Testing Tkinter Dashboard...")
    
    dashboard = PhoenixTkinterDashboard()
    root = dashboard.create_gui()
    dashboard.start_update_loop()
    dashboard.log_message("🔥 Test dashboard running")
    
    root.mainloop()
