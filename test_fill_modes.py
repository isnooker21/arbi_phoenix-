#!/usr/bin/env python3
"""
🔥 ARBI PHOENIX - Fill Mode Testing
Test script for order execution and fill modes across different brokers

"Testing the Phoenix execution power"
"""

import sys
import asyncio
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from phoenix_brokers.order_executor import (
    BrokerOrderExecutor, OrderRequest, OrderType, FillMode, OrderStatus
)
from phoenix_utils.logger import setup_logger

async def test_broker_capabilities():
    """Test broker capabilities and fill modes"""
    print("🔥 ARBI PHOENIX - FILL MODE TESTING")
    print("=" * 60)
    
    logger = setup_logger("FillModeTest")
    
    # Test different brokers
    brokers_to_test = [
        ('MT5', {'default_fill_mode': 'IOC'}),
        ('MT4', {'default_fill_mode': 'INSTANT'}), 
        ('CTRADER', {'default_fill_mode': 'FOK'}),
        ('IB', {'default_fill_mode': 'IOC'}),
        ('OANDA', {'default_fill_mode': 'IOC'}),
        ('FXCM', {'default_fill_mode': 'MARKET'})
    ]
    
    for broker_type, config in brokers_to_test:
        print(f"\n🎯 Testing {broker_type}")
        print("-" * 40)
        
        try:
            # Create executor
            executor = BrokerOrderExecutor(broker_type, config)
            
            # Get capabilities
            capabilities = executor.get_broker_capabilities()
            
            print(f"✅ Broker Type: {capabilities['broker_type']}")
            print(f"📊 Supported Fill Modes: {', '.join(capabilities['supported_fill_modes'])}")
            print(f"🎯 Market Execution: {capabilities['market_execution']}")
            print(f"⚡ Instant Execution: {capabilities['instant_execution']}")
            print(f"📋 Request Execution: {capabilities['request_execution']}")
            print(f"📏 Max Deviation: {capabilities['max_deviation']}")
            print(f"📦 Min Volume: {capabilities['min_volume']}")
            print(f"📈 Volume Step: {capabilities['volume_step']}")
            
            # Test fill mode adjustment
            print(f"\n🔄 Fill Mode Adjustment Test:")
            test_modes = [FillMode.IOC, FillMode.FOK, FillMode.MARKET, FillMode.GTC]
            
            for mode in test_modes:
                adjusted = executor._adjust_fill_mode(mode)
                status = "✅" if adjusted == mode else "🔄"
                print(f"  {status} {mode.value} → {adjusted.value}")
            
        except Exception as e:
            print(f"❌ Error testing {broker_type}: {e}")

