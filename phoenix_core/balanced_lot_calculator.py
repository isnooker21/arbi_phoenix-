#!/usr/bin/env python3
"""
🔥 Balanced Lot Calculator for Triangular Arbitrage
Calculates lot sizes based on equal USD exposure per leg
"""

import math
from typing import Dict, Tuple, List, Optional
from enum import Enum

class BalanceMethod(Enum):
    """Methods for balancing triangle lot sizes"""
    EQUAL_EXPOSURE = "equal_exposure"      # Equal USD exposure per leg
    RISK_ADJUSTED = "risk_adjusted"        # Adjust based on volatility
    CORRELATION_WEIGHTED = "correlation_weighted"  # Weight by correlation

class BalancedLotCalculator:
    """Calculate balanced lot sizes for triangular arbitrage"""
    
    def __init__(self, contract_sizes: Dict[str, int], exchange_rates: Dict[str, float]):
        """
        Initialize calculator with contract sizes and current rates
        
        Args:
            contract_sizes: Dict of pair -> contract size (e.g., {'EURUSD': 100000})
            exchange_rates: Dict of pair -> current rate (e.g., {'EURUSD': 1.0850})
        """
        self.contract_sizes = contract_sizes
        self.exchange_rates = exchange_rates
        self.usd_values = self._calculate_usd_values()
        
    def _calculate_usd_values(self) -> Dict[str, float]:
        """Calculate USD value per 1.00 lot for each currency pair"""
        usd_values = {}
        
        for pair, contract_size in self.contract_sizes.items():
            if pair not in self.exchange_rates:
                continue
                
            rate = self.exchange_rates[pair]
            base_currency = pair[:3]
            quote_currency = pair[3:]
            
            if quote_currency == 'USD':
                # Base/USD pairs: value = base_amount * rate
                usd_values[pair] = contract_size * rate
                
            elif base_currency == 'USD':
                # USD/Quote pairs: value = usd_amount (contract size is in USD)
                usd_values[pair] = contract_size
                
            else:
                # Cross pairs: need to convert base currency to USD
                base_to_usd_rate = self._get_base_to_usd_rate(base_currency)
                if base_to_usd_rate:
                    usd_values[pair] = contract_size * base_to_usd_rate
                else:
                    # Fallback: assume standard contract size
                    usd_values[pair] = 100000
        
        return usd_values
    
    def _get_base_to_usd_rate(self, base_currency: str) -> Optional[float]:
        """Get exchange rate from base currency to USD"""
        
        # Try direct Base/USD pair
        base_usd_pair = base_currency + 'USD'
        if base_usd_pair in self.exchange_rates:
            return self.exchange_rates[base_usd_pair]
        
        # Try inverted USD/Base pair
        usd_base_pair = 'USD' + base_currency
        if usd_base_pair in self.exchange_rates:
            return 1.0 / self.exchange_rates[usd_base_pair]
        
        # Try cross calculation through EUR
        if base_currency != 'EUR':
            eur_base_pair = 'EUR' + base_currency
            eur_usd_pair = 'EURUSD'
            
            if eur_base_pair in self.exchange_rates and eur_usd_pair in self.exchange_rates:
                eur_to_base = self.exchange_rates[eur_base_pair]
                eur_to_usd = self.exchange_rates[eur_usd_pair]
                return eur_to_usd / eur_to_base
        
        return None
    
    def calculate_triangle_lots(self, 
                              triangle_pairs: List[str], 
                              target_exposure_per_leg: float,
                              lot_step: float = 0.01, 
                              min_lot: float = 0.01,
                              max_lot: float = 100.0,
                              method: BalanceMethod = BalanceMethod.EQUAL_EXPOSURE) -> Dict[str, float]:
        """
        Calculate balanced lot sizes for triangle arbitrage
        
        Args:
            triangle_pairs: List of 3 currency pairs in triangle
            target_exposure_per_leg: Target USD exposure per triangle leg
            lot_step: Broker lot step (e.g., 0.01)
            min_lot: Minimum lot size
            max_lot: Maximum lot size
            method: Balancing method to use
            
        Returns:
            Dict of pair -> calculated lot size
        """
        
        if method == BalanceMethod.EQUAL_EXPOSURE:
            return self._calculate_equal_exposure_lots(
                triangle_pairs, target_exposure_per_leg, lot_step, min_lot, max_lot
            )
        elif method == BalanceMethod.RISK_ADJUSTED:
            return self._calculate_risk_adjusted_lots(
                triangle_pairs, target_exposure_per_leg, lot_step, min_lot, max_lot
            )
        else:
            # Fallback to equal exposure
            return self._calculate_equal_exposure_lots(
                triangle_pairs, target_exposure_per_leg, lot_step, min_lot, max_lot
            )
    
    def _calculate_equal_exposure_lots(self, 
                                     triangle_pairs: List[str], 
                                     target_exposure: float,
                                     lot_step: float, 
                                     min_lot: float, 
                                     max_lot: float) -> Dict[str, float]:
        """Calculate lots for equal USD exposure per leg"""
        
        balanced_lots = {}
        
        for pair in triangle_pairs:
            if pair not in self.usd_values:
                # Fallback: use minimum lot if pair not found
                balanced_lots[pair] = min_lot
                continue
            
            usd_per_lot = self.usd_values[pair]
            required_lot = target_exposure / usd_per_lot
            
            # Apply broker constraints
            if required_lot < min_lot:
                final_lot = min_lot
            elif required_lot > max_lot:
                final_lot = max_lot
            else:
                # Round to lot step (nearest)
                final_lot = round(required_lot / lot_step) * lot_step
                final_lot = max(final_lot, min_lot)  # Ensure not below minimum
            
            balanced_lots[pair] = final_lot
        
        return balanced_lots
    
    def _calculate_risk_adjusted_lots(self, 
                                    triangle_pairs: List[str], 
                                    target_exposure: float,
                                    lot_step: float, 
                                    min_lot: float, 
                                    max_lot: float) -> Dict[str, float]:
        """Calculate lots adjusted for volatility/risk (future enhancement)"""
        
        # For now, use equal exposure as base
        base_lots = self._calculate_equal_exposure_lots(
            triangle_pairs, target_exposure, lot_step, min_lot, max_lot
        )
        
        # TODO: Implement volatility adjustments
        # - Reduce lot size for high volatility pairs
        # - Increase lot size for low volatility pairs
        # - Maintain overall triangle balance
        
        return base_lots
    
    def validate_triangle_balance(self, 
                                triangle_lots: Dict[str, float], 
                                tolerance: float = 0.05) -> Tuple[bool, str]:
        """
        Check if triangle lots are reasonably balanced
        
        Args:
            triangle_lots: Dict of pair -> lot size
            tolerance: Maximum allowed deviation from average (e.g., 0.05 = 5%)
            
        Returns:
            Tuple of (is_balanced, message)
        """
        
        exposures = []
        exposure_details = {}
        
        for pair, lot_size in triangle_lots.items():
            if pair in self.usd_values:
                exposure = lot_size * self.usd_values[pair]
                exposures.append(exposure)
                exposure_details[pair] = exposure
        
        if not exposures:
            return False, "No valid exposures calculated"
        
        if len(exposures) < 3:
            return False, f"Only {len(exposures)} valid exposures (need 3 for triangle)"
        
        # Calculate balance metrics
        avg_exposure = sum(exposures) / len(exposures)
        min_exposure = min(exposures)
        max_exposure = max(exposures)
        
        max_deviation = max(abs(exp - avg_exposure) / avg_exposure for exp in exposures)
        
        is_balanced = max_deviation <= tolerance
        
        # Create detailed message
        message = f"Avg: ${avg_exposure:,.0f}, Range: ${min_exposure:,.0f}-${max_exposure:,.0f}, Max deviation: {max_deviation:.1%}"
        
        return is_balanced, message
    
    def get_triangle_exposure_summary(self, triangle_lots: Dict[str, float]) -> Dict[str, any]:
        """Get detailed exposure summary for triangle"""
        
        exposures = {}
        total_exposure = 0
        
        for pair, lot_size in triangle_lots.items():
            if pair in self.usd_values:
                exposure = lot_size * self.usd_values[pair]
                exposures[pair] = {
                    'lot_size': lot_size,
                    'usd_per_lot': self.usd_values[pair],
                    'total_exposure': exposure
                }
                total_exposure += exposure
        
        # Calculate balance score
        if exposures:
            exposure_values = [exp['total_exposure'] for exp in exposures.values()]
            avg_exposure = sum(exposure_values) / len(exposure_values)
            max_deviation = max(abs(exp - avg_exposure) / avg_exposure for exp in exposure_values)
            balance_score = (1.0 - max_deviation) * 100
        else:
            balance_score = 0
        
        return {
            'exposures': exposures,
            'total_exposure': total_exposure,
            'avg_exposure': total_exposure / len(exposures) if exposures else 0,
            'balance_score': balance_score
        }
    
    def update_rates(self, new_rates: Dict[str, float]) -> None:
        """Update exchange rates and recalculate USD values"""
        self.exchange_rates.update(new_rates)
        self.usd_values = self._calculate_usd_values()
    
    def get_usd_value_per_lot(self, pair: str) -> Optional[float]:
        """Get USD value per 1.00 lot for specific pair"""
        return self.usd_values.get(pair)


