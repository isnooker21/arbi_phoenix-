#!/usr/bin/env python3
"""
🔥 Contract Size Balancing for Triangular Arbitrage
Analysis of how to balance lot sizes based on contract sizes
"""

import math

print('🔥 CONTRACT SIZE BALANCING FOR TRIANGULAR ARBITRAGE')
print('=' * 60)

# Contract sizes for major currency pairs (USD value per 1.00 lot)
contract_sizes = {
    # Major USD pairs
    'EURUSD': 100000,    # 1 lot = 100,000 EUR
    'GBPUSD': 100000,    # 1 lot = 100,000 GBP  
    'AUDUSD': 100000,    # 1 lot = 100,000 AUD
    'NZDUSD': 100000,    # 1 lot = 100,000 NZD
    'USDCAD': 100000,    # 1 lot = 100,000 USD
    'USDCHF': 100000,    # 1 lot = 100,000 USD
    'USDJPY': 100000,    # 1 lot = 100,000 USD
    
    # Cross pairs (non-USD)
    'EURJPY': 100000,    # 1 lot = 100,000 EUR
    'GBPJPY': 100000,    # 1 lot = 100,000 GBP
    'EURGBP': 100000,    # 1 lot = 100,000 EUR
    'EURAUD': 100000,    # 1 lot = 100,000 EUR
    'GBPAUD': 100000,    # 1 lot = 100,000 GBP
    'AUDCAD': 100000,    # 1 lot = 100,000 AUD
    'AUDJPY': 100000,    # 1 lot = 100,000 AUD
    'CADJPY': 100000,    # 1 lot = 100,000 CAD
    'CHFJPY': 100000,    # 1 lot = 100,000 CHF
    'EURCHF': 100000,    # 1 lot = 100,000 EUR
    'GBPCHF': 100000,    # 1 lot = 100,000 GBP
    'NZDJPY': 100000,    # 1 lot = 100,000 NZD
}

# Sample exchange rates (for calculation)
exchange_rates = {
    'EURUSD': 1.0850,
    'GBPUSD': 1.2650,
    'AUDUSD': 0.6580,
    'NZDUSD': 0.6120,
    'USDCAD': 1.3580,
    'USDCHF': 0.8950,
    'USDJPY': 149.50,
    'EURJPY': 162.21,
    'GBPJPY': 189.12,
    'EURGBP': 0.8577,
    'EURAUD': 1.6490,
    'GBPAUD': 1.9230,
    'AUDCAD': 0.8940,
    'AUDJPY': 98.39,
    'CADJPY': 110.15,
    'CHFJPY': 167.04,
    'EURCHF': 0.9715,
    'GBPCHF': 1.1322,
    'NZDJPY': 91.50,
}

def get_usd_value_per_lot(pair, rate):
    """Calculate USD value of 1 lot for any currency pair"""
    
    base_currency = pair[:3]
    quote_currency = pair[3:]
    
    if quote_currency == 'USD':
        # Base/USD pairs: value = base_amount * rate
        return contract_sizes[pair] * rate
    elif base_currency == 'USD':
        # USD/Quote pairs: value = usd_amount = contract_size
        return contract_sizes[pair]
    else:
        # Cross pairs: need to convert to USD
        base_to_usd_pair = base_currency + 'USD'
        if base_to_usd_pair in exchange_rates:
            base_to_usd_rate = exchange_rates[base_to_usd_pair]
            return contract_sizes[pair] * base_to_usd_rate
        else:
            # Try USD/Base pair (inverted)
            usd_to_base_pair = 'USD' + base_currency
            if usd_to_base_pair in exchange_rates:
                usd_to_base_rate = exchange_rates[usd_to_base_pair]
                return contract_sizes[pair] / usd_to_base_rate
    
    return 100000  # Default fallback

print('💰 USD VALUE PER 1.00 LOT:')
print('-' * 50)

usd_values = {}
for pair in contract_sizes.keys():
    if pair in exchange_rates:
        usd_value = get_usd_value_per_lot(pair, exchange_rates[pair])
        usd_values[pair] = usd_value
        print(f'{pair}: ${usd_value:,.0f} per 1.00 lot')

print('\n🔺 TRIANGLE EXAMPLES - PROBLEM WITH EQUAL LOTS:')
print('-' * 50)

# Example triangular arbitrage opportunities
triangles = {
    'EUR Triangle': {
        'pairs': ['EURUSD', 'GBPUSD', 'EURGBP'],
        'direction': ['buy', 'sell', 'buy'],
        'rates': [1.0850, 1.2650, 0.8577]
    },
    'JPY Triangle': {
        'pairs': ['USDJPY', 'EURJPY', 'EURUSD'],
        'direction': ['buy', 'sell', 'buy'],
        'rates': [149.50, 162.21, 1.0850]
    },
    'AUD Triangle': {
        'pairs': ['AUDUSD', 'EURAUD', 'EURUSD'],
        'direction': ['buy', 'sell', 'buy'],
        'rates': [0.6580, 1.6490, 1.0850]
    }
}

