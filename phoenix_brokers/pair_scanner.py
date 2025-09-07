"""
🔍 ARBI PHOENIX - Broker Pair Scanner
Multi-broker currency pair discovery with nomenclature handling

"The Phoenix eyes that see all opportunities"
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class BrokerType(Enum):
    """Supported broker types"""
    MT5 = "MetaTrader5"
    MT4 = "MetaTrader4"
    CTRADER = "cTrader"
    IB = "InteractiveBrokers"
    OANDA = "Oanda"
    FXCM = "FXCM"
    PEPPERSTONE = "Pepperstone"
    IC_MARKETS = "IC_Markets"

@dataclass
class CurrencyPair:
    """Currency pair information"""
    symbol: str                    # Broker-specific symbol
    standard_name: str             # Standardized name (e.g., EURUSD)
    base_currency: str             # Base currency (e.g., EUR)
    quote_currency: str            # Quote currency (e.g., USD)
    spread: float                  # Current spread in pips
    min_lot: float                 # Minimum lot size
    max_lot: float                 # Maximum lot size
    lot_step: float                # Lot step size
    pip_value: float               # Pip value in account currency
    digits: int                    # Price digits
    is_tradeable: bool             # Whether pair is currently tradeable
    trading_hours: str             # Trading hours
    category: str                  # major, minor, exotic

class BrokerPairScanner:
    """
    🔍 Multi-broker currency pair scanner
    
    Discovers and normalizes currency pairs across different brokers
    """
    
    def __init__(self, broker_config: Dict):
        """Initialize the pair scanner"""
        self.logger = logging.getLogger("PairScanner")
        self.broker_config = broker_config
        self.broker_type = BrokerType(broker_config.get('api_type', 'MT5'))
        
        # Available pairs storage
        self.available_pairs: List[CurrencyPair] = []
        self.major_pairs: List[CurrencyPair] = []
        self.minor_pairs: List[CurrencyPair] = []
        self.exotic_pairs: List[CurrencyPair] = []
        
        # Nomenclature mapping
        self.nomenclature_map = self._load_nomenclature_rules()
        
        # Major currencies for classification
        self.major_currencies = {'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'NZD', 'CAD'}
        
        self.logger.info(f"🔍 Pair Scanner initialized for {self.broker_type.value}")
    
    def _load_nomenclature_rules(self) -> Dict[BrokerType, Dict]:
        """Load broker-specific nomenclature rules"""
        return {
            BrokerType.MT5: {
                'suffix_patterns': ['', '.raw', '.a', '.b', '.c'],
                'prefix_patterns': ['', 'FX:', 'FOREX:'],
                'separator': '',
                'case': 'upper'
            },
            BrokerType.MT4: {
                'suffix_patterns': ['', '.raw', '.a', '.b'],
                'prefix_patterns': [''],
                'separator': '',
                'case': 'upper'
            },
            BrokerType.CTRADER: {
                'suffix_patterns': ['', '.raw', '.a'],
                'prefix_patterns': [''],
                'separator': '',
                'case': 'upper'
            },
            BrokerType.IB: {
                'suffix_patterns': [''],
                'prefix_patterns': [''],
                'separator': '.',
                'case': 'upper'
            },
            BrokerType.OANDA: {
                'suffix_patterns': [''],
                'prefix_patterns': [''],
                'separator': '_',
                'case': 'upper'
            },
            BrokerType.FXCM: {
                'suffix_patterns': [''],
                'prefix_patterns': [''],
                'separator': '/',
                'case': 'upper'
            }
        }
    
    async def initialize(self):
        """Initialize broker connection and scan pairs"""
        try:
            self.logger.info("🚀 Initializing broker connection...")
            
            # Initialize broker-specific connection
            await self._initialize_broker_connection()
            
            # Scan available pairs
            await self.scan_all_pairs()
            
            self.logger.info(f"✅ Scanner initialized with {len(self.available_pairs)} pairs")
            
        except Exception as e:
            self.logger.error(f"❌ Scanner initialization failed: {e}")
            raise
    
    async def _initialize_broker_connection(self):
        """Initialize connection to specific broker"""
        if self.broker_type == BrokerType.MT5:
            await self._initialize_mt5()
        elif self.broker_type == BrokerType.IB:
            await self._initialize_ib()
        elif self.broker_type == BrokerType.OANDA:
            await self._initialize_oanda()
        else:
            raise NotImplementedError(f"Broker {self.broker_type} not yet implemented")
    
    async def _initialize_mt5(self):
        """Initialize MetaTrader 5 connection"""
        try:
            import MetaTrader5 as mt5
            
            # Initialize MT5
            if not mt5.initialize():
                raise Exception("MT5 initialization failed")
            
            # Login to account
            login = self.broker_config.get('login')
            password = self.broker_config.get('password')
            server = self.broker_config.get('server')
            
            if login and password and server:
                if not mt5.login(int(login), password, server):
                    raise Exception(f"MT5 login failed: {mt5.last_error()}")
            
            self.mt5 = mt5
            self.logger.info("✅ MT5 connection established")
            
        except ImportError:
            raise Exception("MetaTrader5 package not installed")
        except Exception as e:
            raise Exception(f"MT5 connection failed: {e}")
    
    async def _initialize_ib(self):
        """Initialize Interactive Brokers connection"""
        # Placeholder for IB implementation
        self.logger.info("📝 IB connection - Implementation pending")
        pass
    
    async def _initialize_oanda(self):
        """Initialize Oanda connection"""
        # Placeholder for Oanda implementation
        self.logger.info("📝 Oanda connection - Implementation pending")
        pass
    
    async def scan_all_pairs(self):
        """Scan all available currency pairs"""
        try:
            self.logger.info("🔍 Scanning available currency pairs...")
            
            if self.broker_type == BrokerType.MT5:
                await self._scan_mt5_pairs()
            elif self.broker_type == BrokerType.IB:
                await self._scan_ib_pairs()
            elif self.broker_type == BrokerType.OANDA:
                await self._scan_oanda_pairs()
            
            # Categorize pairs
            self._categorize_pairs()
            
            # Log results
            self._log_scan_results()
            
        except Exception as e:
            self.logger.error(f"❌ Pair scanning failed: {e}")
            raise
    
    async def _scan_mt5_pairs(self):
        """Scan MT5 currency pairs"""
        try:
            # Get all symbols
            symbols = self.mt5.symbols_get()
            
            if symbols is None:
                raise Exception("Failed to get MT5 symbols")
            
            for symbol_info in symbols:
                symbol = symbol_info.name
                
                # Check if it's a forex pair
                if self._is_forex_pair(symbol):
                    pair_info = await self._get_mt5_pair_info(symbol_info)
                    if pair_info:
                        self.available_pairs.append(pair_info)
            
            self.logger.info(f"📊 Found {len(self.available_pairs)} forex pairs in MT5")
            
        except Exception as e:
            self.logger.error(f"❌ MT5 pair scanning failed: {e}")
            raise
    
    async def _get_mt5_pair_info(self, symbol_info) -> Optional[CurrencyPair]:
        """Extract pair information from MT5 symbol info"""
        try:
            symbol = symbol_info.name
            
            # Normalize symbol name
            standard_name = self._normalize_symbol_name(symbol)
            if not standard_name:
                return None
            
            # Extract base and quote currencies
            base_currency = standard_name[:3]
            quote_currency = standard_name[3:6]
            
            # Get current spread
            spread = self._calculate_spread(symbol_info)
            
            # Create pair object
            pair = CurrencyPair(
                symbol=symbol,
                standard_name=standard_name,
                base_currency=base_currency,
                quote_currency=quote_currency,
                spread=spread,
                min_lot=symbol_info.volume_min,
                max_lot=symbol_info.volume_max,
                lot_step=symbol_info.volume_step,
                pip_value=symbol_info.trade_tick_value,
                digits=symbol_info.digits,
                is_tradeable=symbol_info.visible and symbol_info.select,
                trading_hours=self._get_trading_hours(symbol_info),
                category=self._classify_pair(base_currency, quote_currency)
            )
            
            return pair
            
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to process symbol {symbol_info.name}: {e}")
            return None
    
    def _is_forex_pair(self, symbol: str) -> bool:
        """Check if symbol is a forex pair"""
        # Remove common suffixes and prefixes
        clean_symbol = self._clean_symbol_name(symbol)
        
        # Check if it's 6 characters (EURUSD format)
        if len(clean_symbol) == 6:
            # Check if both parts are valid currencies
            base = clean_symbol[:3]
            quote = clean_symbol[3:6]
            return self._is_valid_currency(base) and self._is_valid_currency(quote)
        
        return False
    
    def _clean_symbol_name(self, symbol: str) -> str:
        """Clean symbol name by removing prefixes and suffixes"""
        clean_symbol = symbol.upper()
        
        # Remove common prefixes
        prefixes = ['FX:', 'FOREX:', 'CURRENCY:']
        for prefix in prefixes:
            if clean_symbol.startswith(prefix):
                clean_symbol = clean_symbol[len(prefix):]
        
        # Remove common suffixes
        suffixes = ['.RAW', '.A', '.B', '.C', '.ECN', '.STP']
        for suffix in suffixes:
            if clean_symbol.endswith(suffix):
                clean_symbol = clean_symbol[:-len(suffix)]
        
        # Remove separators
        clean_symbol = clean_symbol.replace('/', '').replace('_', '').replace('.', '')
        
        return clean_symbol
    
    def _normalize_symbol_name(self, symbol: str) -> Optional[str]:
        """Normalize symbol to standard format (EURUSD)"""
        clean_symbol = self._clean_symbol_name(symbol)
        
        if len(clean_symbol) == 6:
            base = clean_symbol[:3]
            quote = clean_symbol[3:6]
            
            if self._is_valid_currency(base) and self._is_valid_currency(quote):
                return f"{base}{quote}"
        
        return None
    
    def _is_valid_currency(self, currency: str) -> bool:
        """Check if currency code is valid"""
        valid_currencies = {
            'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'NZD', 'CAD',  # Majors
            'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'TRY',         # Minors
            'ZAR', 'MXN', 'SGD', 'HKD', 'THB', 'KRW', 'BRL', 'CNY',  # Exotics
            'INR', 'RUB', 'ILS', 'AED', 'SAR', 'QAR', 'KWD'          # More exotics
        }
        return currency in valid_currencies
    
    def _calculate_spread(self, symbol_info) -> float:
        """Calculate current spread in pips"""
        try:
            # Get current tick
            tick = self.mt5.symbol_info_tick(symbol_info.name)
            if tick is None:
                return 0.0
            
            # Calculate spread
            spread_points = tick.ask - tick.bid
            
            # Convert to pips
            if symbol_info.digits == 5 or symbol_info.digits == 3:
                # 5-digit or 3-digit broker
                spread_pips = spread_points / (10 ** (symbol_info.digits - 1))
            else:
                # 4-digit or 2-digit broker
                spread_pips = spread_points / (10 ** symbol_info.digits)
            
            return round(spread_pips, 1)
            
        except Exception:
            return 0.0
    
    def _get_trading_hours(self, symbol_info) -> str:
        """Get trading hours for the symbol"""
        # Simplified - most forex pairs trade 24/5
        return "24/5"
    
    def _classify_pair(self, base: str, quote: str) -> str:
        """Classify pair as major, minor, or exotic"""
        if base in self.major_currencies and quote in self.major_currencies:
            if 'USD' in [base, quote]:
                return 'major'
            else:
                return 'minor'
        else:
            return 'exotic'
    
    def _categorize_pairs(self):
        """Categorize pairs into major, minor, and exotic"""
        self.major_pairs = [p for p in self.available_pairs if p.category == 'major']
        self.minor_pairs = [p for p in self.available_pairs if p.category == 'minor']
        self.exotic_pairs = [p for p in self.available_pairs if p.category == 'exotic']
    
    def _log_scan_results(self):
        """Log scanning results"""
        self.logger.info("📊 Pair Scanning Results:")
        self.logger.info(f"   🟢 Major pairs: {len(self.major_pairs)}")
        self.logger.info(f"   🟡 Minor pairs: {len(self.minor_pairs)}")
        self.logger.info(f"   🟠 Exotic pairs: {len(self.exotic_pairs)}")
        self.logger.info(f"   📈 Total pairs: {len(self.available_pairs)}")
        
        # Log some examples
        if self.major_pairs:
            major_examples = [p.standard_name for p in self.major_pairs[:5]]
            self.logger.info(f"   Major examples: {', '.join(major_examples)}")
        
        if self.minor_pairs:
            minor_examples = [p.standard_name for p in self.minor_pairs[:5]]
            self.logger.info(f"   Minor examples: {', '.join(minor_examples)}")
    
    async def _scan_ib_pairs(self):
        """Scan Interactive Brokers pairs - Placeholder"""
        self.logger.info("📝 IB pair scanning - Implementation pending")
        pass
    
    async def _scan_oanda_pairs(self):
        """Scan Oanda pairs - Placeholder"""
        self.logger.info("📝 Oanda pair scanning - Implementation pending")
        pass
    
    def get_pairs_by_category(self, category: str) -> List[CurrencyPair]:
        """Get pairs by category"""
        if category.lower() == 'major':
            return self.major_pairs
        elif category.lower() == 'minor':
            return self.minor_pairs
        elif category.lower() == 'exotic':
            return self.exotic_pairs
        else:
            return self.available_pairs
    
    def get_pair_by_symbol(self, symbol: str) -> Optional[CurrencyPair]:
        """Get pair information by symbol"""
        for pair in self.available_pairs:
            if pair.symbol == symbol or pair.standard_name == symbol:
                return pair
        return None
    
    def get_pairs_with_currency(self, currency: str) -> List[CurrencyPair]:
        """Get all pairs containing a specific currency"""
        return [
            pair for pair in self.available_pairs
            if currency.upper() in [pair.base_currency, pair.quote_currency]
        ]
    
    def get_tradeable_pairs(self) -> List[CurrencyPair]:
        """Get all currently tradeable pairs"""
        return [pair for pair in self.available_pairs if pair.is_tradeable]
    
    async def refresh_spreads(self):
        """Refresh current spreads for all pairs"""
        if self.broker_type == BrokerType.MT5:
            for pair in self.available_pairs:
                try:
                    symbol_info = self.mt5.symbol_info(pair.symbol)
                    if symbol_info:
                        pair.spread = self._calculate_spread(symbol_info)
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to refresh spread for {pair.symbol}: {e}")
    
    def get_statistics(self) -> Dict:
        """Get scanner statistics"""
        return {
            'total_pairs': len(self.available_pairs),
            'major_pairs': len(self.major_pairs),
            'minor_pairs': len(self.minor_pairs),
            'exotic_pairs': len(self.exotic_pairs),
            'tradeable_pairs': len(self.get_tradeable_pairs()),
            'average_spread': sum(p.spread for p in self.available_pairs) / len(self.available_pairs) if self.available_pairs else 0,
            'broker_type': self.broker_type.value
        }
