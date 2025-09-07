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
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import qasync

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_core.arbitrage_engine import ArbitrageEngine
from phoenix_core.recovery_system import RecoverySystem
from phoenix_core.profit_harvester import ProfitHarvester
from phoenix_brokers.pair_scanner import BrokerPairScanner
from phoenix_gui.dashboard import PhoenixDashboard
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
            
            # 5. Initialize GUI dashboard
            self.dashboard = PhoenixDashboard(
                arbitrage_engine=self.arbitrage_engine,
                recovery_system=self.recovery_system,
                profit_harvester=self.profit_harvester
            )
            
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
        """Start the Phoenix GUI system"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            self.logger.info("🔥 Starting Arbi Phoenix GUI - The Phoenix awakens!")
            
            # Start GUI dashboard
            await self.dashboard.start()
            
            self.is_running = True
            self.logger.info("✅ Phoenix GUI started successfully")
            
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
        """Run the Phoenix application with GUI"""
        try:
            print_phoenix_banner()
            
            # Create QApplication
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("Arbi Phoenix")
            self.app.setApplicationVersion("1.0")
            
            # Create Phoenix system
            self.phoenix = ArbiPhoenix()
            
            # Initialize Phoenix system
            await self.phoenix.initialize()
            
            # Connect GUI signals to Phoenix methods
            if self.phoenix.dashboard:
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
    
    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        print(f"\n🔥 Received signal {signum} - Shutting down Phoenix...")
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
    try:
        # Use qasync for better Qt/asyncio integration
        import qasync
        
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        with loop:
            loop.run_until_complete(main())
            
    except ImportError:
        # Fallback to basic asyncio if qasync not available
        print("⚠️ qasync not available - using basic asyncio")
        asyncio.run(main())

if __name__ == "__main__":
    # Run the Phoenix
    main_sync()