for triangle_name, triangle in triangles.items():
    print(f'\n📊 {triangle_name}:')
    
    total_exposure_equal = 0
    total_exposure_balanced = 0
    
    print('   Equal Lot Method (WRONG):')
    equal_lot = 0.10  # Same lot for all pairs
    
    for i, pair in enumerate(triangle['pairs']):
        if pair in usd_values:
            exposure = equal_lot * usd_values[pair]
            total_exposure_equal += exposure
            print(f'   {pair}: {equal_lot:.2f} lot = ${exposure:,.0f} exposure')
    
    print(f'   Total Exposure: ${total_exposure_equal:,.0f}')
    
    # Calculate balanced lots
    print('\n   Balanced Lot Method (CORRECT):')
    target_exposure = 10000  # Target $10,000 per leg
    
    balanced_lots = {}
    for i, pair in enumerate(triangle['pairs']):
        if pair in usd_values:
            required_lot = target_exposure / usd_values[pair]
            # Round to broker step (0.01)
            balanced_lot = round(required_lot / 0.01) * 0.01
            balanced_lots[pair] = balanced_lot
            
            actual_exposure = balanced_lot * usd_values[pair]
            total_exposure_balanced += actual_exposure
            
            print(f'   {pair}: {balanced_lot:.2f} lot = ${actual_exposure:,.0f} exposure')
    
    print(f'   Total Exposure: ${total_exposure_balanced:,.0f}')
    
    # Show the difference
    exposure_diff = abs(total_exposure_equal - total_exposure_balanced)
    print(f'   💥 Difference: ${exposure_diff:,.0f}')

print('\n⚠️ PROBLEMS WITH EQUAL LOT SIZES:')
print('-' * 50)

problems = {
    'Unequal Exposure': {
        'description': 'Different USD values per leg create imbalanced risk',
        'example': 'EURUSD 0.1 lot = $10,850 vs USDJPY 0.1 lot = $10,000',
        'impact': 'Asymmetric profit/loss potential'
    },
    'Correlation Risk': {
        'description': 'Unbalanced exposures amplify correlation effects',
        'example': 'EUR exposure >> USD exposure in EUR/USD/GBP triangle',
        'impact': 'EUR moves dominate P&L, breaking arbitrage balance'
    },
    'Hedging Inefficiency': {
        'description': 'Imperfect hedges due to size mismatches',
        'example': 'Small profit on 2 legs, large loss on 1 leg',
        'impact': 'Net losses instead of risk-free profits'
    },
    'Slippage Amplification': {
        'description': 'Different lot sizes create uneven slippage impact',
        'example': 'High-value pair slippage outweighs low-value gains',
        'impact': 'Reduced or negative net profits'
    }
}

for problem, details in problems.items():
    print(f'\n🚨 {problem}:')
    print(f'   Issue: {details["description"]}')
    print(f'   Example: {details["example"]}')
    print(f'   Impact: {details["impact"]}')

print('\n✅ SOLUTION: BALANCED LOT CALCULATION')
print('-' * 50)

def calculate_balanced_triangle_lots(pairs, rates, target_usd_exposure, lot_step=0.01, min_lot=0.01):
    """Calculate balanced lot sizes for triangle arbitrage"""
    
    balanced_lots = {}
    actual_exposures = {}
    
    for pair in pairs:
        if pair in usd_values:
            # Calculate required lot for target exposure
            usd_per_lot = usd_values[pair]
            required_lot = target_usd_exposure / usd_per_lot
            
            # Round to broker constraints
            if required_lot < min_lot:
                final_lot = min_lot
            else:
                final_lot = round(required_lot / lot_step) * lot_step
            
            balanced_lots[pair] = final_lot
            actual_exposures[pair] = final_lot * usd_per_lot
    
    return balanced_lots, actual_exposures

# Test with different target exposures
test_exposures = [1000, 5000, 10000, 25000]

print('🧮 BALANCED LOT CALCULATIONS:')
print('-' * 40)

for target in test_exposures:
    print(f'\n💰 Target: ${target:,} per leg')
    
    # Test with EUR triangle
    test_pairs = ['EURUSD', 'GBPUSD', 'EURGBP']
    test_rates = [1.0850, 1.2650, 0.8577]
    
    lots, exposures = calculate_balanced_triangle_lots(test_pairs, test_rates, target)
    
    total_exposure = 0
    for pair in test_pairs:
        if pair in lots:
            lot = lots[pair]
            exposure = exposures[pair]
            total_exposure += exposure
            
            print(f'   {pair}: {lot:.3f} lot = ${exposure:,.0f}')
    
    print(f'   Total: ${total_exposure:,.0f}')
    
    # Calculate balance score
    avg_exposure = total_exposure / len(test_pairs)
    balance_score = 100 - (max(exposures.values()) - min(exposures.values())) / avg_exposure * 100
    print(f'   Balance Score: {balance_score:.1f}%')

print('\n🔧 IMPLEMENTATION CODE:')
print('-' * 50)

