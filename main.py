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
            
            # 1. Initialize broker pair scanner
            self.pair_scanner = BrokerPairScanner(self.config.broker_config)
            await self.pair_scanner.initialize()
            
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
            
        except Exception as e:
            self.logger.error(f"❌ Phoenix initialization failed: {e}")
            raise
    
    async def start(self):
        """Start the Phoenix trading system"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            self.logger.info("🔥 Starting Arbi Phoenix - The hunt begins!")
            
            # Start all components
            tasks = [
                self.arbitrage_engine.start(),
                self.recovery_system.start(),
                self.profit_harvester.start(),
                self.dashboard.start()
            ]
            
            self.is_running = True
            
            # Run all components concurrently
            await asyncio.gather(*tasks)
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Phoenix shutdown requested by user")
            await self.stop()
        except Exception as e:
            self.logger.error(f"💥 Phoenix encountered an error: {e}")
            await self.emergency_stop()
    
    async def stop(self):
        """Gracefully stop the Phoenix system"""
        self.logger.info("🔄 Phoenix shutdown initiated - Preparing for rebirth...")
        
        self.is_running = False
        
        # Stop all components gracefully
        if self.profit_harvester:
            await self.profit_harvester.stop()
        
        if self.recovery_system:
            await self.recovery_system.stop()
        
        if self.arbitrage_engine:
            await self.arbitrage_engine.stop()
        
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

async def main():
    """Main entry point"""
    print_phoenix_banner()
    
    # Create and start Phoenix
    phoenix = ArbiPhoenix()
    
    try:
        await phoenix.start()
    except KeyboardInterrupt:
        print("\n🔥 Phoenix rising again soon...")
    except Exception as e:
        print(f"💥 Phoenix encountered an error: {e}")
        logging.exception("Phoenix error details:")
    finally:
        if phoenix.is_running:
            await phoenix.stop()

if __name__ == "__main__":
    # Run the Phoenix
    asyncio.run(main())