# Default contract sizes for major currency pairs
DEFAULT_CONTRACT_SIZES = {
    # Major USD pairs
    'EURUSD': 100000,
    'GBPUSD': 100000,
    'AUDUSD': 100000,
    'NZDUSD': 100000,
    'USDCAD': 100000,
    'USDCHF': 100000,
    'USDJPY': 100000,
    'USDSGD': 100000,
    'USDHKD': 100000,
    'USDNOK': 100000,
    'USDSEK': 100000,
    'USDDKK': 100000,
    'USDPLN': 100000,
    'USDZAR': 100000,
    'USDMXN': 100000,
    
    # EUR cross pairs
    'EURJPY': 100000,
    'EURGBP': 100000,
    'EURAUD': 100000,
    'EURNZD': 100000,
    'EURCAD': 100000,
    'EURCHF': 100000,
    'EURSGD': 100000,
    'EURNOK': 100000,
    'EURSEK': 100000,
    'EURDKK': 100000,
    'EURPLN': 100000,
    'EURZAR': 100000,
    
    # GBP cross pairs
    'GBPJPY': 100000,
    'GBPAUD': 100000,
    'GBPNZD': 100000,
    'GBPCAD': 100000,
    'GBPCHF': 100000,
    'GBPSGD': 100000,
    'GBPNOK': 100000,
    'GBPSEK': 100000,
    'GBPDKK': 100000,
    'GBPPLN': 100000,
    'GBPZAR': 100000,
    
    # Other major cross pairs
    'AUDJPY': 100000,
    'AUDCAD': 100000,
    'AUDCHF': 100000,
    'AUDNZD': 100000,
    'AUDSGD': 100000,
    'NZDJPY': 100000,
    'NZDCAD': 100000,
    'NZDCHF': 100000,
    'NZDSGD': 100000,
    'CADJPY': 100000,
    'CADCHF': 100000,
    'CADSGD': 100000,
    'CHFJPY': 100000,
    'CHFSGD': 100000,
    'SGDJPY': 100000,
}