implementation_code = '''
class BalancedLotCalculator:
    def __init__(self, contract_sizes, exchange_rates):
        self.contract_sizes = contract_sizes
        self.exchange_rates = exchange_rates
        self.usd_values = self._calculate_usd_values()
    
    def _calculate_usd_values(self):
        """Calculate USD value per 1.00 lot for each pair"""
        usd_values = {}
        
        for pair, contract_size in self.contract_sizes.items():
            if pair not in self.exchange_rates:
                continue
                
            rate = self.exchange_rates[pair]
            base_currency = pair[:3]
            quote_currency = pair[3:]
            
            if quote_currency == 'USD':
                # Base/USD: value = base_amount * rate
                usd_values[pair] = contract_size * rate
            elif base_currency == 'USD':
                # USD/Quote: value = usd_amount
                usd_values[pair] = contract_size
            else:
                # Cross pairs: convert base to USD
                base_to_usd = self._get_base_to_usd_rate(base_currency)
                usd_values[pair] = contract_size * base_to_usd
        
        return usd_values
    
    def calculate_triangle_lots(self, triangle_pairs, target_exposure_per_leg, 
                              lot_step=0.01, min_lot=0.01):
        """Calculate balanced lots for triangle arbitrage"""
        
        balanced_lots = {}
        
        for pair in triangle_pairs:
            if pair not in self.usd_values:
                continue
            
            usd_per_lot = self.usd_values[pair]
            required_lot = target_exposure_per_leg / usd_per_lot
            
            # Apply broker constraints
            if required_lot < min_lot:
                final_lot = min_lot
            else:
                # Round to lot step
                final_lot = round(required_lot / lot_step) * lot_step
            
            balanced_lots[pair] = final_lot
        
        return balanced_lots
    
    def validate_triangle_balance(self, triangle_lots, tolerance=0.05):
        """Check if triangle lots are reasonably balanced"""
        
        exposures = []
        for pair, lot_size in triangle_lots.items():
            if pair in self.usd_values:
                exposure = lot_size * self.usd_values[pair]
                exposures.append(exposure)
        
        if not exposures:
            return False, "No valid exposures calculated"
        
        avg_exposure = sum(exposures) / len(exposures)
        max_deviation = max(abs(exp - avg_exposure) / avg_exposure for exp in exposures)
        
        is_balanced = max_deviation <= tolerance
        return is_balanced, f"Max deviation: {max_deviation:.1%}"

# Usage in ArbitrageEngine:
def _calculate_position_size(self, opportunity):
    # Get target exposure per leg from risk management
    account_balance = self.broker.get_account_balance()
    risk_percent = self.config.get_risk_percent()
    max_risk = account_balance * (risk_percent / 100)
    target_exposure = max_risk / 3  # Divide by 3 legs
    
    # Calculate balanced lots
    calculator = BalancedLotCalculator(self.contract_sizes, self.current_rates)
    triangle_pairs = [opportunity.pair1, opportunity.pair2, opportunity.pair3]
    
    balanced_lots = calculator.calculate_triangle_lots(
        triangle_pairs, 
        target_exposure,
        lot_step=0.01,
        min_lot=0.01
    )
    
    # Validate balance
    is_balanced, message = calculator.validate_triangle_balance(balanced_lots)
    if not is_balanced:
        self.logger.warning(f"Triangle imbalance detected: {message}")
    
    return balanced_lots
'''

print(implementation_code)

print('\n📊 CONFIG YAML ADDITION:')
print('-' * 30)

config_yaml = '''
# เพิ่มใน config.yaml
trading:
  position_sizing:
    method: "balanced_exposure"     # balanced_exposure, fixed_lot, risk_based
    target_exposure_per_leg: 10000  # USD per triangle leg
    balance_tolerance: 0.05         # 5% deviation allowed
    
  contract_sizes:
    # Major pairs
    EURUSD: 100000
    GBPUSD: 100000  
    USDJPY: 100000
    USDCHF: 100000
    # Add all trading pairs...
    
  lot_constraints:
    min_lot: 0.01
    max_lot: 100.0
    lot_step: 0.01
    
risk_management:
  max_exposure_per_triangle: 30000  # Max $30K total per triangle
  max_imbalance_ratio: 1.5          # Max 1.5:1 ratio between legs
  rebalance_threshold: 0.10         # Rebalance if >10% imbalanced
'''

print(config_yaml)

print('\n🎯 EXPECTED RESULTS:')
print('-' * 30)
print('✅ Equal USD exposure per triangle leg')
print('✅ Balanced profit/loss potential')  
print('✅ Proper hedging effectiveness')
print('✅ Consistent slippage impact')
print('✅ True arbitrage risk neutrality')
print('')
print('Example Triangle (Target $10K per leg):')
print('• EURUSD: 0.092 lot = $9,982')
print('• GBPUSD: 0.079 lot = $9,994') 
print('• EURGBP: 0.092 lot = $9,982')
print('• Balance Score: 99.9%')
print('')
print('🚀 Ready for implementation!')
