#!/usr/bin/env python3
"""
🔥 ARBI PHOENIX - Main Entry Point
The Ultimate Immortal Forex Trading System

"From the ashes of loss, rises the phoenix of profit"
"""

import sys
import asyncio
import logging
from pathlib import Path
import signal
import threading

# Try to import GUI components, fall back to console mode if failed
GUI_AVAILABLE = True
QApplication = None
QTimer = None
qasync = None

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer
    import qasync
    print("✅ PyQt6 available")
except ImportError:
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        import qasync
        print("✅ PyQt5 available")
    except ImportError:
        try:
            import tkinter as tk
            print("✅ tkinter available")
            GUI_AVAILABLE = True
        except ImportError:
            GUI_AVAILABLE = False
            print("⚠️ No GUI libraries available, running in console mode")

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_core.arbitrage_engine import ArbitrageEngine
from phoenix_core.recovery_system import RecoverySystem
from phoenix_core.profit_harvester import ProfitHarvester
from phoenix_brokers.pair_scanner import BrokerPairScanner
# Try to import GUI dashboard, fall back if not available
PhoenixDashboard = None
if GUI_AVAILABLE:
    if QApplication and qasync:
        # Try PyQt first
        try:
            from phoenix_gui.dashboard import PhoenixDashboard
            print("✅ Using PyQt dashboard")
        except ImportError:
            print("⚠️ PyQt GUI dashboard not available, trying tkinter...")
            try:
                from phoenix_gui.tkinter_dashboard import PhoenixTkinterDashboard as PhoenixDashboard
                print("✅ Using tkinter dashboard")
            except ImportError:
                print("⚠️ No GUI dashboard available")
                GUI_AVAILABLE = False
    else:
        # Try tkinter
        try:
            from phoenix_gui.tkinter_dashboard import PhoenixTkinterDashboard as PhoenixDashboard
            print("✅ Using tkinter dashboard")
        except ImportError:
            print("⚠️ tkinter GUI dashboard not available")
            GUI_AVAILABLE = False
from phoenix_utils.logger import setup_logger
from phoenix_utils.config_manager import ConfigManager

