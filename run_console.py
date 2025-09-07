#!/usr/bin/env python3
"""
🔥 ARBI PHOENIX - Console Mode
Console-only version for testing without GUI dependencies

"The Phoenix that runs everywhere"
"""

import sys
import asyncio
import logging
from pathlib import Path
import signal

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_core.arbitrage_engine import ArbitrageEngine
from phoenix_core.recovery_system import RecoverySystem
from phoenix_core.profit_harvester import ProfitHarvester
from phoenix_brokers.pair_scanner import BrokerPairScanner
from phoenix_utils.logger import setup_logger
from phoenix_utils.config_manager import ConfigManager

class ArbiPhoenixConsole:
    """
    🔥 Console-only Arbi Phoenix System
    
    Runs without GUI for testing and server deployment
    """
    
    def __init__(self):
        """Initialize the Phoenix console system"""
        self.logger = setup_logger("ArbiPhoenixConsole")
        self.config = ConfigManager()
        
        # Core components
        self.pair_scanner = None
        self.arbitrage_engine = None
        self.recovery_system = None
        self.profit_harvester = None
        
        # System status
        self.is_running = False
        self.is_initialized = False
        
        self.logger.info("🔥 Arbi Phoenix Console initialized")
    
    async def initialize(self):
        """Initialize all system components"""
        try:
            self.logger.info("🚀 Initializing Phoenix components...")
            
            # 1. Initialize broker pair scanner
            self.pair_scanner = BrokerPairScanner(self.config.broker_config)
            if self.config.is_auto_connect_enabled():
                self.logger.info("🔗 Auto-connection enabled - connecting to broker...")
                try:
                    await self.pair_scanner.initialize()
                except Exception as e:
                    self.logger.warning(f"⚠️ Broker connection failed: {e}")
                    self.logger.info("📝 Continuing in demo mode...")
            else:
                self.logger.info("🔗 Auto-connection disabled - running in demo mode")
            
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
            
            self.is_initialized = True
            self.logger.info("✅ Phoenix initialization complete - Ready to rise!")
            
        except Exception as e:
            self.logger.error(f"❌ Phoenix initialization failed: {e}")
            raise
    
    async def start_trading(self):
        """Start the trading system"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            self.logger.info("🚀 Starting trading system...")
            
            # Start all components
            tasks = []
            
            if self.pair_scanner.is_connected:
                tasks.extend([
                    self.arbitrage_engine.start(),
                    self.recovery_system.start(),
                    self.profit_harvester.start()
                ])
            else:
                self.logger.warning("⚠️ Broker not connected - running in simulation mode")
                # In simulation mode, we could run mock trading
            
            self.is_running = True
            
            if tasks:
                # Run all components concurrently
                await asyncio.gather(*tasks)
            else:
                # Just keep running in demo mode
                await self.demo_mode()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Phoenix shutdown requested by user")
            await self.stop()
        except Exception as e:
            self.logger.error(f"💥 Phoenix encountered an error: {e}")
            await self.stop()
    
    async def demo_mode(self):
        """Run in demo mode without actual trading"""
        self.logger.info("🎭 Running in demo mode...")
        
        while self.is_running:
            # Print status every 30 seconds
            await asyncio.sleep(30)
            
            if self.is_running:
                self.print_status()
    
    def print_status(self):
        """Print current system status"""
        print("\n" + "="*60)
        print("🔥 ARBI PHOENIX - STATUS REPORT")
        print("="*60)
        
        # Connection status
        if self.pair_scanner:
            conn_status = self.pair_scanner.get_connection_status()
            status_icon = "🟢" if conn_status['is_connected'] else "🔴"
            print(f"{status_icon} Broker: {conn_status['status']}")
        
        # Engine status
        if self.arbitrage_engine:
            arb_status = self.arbitrage_engine.get_status()
            print(f"⚡ Arbitrage Engine: {arb_status['status']}")
            print(f"🎯 Opportunities Found: {arb_status['opportunities_found']}")
            print(f"✅ Success Rate: {arb_status['success_rate']:.1f}%")
            print(f"💰 Total Profit: ${arb_status['total_profit']:.2f}")
        
        # Recovery status
        if self.recovery_system:
            rec_status = self.recovery_system.get_status()
            print(f"🔄 Recovery System: {rec_status['status']}")
            print(f"🏥 Active Recoveries: {rec_status['active_recoveries']}")
        
        # Profit harvester status
        if self.profit_harvester:
            prof_status = self.profit_harvester.get_status()
            print(f"💎 Profit Harvester: {prof_status['status']}")
            print(f"📊 Total Harvested: ${prof_status['total_harvested']:.2f}")
        
        print("="*60)
    
    async def stop(self):
        """Stop the Phoenix system"""
        self.logger.info("🔄 Phoenix shutdown initiated...")
        
        self.is_running = False
        
        # Stop all components
        if self.profit_harvester:
            await self.profit_harvester.stop()
        
        if self.recovery_system:
            await self.recovery_system.stop()
        
        if self.arbitrage_engine:
            await self.arbitrage_engine.stop()
        
        if self.pair_scanner:
            await self.pair_scanner.disconnect()
        
        self.logger.info("✅ Phoenix shutdown complete")
    
    def get_status(self):
        """Get current system status"""
        return {
            'initialized': self.is_initialized,
            'running': self.is_running,
            'components': {
                'pair_scanner': self.pair_scanner is not None,
                'arbitrage_engine': self.arbitrage_engine is not None,
                'recovery_system': self.recovery_system is not None,
                'profit_harvester': self.profit_harvester is not None
            }
        }

def print_phoenix_banner():
    """Print the Phoenix startup banner"""
    banner = """
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    🔥                                                                  🔥
    🔥                     ARBI PHOENIX CONSOLE                        🔥
    🔥                                                                  🔥
    🔥              "From the ashes of loss, rises the                 🔥
    🔥                      phoenix of profit"                         🔥
    🔥                                                                  🔥
    🔥                Console Mode - No GUI Required                   🔥
    🔥                                                                  🔥
    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    
    ⚡ Features:
    • Triangular Arbitrage Engine
    • Multi-layer Recovery System  
    • Intelligent Profit Harvesting
    • Console-based Monitoring
    • Auto-connection & Auto-trading
    
    🛡️ "The Phoenix Never Dies" 🛡️
    
    Commands:
    • Ctrl+C: Stop trading and exit
    • Status updates every 30 seconds
    """
    print(banner)

async def main():
    """Main entry point for console mode"""
    print_phoenix_banner()
    
    # Create Phoenix console system
    phoenix = ArbiPhoenixConsole()
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        print(f"\n🔥 Received signal {signum} - Shutting down Phoenix...")
        asyncio.create_task(phoenix.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the system
        await phoenix.start_trading()
        
    except KeyboardInterrupt:
        print("\n🔥 Phoenix rising again soon...")
    except Exception as e:
        print(f"💥 Phoenix encountered an error: {e}")
        logging.exception("Phoenix error details:")
    finally:
        if phoenix.is_running:
            await phoenix.stop()

if __name__ == "__main__":
    # Run the Phoenix console
    asyncio.run(main())