async def test_order_creation():
    """Test order creation with different fill modes"""
    print(f"\n🎯 ORDER CREATION TEST")
    print("-" * 40)
    
    # Create MT5 executor for testing
    executor = BrokerOrderExecutor('MT5', {'default_fill_mode': 'IOC'})
    
    # Test different order types and fill modes
    test_orders = [
        {
            'symbol': 'EURUSD',
            'order_type': OrderType.MARKET_BUY,
            'volume': 0.01,
            'fill_mode': FillMode.IOC,
            'comment': 'Test IOC Order'
        },
        {
            'symbol': 'GBPUSD', 
            'order_type': OrderType.MARKET_SELL,
            'volume': 0.01,
            'fill_mode': FillMode.FOK,
            'comment': 'Test FOK Order'
        },
        {
            'symbol': 'USDJPY',
            'order_type': OrderType.LIMIT_BUY,
            'volume': 0.01,
            'price': 150.000,
            'fill_mode': FillMode.GTC,
            'comment': 'Test GTC Limit Order'
        }
    ]
    
    for i, order_data in enumerate(test_orders, 1):
        print(f"\n📋 Test Order {i}:")
        
        try:
            # Create order request
            order_request = OrderRequest(**order_data)
            
            print(f"  Symbol: {order_request.symbol}")
            print(f"  Type: {order_request.order_type.value}")
            print(f"  Volume: {order_request.volume}")
            print(f"  Fill Mode: {order_request.fill_mode.value}")
            print(f"  Comment: {order_request.comment}")
            
            # Validate order (without executing)
            is_valid = executor._validate_order_request(order_request)
            print(f"  Validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
            # Test fill mode adjustment
            adjusted_mode = executor._adjust_fill_mode(order_request.fill_mode)
            if adjusted_mode != order_request.fill_mode:
                print(f"  Fill Mode Adjusted: {order_request.fill_mode.value} → {adjusted_mode.value}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

async def test_triangle_execution_simulation():
    """Test triangle arbitrage execution simulation"""
    print(f"\n🔺 TRIANGLE ARBITRAGE SIMULATION")
    print("-" * 40)
    
    executor = BrokerOrderExecutor('MT5', {
        'default_fill_mode': 'IOC',
        'max_deviation': 10,
        'execution_timeout': 5.0
    })
    
    # Simulate triangle execution
    print("🎯 Simulating Triangle: EUR/USD - GBP/USD - EUR/GBP")
    print("📊 Forward Direction: BUY EUR/USD, BUY GBP/USD, SELL EUR/GBP")
    
    try:
        # Note: This won't actually execute since no connection is set
        # It will test the order creation and validation logic
        
        pairs = ['EURUSD', 'GBPUSD', 'EURGBP']
        volumes = [0.01, 0.01, 0.01]
        directions = ['buy', 'buy', 'sell']
        
        print(f"\n📋 Triangle Orders:")
        for i, (pair, volume, direction) in enumerate(zip(pairs, volumes, directions), 1):
            order_type = OrderType.MARKET_BUY if direction == 'buy' else OrderType.MARKET_SELL
            
            order_request = OrderRequest(
                symbol=pair,
                order_type=order_type,
                volume=volume,
                fill_mode=FillMode.IOC,
                comment=f"Phoenix Triangle {i}/3"
            )
            
            is_valid = executor._validate_order_request(order_request)
            print(f"  {i}. {direction.upper()} {pair} {volume} lots - {'✅' if is_valid else '❌'}")
        
        print(f"\n⚡ Execution Mode: IOC (Immediate or Cancel)")
        print(f"🎯 Expected Behavior: All 3 orders execute simultaneously")
        print(f"⏱️ Timeout: 5.0 seconds")
        print(f"📊 Success Criteria: ≥67% orders filled (2/3)")
        
    except Exception as e:
        print(f"❌ Simulation error: {e}")

async def show_fill_mode_comparison():
    """Show comparison of fill modes"""
    print(f"\n📊 FILL MODE COMPARISON")
    print("=" * 60)
    
    fill_modes = {
        'IOC': {
            'name': 'Immediate or Cancel',
            'description': 'Execute immediately, cancel unfilled portion',
            'best_for': 'Fast arbitrage, partial fills OK',
            'risk': 'Medium',
            'speed': 'Very Fast'
        },
        'FOK': {
            'name': 'Fill or Kill',
            'description': 'Execute completely or cancel entirely',
            'best_for': 'All-or-nothing strategies',
            'risk': 'Low',
            'speed': 'Very Fast'
        },
        'MARKET': {
            'name': 'Market Execution',
            'description': 'Execute at best available price',
            'best_for': 'Guaranteed execution',
            'risk': 'High (slippage)',
            'speed': 'Fast'
        },
        'GTC': {
            'name': 'Good Till Cancelled',
            'description': 'Stay active until filled or cancelled',
            'best_for': 'Limit orders, patient strategies',
            'risk': 'Low',
            'speed': 'Slow'
        },
        'INSTANT': {
            'name': 'Instant Execution',
            'description': 'Execute at quoted price or reject',
            'best_for': 'Price-sensitive strategies',
            'risk': 'Medium',
            'speed': 'Very Fast'
        }
    }
    
    for mode, info in fill_modes.items():
        print(f"\n🎯 {mode} - {info['name']}")
        print(f"   📝 {info['description']}")
        print(f"   💡 Best for: {info['best_for']}")
        print(f"   ⚠️ Risk: {info['risk']}")
        print(f"   ⚡ Speed: {info['speed']}")

async def main():
    """Main test function"""
    try:
        await test_broker_capabilities()
        await test_order_creation()
        await test_triangle_execution_simulation()
        await show_fill_mode_comparison()
        
        print(f"\n🎉 FILL MODE TESTING COMPLETE!")
        print("=" * 60)
        print("📝 Summary:")
        print("• All brokers have different fill mode capabilities")
        print("• IOC/FOK modes are best for arbitrage (speed + control)")
        print("• System automatically adjusts unsupported fill modes")
        print("• Triangle execution uses simultaneous order placement")
        print("• Success criteria: ≥67% order fill rate")
        
    except Exception as e:
        print(f"💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