class ArbiPhoenix:
    """
    🔥 Main Arbi Phoenix System Controller
    
    The immortal trading system that rises from every setback
    """
    
    def __init__(self):
        """Initialize the Phoenix system"""
        self.logger = setup_logger("ArbiPhoenix")
        self.config = ConfigManager()
        
        # Core components
        self.pair_scanner = None
        self.arbitrage_engine = None
        self.recovery_system = None
        self.profit_harvester = None
        self.dashboard = None
        
        # System status
        self.is_running = False
        self.is_initialized = False
        
        self.logger.info("🔥 Arbi Phoenix initialized - The Phoenix awakens!")
    
    async def initialize(self):
        """Initialize all system components"""
        try:
            self.logger.info("🚀 Initializing Phoenix components...")
            
            # 1. Initialize broker pair scanner with auto-connection
            self.pair_scanner = BrokerPairScanner(self.config.broker_config)
            if self.config.is_auto_connect_enabled():
                self.logger.info("🔗 Auto-connection enabled - connecting to broker...")
                await self.pair_scanner.initialize()
            else:
                self.logger.info("🔗 Auto-connection disabled - manual connection required")
            
            # 2. Initialize arbitrage engine
            self.arbitrage_engine = ArbitrageEngine(
                pair_scanner=self.pair_scanner,
                config=self.config.trading_config
            )
            
            # 3. Initialize recovery system
            self.recovery_system = RecoverySystem(
                arbitrage_engine=self.arbitrage_engine,
                config=self.config.recovery_config
            )
            
            # 4. Initialize profit harvester
            self.profit_harvester = ProfitHarvester(
                arbitrage_engine=self.arbitrage_engine,
                config=self.config.profit_config
            )
            
            # 5. Initialize GUI dashboard (if available)
            if GUI_AVAILABLE and PhoenixDashboard:
                self.dashboard = PhoenixDashboard(
                    arbitrage_engine=self.arbitrage_engine,
                    recovery_system=self.recovery_system,
                    profit_harvester=self.profit_harvester
                )
                self.logger.info("📊 GUI Dashboard initialized")
            else:
                self.dashboard = None
                self.logger.info("📊 Running in console mode - no GUI dashboard")
            
            self.is_initialized = True
            self.logger.info("✅ Phoenix initialization complete - Ready to rise!")
            
            # Auto-start trading if enabled
            if self.config.is_auto_start_enabled():
                self.logger.info("🚀 Auto-start enabled - starting trading system...")
                await self.start_trading()
            
        except Exception as e:
            self.logger.error(f"❌ Phoenix initialization failed: {e}")
            raise
    
    async def start(self):
        """Start the Phoenix system (GUI or Console)"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            if GUI_AVAILABLE and self.dashboard:
                self.logger.info("🔥 Starting Arbi Phoenix GUI - The Phoenix awakens!")
                # Start GUI dashboard
                await self.dashboard.start()
                self.logger.info("✅ Phoenix GUI started successfully")
            else:
                self.logger.info("🔥 Starting Arbi Phoenix Console - The Phoenix awakens!")
                # Start console mode
                await self.start_console_mode()
                self.logger.info("✅ Phoenix Console started successfully")
            
            self.is_running = True
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Phoenix shutdown requested by user")
            await self.stop()
        except Exception as e:
            self.logger.error(f"💥 Phoenix encountered an error: {e}")
            await self.emergency_stop()
    
    async def start_trading(self):
        """Start the trading components"""
        try:
            if not self.pair_scanner.is_connected:
                self.logger.warning("⚠️ Broker not connected - attempting connection...")
                await self.pair_scanner.initialize()
            
            self.logger.info("🚀 Starting trading components...")
            
            # Start trading components
            trading_tasks = [
                self.arbitrage_engine.start(),
                self.recovery_system.start(),
                self.profit_harvester.start()
            ]
            
            # Start trading components in background
            for task in trading_tasks:
                asyncio.create_task(task)
            
            self.logger.info("✅ Trading system started")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start trading: {e}")
            raise
    
    async def stop_trading(self):
        """Stop the trading components"""
        try:
            self.logger.info("🛑 Stopping trading components...")
            
            # Stop trading components
            if self.profit_harvester:
                await self.profit_harvester.stop()
            
            if self.recovery_system:
                await self.recovery_system.stop()
            
            if self.arbitrage_engine:
                await self.arbitrage_engine.stop()
            
            self.logger.info("✅ Trading system stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to stop trading: {e}")
    
    async def stop(self):
        """Gracefully stop the Phoenix system"""
        self.logger.info("🔄 Phoenix shutdown initiated - Preparing for rebirth...")
        
        self.is_running = False
        
        # Stop trading components first
        await self.stop_trading()
        
        # Stop GUI dashboard
        if self.dashboard:
            await self.dashboard.stop()
        
        self.logger.info("✅ Phoenix shutdown complete - Ready for next resurrection!")
    
    async def emergency_stop(self):
        """Emergency stop with position protection"""
        self.logger.warning("🚨 EMERGENCY STOP - Protecting positions!")
        
        # Close all positions safely
        if self.arbitrage_engine:
            await self.arbitrage_engine.emergency_close_all()
        
        await self.stop()
    
    def get_status(self):
        """Get current system status"""
        return {
            'initialized': self.is_initialized,
            'running': self.is_running,
            'components': {
                'pair_scanner': self.pair_scanner is not None,
                'arbitrage_engine': self.arbitrage_engine is not None,
                'recovery_system': self.recovery_system is not None,
                'profit_harvester': self.profit_harvester is not None,
                'dashboard': self.dashboard is not None
            }
        }
    
    async def start_console_mode(self):
        """Start console mode interface"""
        print("\n🔥 ARBI PHOENIX - CONSOLE MODE")
        print("=" * 50)
        print("GUI not available, running in console mode")
        print("Use Ctrl+C to exit")
        
        # Start trading components automatically in console mode
        if self.config.is_auto_start_enabled():
            await self.start_trading()
        
        # Keep running until interrupted
        try:
            while self.is_running:
                await asyncio.sleep(10)  # Check every 10 seconds
                
                # Show basic status every minute
                if hasattr(self, '_last_status_time'):
                    if asyncio.get_event_loop().time() - self._last_status_time > 60:
                        await self._show_console_status()
                        self._last_status_time = asyncio.get_event_loop().time()
                else:
                    self._last_status_time = asyncio.get_event_loop().time()
                    
        except KeyboardInterrupt:
            print("\n🔥 Console mode interrupted by user")
            await self.stop()
    
    async def _show_console_status(self):
        """Show basic status in console"""
        if self.arbitrage_engine:
            status = self.arbitrage_engine.get_status()
            print(f"\n📊 Status: {status['status']} | "
                  f"Opportunities: {status['opportunities_found']} | "
                  f"Executed: {status['opportunities_executed']} | "
                  f"Profit: ${status['total_profit']:.2f}")
        else:
            print("📊 System initializing...")

def print_phoenix_banner():
    """Print the Phoenix startup banner"""
    banner = """
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    🔥                                                                  🔥
    🔥                          ARBI PHOENIX                           🔥
    🔥                                                                  🔥
    🔥              "From the ashes of loss, rises the                 🔥
    🔥                      phoenix of profit"                         🔥
    🔥                                                                  🔥
    🔥                The Ultimate Immortal Trading System             🔥
    🔥                                                                  🔥
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    
    ⚡ Features:
    • Triangular Arbitrage Engine
    • Multi-layer Recovery System  
    • Intelligent Profit Harvesting
    • Real-time GUI Dashboard
    • Multi-broker Support
    
    🛡️ "The Phoenix Never Dies" 🛡️
    """
    print(banner)

class PhoenixApp:
    """Phoenix GUI Application wrapper"""
    
    def __init__(self):
        self.app = None
        self.phoenix = None
        self.loop = None
    
    async def run(self):
        """Run the Phoenix application (GUI or Console)"""
        try:
            print_phoenix_banner()
            
            # Create Phoenix system
            self.phoenix = ArbiPhoenix()
            
            # Initialize Phoenix system
            await self.phoenix.initialize()
            
            if GUI_AVAILABLE and self.phoenix.dashboard:
                # Check if it's PyQt or tkinter dashboard
                if hasattr(self.phoenix.dashboard, 'control_panel'):
                    # PyQt GUI Mode
                    self.app = QApplication(sys.argv)
                    self.app.setApplicationName("Arbi Phoenix")
                    self.app.setApplicationVersion("1.0")
                    
                    # Connect GUI signals to Phoenix methods
                    self.phoenix.dashboard.control_panel.start_trading.connect(
                        lambda: asyncio.create_task(self.phoenix.start_trading())
                    )
                    self.phoenix.dashboard.control_panel.stop_trading.connect(
                        lambda: asyncio.create_task(self.phoenix.stop_trading())
                    )
                    
                    # Start Phoenix GUI
                    await self.phoenix.start()
                    
                    # Setup signal handlers
                    signal.signal(signal.SIGINT, self._signal_handler)
                    signal.signal(signal.SIGTERM, self._signal_handler)
                    
                    # Run Qt event loop with asyncio
                    await self._run_qt_loop()
                else:
                    # tkinter GUI Mode
                    print("🖥️ Starting tkinter GUI...")
                    
                    # Setup signal handlers
                    signal.signal(signal.SIGINT, self._signal_handler)
                    signal.signal(signal.SIGTERM, self._signal_handler)
                    
                    # Start Phoenix with tkinter
                    await self.phoenix.start()
                    
                    # Run tkinter main loop in thread
                    await self._run_tkinter_loop()
            else:
                # Console Mode
                # Setup signal handlers
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
                
                # Start Phoenix Console
                await self.phoenix.start()
            
        except KeyboardInterrupt:
            print("\n🔥 Phoenix rising again soon...")
        except Exception as e:
            print(f"💥 Phoenix encountered an error: {e}")
            logging.exception("Phoenix error details:")
        finally:
            if self.phoenix and self.phoenix.is_running:
                await self.phoenix.stop()
    
    async def _run_qt_loop(self):
        """Run Qt event loop asynchronously"""
        # Create a timer to process Qt events
        timer = QTimer()
        timer.timeout.connect(lambda: None)  # Keep event loop alive
        timer.start(10)  # 10ms interval
        
        # Process events until application quits
        while not self.app.property("quit_requested"):
            self.app.processEvents()
            await asyncio.sleep(0.01)  # Small delay to prevent CPU spinning
    
    async def _run_tkinter_loop(self):
        """Run tkinter GUI loop asynchronously"""
        try:
            if self.phoenix.dashboard:
                # Run tkinter in a separate thread
                def run_tkinter():
                    self.phoenix.dashboard.run()
                
                import threading
                gui_thread = threading.Thread(target=run_tkinter, daemon=True)
                gui_thread.start()
                
                # Keep main thread alive
                while gui_thread.is_alive():
                    await asyncio.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ tkinter loop error: {e}")

    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        print(f"\n🔥 Received signal {signum} - Shutting down Phoenix...")
        if hasattr(self, 'app') and self.app:
            self.app.setProperty("quit_requested", True)
        if self.phoenix:
            asyncio.create_task(self.phoenix.stop())

async def main():
    """Main entry point with GUI support"""
    # Create and run Phoenix application
    phoenix_app = PhoenixApp()
    await phoenix_app.run()

def main_sync():
    """Synchronous main entry point"""
    if GUI_AVAILABLE:
        if qasync and QApplication:
            try:
                # PyQt mode with qasync
                app = QApplication(sys.argv)
                loop = qasync.QEventLoop(app)
                asyncio.set_event_loop(loop)
                
                with loop:
                    loop.run_until_complete(main())
                    
            except Exception as e:
                print(f"⚠️ PyQt GUI mode failed: {e}")
                print("🔄 Falling back to console mode...")
                asyncio.run(main())
        else:
            try:
                # tkinter mode - basic asyncio
                print("🖥️ Running tkinter GUI mode")
                asyncio.run(main())
                
            except Exception as e:
                print(f"⚠️ tkinter GUI mode failed: {e}")
                print("🔄 Falling back to console mode...")
                asyncio.run(main())
    else:
        # Console mode - basic asyncio
        print("📟 Running in console mode")
        asyncio.run(main())

if __name__ == "__main__":
    # Run the Phoenix
    main_sync()