if __name__ == "__main__":
    # Test the calculator
    sample_rates = {
        'EURUSD': 1.0850,
        'GBPUSD': 1.2650,
        'EURGBP': 0.8577,
        'USDJPY': 149.50,
        'EURJPY': 162.21,
        'GBPJPY': 189.12,
    }
    
    calculator = BalancedLotCalculator(DEFAULT_CONTRACT_SIZES, sample_rates)
    
    # Test EUR triangle
    triangle_pairs = ['EURUSD', 'GBPUSD', 'EURGBP']
    target_exposure = 10000  # $10K per leg
    
    lots = calculator.calculate_triangle_lots(triangle_pairs, target_exposure)
    
    print("🔥 Balanced Lot Calculator Test")
    print("=" * 40)
    print(f"Target exposure: ${target_exposure:,} per leg")
    print()
    
    for pair, lot_size in lots.items():
        usd_value = calculator.get_usd_value_per_lot(pair)
        exposure = lot_size * usd_value
        print(f"{pair}: {lot_size:.3f} lot = ${exposure:,.0f} exposure")
    
    # Validate balance
    is_balanced, message = calculator.validate_triangle_balance(lots)
    print(f"\nBalance check: {'✅ BALANCED' if is_balanced else '❌ IMBALANCED'}")
    print(f"Details: {message}")
    
    # Get summary
    summary = calculator.get_triangle_exposure_summary(lots)
    print(f"Balance score: {summary['balance_score']:.1f}%")
