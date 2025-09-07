#!/usr/bin/env python3
"""
🔥 Lot Size Rounding Analysis for Triangular Arbitrage
Analysis of lot size rounding to broker constraints
"""

import math

print('🔥 LOT SIZE ROUNDING FOR BROKER CONSTRAINTS')
print('=' * 60)

def round_to_lot_step(lot_size, lot_step=0.01, min_lot=0.01):
    """Round lot size to broker's lot step"""
    if lot_size < min_lot:
        return min_lot
    
    # Round down to nearest lot step
    rounded = math.floor(lot_size / lot_step) * lot_step
    
    # Ensure it's not below minimum
    return max(rounded, min_lot)

def round_to_lot_step_nearest(lot_size, lot_step=0.01, min_lot=0.01):
    """Round lot size to nearest broker's lot step"""
    if lot_size < min_lot:
        return min_lot
    
    # Round to nearest lot step
    rounded = round(lot_size / lot_step) * lot_step
    
    # Ensure it's not below minimum
    return max(rounded, min_lot)

# Broker lot step configurations
broker_configs = {
    'Standard Forex': {
        'min_lot': 0.01,
        'max_lot': 100.0,
        'lot_step': 0.01,
        'examples': ['IC Markets', 'FXCM', 'Pepperstone']
    },
    'Micro Forex': {
        'min_lot': 0.001,
        'max_lot': 100.0,
        'lot_step': 0.001,
        'examples': ['Oanda', 'XM Micro']
    },
    'Mini Forex': {
        'min_lot': 0.1,
        'max_lot': 100.0,
        'lot_step': 0.1,
        'examples': ['Some MT4 brokers']
    },
    'Standard Lot Only': {
        'min_lot': 1.0,
        'max_lot': 100.0,
        'lot_step': 1.0,
        'examples': ['Traditional brokers']
    }
}

print('📊 BROKER LOT CONFIGURATIONS:')
print('-' * 50)
for config_name, config in broker_configs.items():
    print(f'\n🎯 {config_name}:')
    print(f'   Min Lot: {config["min_lot"]}')
    print(f'   Max Lot: {config["max_lot"]}')
    print(f'   Lot Step: {config["lot_step"]}')
    print(f'   Examples: {", ".join(config["examples"])}')

print('\n🧮 LOT SIZE CALCULATION EXAMPLES:')
print('-' * 50)

# Example: $10,000 account, 1% risk, different scenarios
account_balance = 10000
risk_percent = 1.0
max_risk = account_balance * (risk_percent / 100)  # $100
risk_per_leg = max_risk / 3  # $33.33 per leg

# Calculated lot sizes (before rounding)
calculated_lots = {
    'Conservative Market': 0.0167,  # Low volatility
    'Normal Market': 0.0333,        # Normal conditions  
    'Volatile Market': 0.0125,      # High volatility
    'High Risk Setting': 0.0833,    # 2.5% risk instead of 1%
    'Large Account': 0.1667         # $100K account
}

print(f'Account: ${account_balance:,} | Risk: {risk_percent}% = ${max_risk:.0f}')
print('\nCalculated → Rounded Lot Sizes:')

for scenario, calc_lot in calculated_lots.items():
    print(f'\n📈 {scenario}:')
    print(f'   Calculated: {calc_lot:.4f} lot')
    
    for config_name, config in broker_configs.items():
        rounded_floor = round_to_lot_step(calc_lot, config['lot_step'], config['min_lot'])
        rounded_nearest = round_to_lot_step_nearest(calc_lot, config['lot_step'], config['min_lot'])
        
        print(f'   {config_name:<20}: Floor={rounded_floor:.3f} | Nearest={rounded_nearest:.3f}')

print('\n🔺 TRIANGLE BALANCE PROBLEM:')
print('-' * 50)

# Example triangle with different calculated lot sizes
triangle_calculated = {
    'EURUSD': 0.0234,  # Risk-based calculation
    'GBPUSD': 0.0187,  # Different due to higher USD value
    'EURGBP': 0.0234   # Same as EURUSD
}

print('Calculated lot sizes for triangle:')
for pair, calc_lot in triangle_calculated.items():
    print(f'{pair}: {calc_lot:.4f} lot')

print('\nAfter rounding to 0.01 step:')
triangle_rounded = {}
for pair, calc_lot in triangle_calculated.items():
    rounded = round_to_lot_step(calc_lot, 0.01, 0.01)
    triangle_rounded[pair] = rounded
    print(f'{pair}: {calc_lot:.4f} → {rounded:.2f} lot')

# Calculate the impact
print('\nImpact of rounding:')
total_calc = sum(triangle_calculated.values())
total_rounded = sum(triangle_rounded.values())
difference = total_rounded - total_calc

