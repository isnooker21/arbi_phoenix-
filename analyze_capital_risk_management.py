#!/usr/bin/env python3
"""
🔥 Capital and Risk Management Analysis for Triangular Arbitrage
Analysis of capital-based position sizing and risk management
"""

import math

print('🔥 CAPITAL & RISK MANAGEMENT FOR TRIANGULAR ARBITRAGE')
print('=' * 65)

# Account scenarios
accounts = {
    'Small': {'balance': 1000, 'currency': 'USD'},
    'Medium': {'balance': 10000, 'currency': 'USD'}, 
    'Large': {'balance': 100000, 'currency': 'USD'}
}

# Risk levels
risk_levels = {
    'Conservative': 0.5,   # 0.5% per trade
    'Moderate': 1.0,       # 1.0% per trade
    'Aggressive': 2.0,     # 2.0% per trade
    'High Risk': 5.0       # 5.0% per trade
}

# Current market prices (example)
prices = {
    'EURUSD': 1.0950,
    'GBPUSD': 1.2650,
    'USDJPY': 150.25,
    'EURGBP': 0.8656
}

def calculate_usd_value_per_lot(pair, price):
    """Calculate USD value of 1 lot for a currency pair"""
    base_currency = pair[:3]
    quote_currency = pair[3:6]
    
    if quote_currency == 'USD':
        # Direct USD quote (e.g., EURUSD = 1.0950)
        return 100000 * price  # 1 lot = 100,000 base currency
    elif base_currency == 'USD':
        # USD base (e.g., USDJPY = 150.25)
        return 100000  # 1 lot = 100,000 USD
    else:
        # Cross pair - convert to USD
        if base_currency == 'EUR':
            eur_usd = prices['EURUSD']
            return 100000 * eur_usd
        elif base_currency == 'GBP':
            gbp_usd = prices['GBPUSD'] 
            return 100000 * gbp_usd
        else:
            return 100000  # Default approximation

def calculate_pip_value(pair, lot_size, account_currency='USD'):
    """Calculate pip value for position sizing"""
    quote_currency = pair[3:6]
    
    if quote_currency == 'USD' or quote_currency == account_currency:
        # Standard calculation
        if 'JPY' in pair:
            pip_value = lot_size * 100000 * 0.01  # JPY pairs: 0.01 = 1 pip
        else:
            pip_value = lot_size * 100000 * 0.0001  # Standard pairs: 0.0001 = 1 pip
    else:
        # Cross currency calculation (simplified)
        pip_value = lot_size * 100000 * 0.0001
        # Convert to account currency if needed
        
    return pip_value

def calculate_risk_based_position_size(account_balance, risk_percent, stop_loss_pips, pair):
    """Calculate position size based on risk management"""
    
    # Maximum risk in account currency
    max_risk_amount = account_balance * (risk_percent / 100)
    
    # Calculate pip value for 1 lot
    pip_value_per_lot = calculate_pip_value(pair, 1.0)
    
    # Calculate maximum lot size based on risk
    if stop_loss_pips > 0:
        max_lot_size = max_risk_amount / (stop_loss_pips * pip_value_per_lot)
    else:
        # If no stop loss, use conservative approach
        max_lot_size = max_risk_amount / (100000 * 0.02)  # Assume 2% price movement
    
    return max_lot_size

print('📊 ACCOUNT BALANCE & RISK SCENARIOS:')
print('-' * 50)

triangle_pairs = ['EURUSD', 'GBPUSD', 'EURGBP']
stop_loss_pips = 20  # Typical stop loss for arbitrage

for account_name, account_info in accounts.items():
    balance = account_info['balance']
    print(f'\n💰 {account_name} Account: ${balance:,}')
    print('   Risk Level → Max Risk → Triangle Lot Sizes')
    
    for risk_name, risk_percent in risk_levels.items():
        max_risk = balance * (risk_percent / 100)
        
        # Calculate lot sizes for each pair in triangle
        total_triangle_risk = max_risk / 3  # Divide risk among 3 legs
        
        lot_sizes = []
        for pair in triangle_pairs:
            lot_size = calculate_risk_based_position_size(
                balance, risk_percent/3, stop_loss_pips, pair
            )
            
            # Apply broker constraints
            min_lot = 0.01
            max_lot = min(lot_size, balance / 10000)  # Conservative max
            final_lot = max(min_lot, min(max_lot, lot_size))
            
            lot_sizes.append(final_lot)
        
        avg_lot = sum(lot_sizes) / len(lot_sizes)
        print(f'   {risk_name:<12} → ${max_risk:>6.0f} → {avg_lot:.4f} lot avg')

print('\n🎯 TRIANGLE ARBITRAGE RISK CALCULATION:')
print('-' * 50)

# Example calculation for $10,000 account with 1% risk
account_balance = 10000
risk_percent = 1.0
max_risk_per_triangle = account_balance * (risk_percent / 100)

print(f'Account Balance: ${account_balance:,}')
print(f'Risk per Triangle: {risk_percent}% = ${max_risk_per_triangle:.0f}')
print(f'Risk per Leg: ${max_risk_per_triangle/3:.0f}')

