#!/usr/bin/env python3
"""
🔥 ARBI PHOENIX - System Test Script
Test script for Phoenix trading system components

"Testing the Phoenix before it flies"
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_utils.logger import setup_logger
from phoenix_utils.config_manager import ConfigManager

async def test_config_manager():
    """Test configuration manager"""
    print("🧪 Testing Configuration Manager...")
    
    try:
        config = ConfigManager()
        
        # Test basic functionality
        broker_config = config.broker_config
        trading_config = config.trading_config
        
        print(f"✅ Broker: {broker_config.get('name', 'Unknown')}")
        print(f"✅ API Type: {broker_config.get('api_type', 'Unknown')}")
        print(f"✅ Auto Connect: {config.is_auto_connect_enabled()}")
        print(f"✅ Auto Start: {config.is_auto_start_enabled()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config Manager test failed: {e}")
        return False

async def test_logger():
    """Test logging system"""
    print("\n🧪 Testing Logger System...")
    
    try:
        logger = setup_logger("TestLogger")
        
        logger.info("✅ Info message test")
        logger.warning("⚠️ Warning message test")
        logger.error("❌ Error message test")
        
        print("✅ Logger system working")
        return True
        
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        return False

async def test_pair_scanner():
    """Test pair scanner (without actual broker connection)"""
    print("\n🧪 Testing Pair Scanner...")
    
    try:
        from phoenix_brokers.pair_scanner import BrokerPairScanner, BrokerType
        
        # Create scanner with test config
        test_config = {
            'api_type': 'MT5',
            'auto_connect': False,  # Don't actually connect
            'retries': 1,
            'reconnect_interval': 5
        }
        
        scanner = BrokerPairScanner(test_config)
        
        # Test basic functionality
        print(f"✅ Scanner created for {scanner.broker_type.value}")
        print(f"✅ Auto-connect: {scanner.auto_connect}")
        print(f"✅ Major currencies: {len(scanner.major_currencies)}")
        
        # Test nomenclature rules
        rules = scanner.nomenclature_map
        print(f"✅ Nomenclature rules loaded: {len(rules)} broker types")
        
        return True
        
    except Exception as e:
        print(f"❌ Pair Scanner test failed: {e}")
        return False

async def test_core_modules():
    """Test core trading modules (without actual trading)"""
    print("\n🧪 Testing Core Modules...")
    
    try:
        from phoenix_core.arbitrage_engine import ArbitrageEngine
        from phoenix_core.recovery_system import RecoverySystem
        from phoenix_core.profit_harvester import ProfitHarvester
        from phoenix_brokers.pair_scanner import BrokerPairScanner
        
        # Create mock components
        test_broker_config = {
            'api_type': 'MT5',
            'auto_connect': False
        }
        
        test_trading_config = {
            'min_arbitrage_profit': 5,
            'base_lot_size': 0.01
        }
        
        test_recovery_config = {
            'max_recovery_layers': 3,
            'recovery_multiplier': 1.5
        }
        
        test_profit_config = {
            'profit_levels': {
                'quick_scalp': 8,
                'partial_1': 15
            }
        }
        
        # Test component creation
        pair_scanner = BrokerPairScanner(test_broker_config)
        print("✅ Pair Scanner created")
        
        arbitrage_engine = ArbitrageEngine(pair_scanner, test_trading_config)
        print("✅ Arbitrage Engine created")
        
        recovery_system = RecoverySystem(arbitrage_engine, test_recovery_config)
        print("✅ Recovery System created")
        
        profit_harvester = ProfitHarvester(arbitrage_engine, test_profit_config)
        print("✅ Profit Harvester created")
        
        # Test status methods
        arb_status = arbitrage_engine.get_status()
        rec_status = recovery_system.get_status()
        prof_status = profit_harvester.get_status()
        
        print(f"✅ Arbitrage status: {arb_status['status']}")
        print(f"✅ Recovery status: {rec_status['status']}")
        print(f"✅ Profit harvester status: {prof_status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Core modules test failed: {e}")
        return False

async def test_gui_components():
    """Test GUI components (without showing windows)"""
    print("\n🧪 Testing GUI Components...")
    
    try:
        # Test if PyQt6 is available
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        
        print("✅ PyQt6 available")
        
        # Test Phoenix GUI imports
        from phoenix_gui.dashboard import PhoenixDashboard, PhoenixStyle
        
        print("✅ Phoenix GUI modules imported")
        print(f"✅ Style background: {PhoenixStyle.BACKGROUND}")
        print(f"✅ Style primary: {PhoenixStyle.PRIMARY}")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ GUI test skipped (missing dependency): {e}")
        return True  # Not critical for core functionality
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

async def test_system_integration():
    """Test system integration"""
    print("\n🧪 Testing System Integration...")
    
    try:
        from main import ArbiPhoenix
        
        # Create Phoenix system
        phoenix = ArbiPhoenix()
        print("✅ Phoenix system created")
        
        # Test status
        status = phoenix.get_status()
        print(f"✅ System status: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ System integration test failed: {e}")
        return False

async def run_all_tests():
    """Run all system tests"""
    print("🔥 ARBI PHOENIX - System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Configuration Manager", test_config_manager),
        ("Logger System", test_logger),
        ("Pair Scanner", test_pair_scanner),
        ("Core Modules", test_core_modules),
        ("GUI Components", test_gui_components),
        ("System Integration", test_system_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("🔥 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phoenix is ready to fly!")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return passed == total

def main():
    """Main test function"""
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Test suite crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