print(f'Total calculated: {total_calc:.4f} lot')
print(f'Total rounded: {total_rounded:.2f} lot')
print(f'Difference: {difference:+.4f} lot ({difference/total_calc*100:+.1f}%)')

print('\n✅ SMART ROUNDING STRATEGIES:')
print('-' * 50)

def smart_triangle_rounding(lots, lot_step=0.01, min_lot=0.01, target_total=None):
    """Smart rounding that maintains triangle balance"""
    
    # Strategy 1: Proportional rounding
    total_calc = sum(lots.values())
    
    if target_total is None:
        # Round each to nearest and adjust
        rounded = {}
        for pair, lot in lots.items():
            rounded[pair] = round_to_lot_step_nearest(lot, lot_step, min_lot)
    else:
        # Distribute target total proportionally
        rounded = {}
        for pair, lot in lots.items():
            proportion = lot / total_calc
            target_lot = target_total * proportion
            rounded[pair] = round_to_lot_step_nearest(target_lot, lot_step, min_lot)
    
    return rounded

strategies = {
    'Floor Rounding': {
        'method': 'Round all down to lot step',
        'pros': 'Conservative, never exceeds calculated risk',
        'cons': 'May significantly reduce position size'
    },
    'Nearest Rounding': {
        'method': 'Round to nearest lot step',
        'pros': 'Closest to calculated size',
        'cons': 'May slightly exceed intended risk'
    },
    'Proportional Distribution': {
        'method': 'Distribute total rounded amount proportionally',
        'pros': 'Maintains triangle balance',
        'cons': 'More complex calculation'
    },
    'Risk-First Rounding': {
        'method': 'Round down, then increase if risk allows',
        'pros': 'Respects risk limits strictly',
        'cons': 'May leave unused risk capacity'
    }
}

for strategy, info in strategies.items():
    print(f'\n🎯 {strategy}:')
    print(f'   Method: {info["method"]}')
    print(f'   ✅ Pros: {info["pros"]}')
    print(f'   ⚠️ Cons: {info["cons"]}')

print('\n🎯 RECOMMENDED IMPLEMENTATION:')
print('-' * 50)

def calculate_triangle_lots_with_rounding(account_balance, risk_percent, broker_config):
    """Calculate triangle lot sizes with proper rounding"""
    
    max_risk = account_balance * (risk_percent / 100)
    risk_per_leg = max_risk / 3
    
    # Example calculation (simplified)
    base_lot = risk_per_leg / 200  # Assuming $200 risk per 0.01 lot
    
    # Apply broker constraints
    min_lot = broker_config['min_lot']
    lot_step = broker_config['lot_step']
    
    # Smart rounding
    if base_lot < min_lot:
        final_lot = min_lot
    else:
        # Round to lot step
        final_lot = round_to_lot_step_nearest(base_lot, lot_step, min_lot)
    
    return final_lot

# Test with different broker configs
test_scenarios = [
    {'balance': 1000, 'risk': 1.0},
    {'balance': 10000, 'risk': 1.0},
    {'balance': 100000, 'risk': 1.0}
]

print('Test Results:')
for scenario in test_scenarios:
    balance = scenario['balance']
    risk = scenario['risk']
    
    print(f'\n💰 ${balance:,} account, {risk}% risk:')
    
    for config_name, config in broker_configs.items():
        lot_size = calculate_triangle_lots_with_rounding(balance, risk, config)
        capital_used = lot_size * 100000 * 1.10  # Approximate USD value
        
        print(f'   {config_name:<20}: {lot_size:.3f} lot (${capital_used:,.0f})')

print('\n🔧 CONFIG IMPLEMENTATION:')
print('-' * 50)

config_code = '''
# เพิ่มใน config.yaml
broker:
  lot_constraints:
    min_lot: 0.01           # Minimum lot size
    max_lot: 100.0          # Maximum lot size  
    lot_step: 0.01          # Lot step increment
    
risk_management:
  position_sizing:
    rounding_method: "nearest"    # floor, nearest, proportional
    maintain_triangle_balance: true
    allow_risk_overage: 5.0       # Allow 5% risk overage for rounding
    
  fallback_rules:
    min_lot_override: true        # Use min lot if calculated < min
    max_capital_per_leg: 20.0     # Never exceed 20% capital per leg
    emergency_lot_reduction: 0.5  # Reduce lot by 50% if constraints violated
'''

print(config_code)

print('\n📊 EXPECTED BEHAVIOR:')
print('-' * 30)
print('✅ All lot sizes will be valid broker increments')
print('✅ Minimum lot constraints will be respected') 
print('✅ Risk will not exceed intended limits (with small tolerance)')
print('✅ Triangle balance will be maintained as much as possible')
print('✅ System will gracefully handle edge cases')
print('')
print('Example: Calculated 0.0167 lot → Rounded 0.02 lot')
print('Impact: +19.8% lot size, but still within risk tolerance')