print('\nTriangle: EUR/USD - GBP/USD - EUR/GBP')
print('Lot Size Calculation:')

for pair in triangle_pairs:
    usd_value_per_lot = calculate_usd_value_per_lot(pair, prices[pair])
    pip_value_per_lot = calculate_pip_value(pair, 1.0)
    
    # Risk-based lot calculation
    risk_per_leg = max_risk_per_triangle / 3
    max_lot_by_risk = risk_per_leg / (stop_loss_pips * pip_value_per_lot)
    
    # Capital-based lot calculation  
    max_lot_by_capital = (account_balance * 0.1) / usd_value_per_lot  # Max 10% capital per leg
    
    # Final lot size (minimum of constraints)
    final_lot = min(max_lot_by_risk, max_lot_by_capital, 1.0)  # Max 1 lot
    final_lot = max(final_lot, 0.01)  # Min 0.01 lot
    
    print(f'\n{pair}:')
    print(f'  USD Value/Lot: ${usd_value_per_lot:,.0f}')
    print(f'  Pip Value/Lot: ${pip_value_per_lot:.2f}')
    print(f'  Max by Risk: {max_lot_by_risk:.4f} lot')
    print(f'  Max by Capital: {max_lot_by_capital:.4f} lot')
    print(f'  Final Lot Size: {final_lot:.4f} lot')
    print(f'  Capital Used: ${final_lot * usd_value_per_lot:,.0f} ({final_lot * usd_value_per_lot / account_balance * 100:.1f}%)')

print('\n🔧 DYNAMIC RISK ADJUSTMENT METHODS:')
print('-' * 50)

adjustment_methods = {
    'Fixed Percentage': {
        'description': 'ใช้เปอร์เซ็นต์ความเสี่ยงคงที่',
        'formula': 'Lot = (Balance × Risk%) ÷ (Stop Loss × Pip Value)',
        'pros': 'ง่าย, เสถียร',
        'cons': 'ไม่ปรับตามสภาพตลาด'
    },
    'Volatility Adjusted': {
        'description': 'ปรับตาม ATR (Average True Range)',
        'formula': 'Lot = Base Lot × (Normal ATR ÷ Current ATR)',
        'pros': 'ปรับตามความผันผวน',
        'cons': 'ซับซ้อนกว่า'
    },
    'Kelly Criterion': {
        'description': 'ปรับตามความน่าจะเป็นชนะ',
        'formula': 'f = (bp - q) ÷ b',
        'pros': 'เหมาะสมทางคณิตศาสตร์',
        'cons': 'ต้องมีข้อมูลประวัติ'
    },
    'Triangle Balance': {
        'description': 'ปรับให้ Triangle สมดุล',
        'formula': 'Equal USD exposure across all legs',
        'pros': 'ลด Currency Risk',
        'cons': 'อาจขัดกับ Broker Constraints'
    }
}

for method, info in adjustment_methods.items():
    print(f'\n🎯 {method}:')
    print(f'   📝 {info["description"]}')
    print(f'   🧮 {info["formula"]}')
    print(f'   ✅ ข้อดี: {info["pros"]}')
    print(f'   ⚠️ ข้อเสีย: {info["cons"]}')

print('\n💡 RECOMMENDED IMPLEMENTATION:')
print('=' * 65)

print('Phase 1: Basic Capital Management')
print('• คำนวณ lot size จาก account balance')
print('• ตั้ง maximum risk per triangle (1-2%)')
print('• ใช้ fixed stop loss distance')
print('')

print('Phase 2: Risk-Adjusted Sizing')
print('• เพิ่ม volatility consideration')
print('• ปรับ lot size ตาม market conditions')
print('• เพิ่ม correlation analysis')
print('')

print('Phase 3: Advanced Portfolio Management')
print('• Kelly Criterion optimization')
print('• Multi-timeframe risk analysis')
print('• Dynamic correlation monitoring')
print('')

print('🔧 CONFIG STRUCTURE:')
print('-' * 30)
config_example = '''
risk_management:
  account_balance: 10000        # Account balance in USD
  risk_per_triangle: 1.0        # Risk percentage per triangle
  max_capital_per_leg: 10.0     # Max capital percentage per leg
  stop_loss_pips: 20            # Default stop loss in pips
  
  position_sizing:
    method: "risk_adjusted"      # fixed, risk_adjusted, kelly
    min_lot: 0.01               # Broker minimum
    max_lot: 10.0               # System maximum
    lot_step: 0.01              # Broker step size
    
  dynamic_adjustment:
    volatility_factor: true     # Adjust for volatility
    correlation_factor: true    # Consider pair correlations
    balance_triangle: true      # Balance USD exposure
'''

print(config_example)

print('📊 EXPECTED RESULTS:')
print('-' * 30)
print('• Consistent risk per trade regardless of account size')
print('• Automatic position sizing based on available capital')
print('• Protection against over-leveraging')
print('• Balanced triangle exposure')
print('• Scalable from $1K to $100K+ accounts')
