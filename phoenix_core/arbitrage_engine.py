"""
🔥 ARBI PHOENIX - Arbitrage Engine
Advanced triangular arbitrage detection and execution system

"The Phoenix engine that never sleeps"
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from enum import Enum

# Import order executor and balanced lot calculator
try:
    from phoenix_brokers.order_executor import BrokerOrderExecutor, OrderRequest, OrderType, FillMode
except ImportError:
    # Fallback if order_executor not available
    BrokerOrderExecutor = None
    OrderRequest = None
    OrderType = None
    FillMode = None

try:
    from phoenix_core.balanced_lot_calculator import BalancedLotCalculator, BalanceMethod, DEFAULT_CONTRACT_SIZES
except ImportError:
    # Fallback if balanced_lot_calculator not available
    BalancedLotCalculator = None
    BalanceMethod = None
    DEFAULT_CONTRACT_SIZES = None

class EngineStatus(Enum):
    """Engine status states"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class TriangleOpportunity:
    """Triangular arbitrage opportunity"""
    pair1: str          # First pair (e.g., EURUSD)
    pair2: str          # Second pair (e.g., GBPUSD)
    pair3: str          # Third pair (e.g., EURGBP)
    direction: str      # 'forward' or 'reverse'
    profit_pips: float  # Expected profit in pips
    profit_percent: float  # Expected profit percentage
    spread_cost: float  # Total spread cost
    net_profit: float   # Net profit after spreads
    confidence: float   # Opportunity confidence (0-1)
    timestamp: datetime # When opportunity was detected
    is_executable: bool # Whether opportunity is tradeable

@dataclass
class Position:
    """Trading position information"""
    ticket: int
    symbol: str
    type: str           # 'buy' or 'sell'
    volume: float
    open_price: float
    current_price: float
    profit: float
    swap: float
    commission: float
    open_time: datetime
    magic_number: int

class ArbitrageEngine:
    """
    🔥 Advanced Triangular Arbitrage Engine
    
    Detects and executes triangular arbitrage opportunities
    """
    
    def __init__(self, pair_scanner, config: Dict):
        """Initialize the arbitrage engine"""
        self.logger = logging.getLogger("ArbitrageEngine")
        self.pair_scanner = pair_scanner
        self.config = config
        
        # Engine status
        self.status = EngineStatus.STOPPED
        self.is_running = False
        self.start_time = None
        
        # Trading parameters
        self.min_profit = config.get('min_arbitrage_profit', 5)
        self.max_spread_cost = config.get('max_spread_cost', 8)
        self.base_lot_size = config.get('base_lot_size', 0.01)
        self.max_risk = config.get('max_position_risk', 2.0)
        
        # Opportunity tracking
        self.opportunities: List[TriangleOpportunity] = []
        self.active_positions: List[Position] = []
        self.executed_triangles = 0
        self.total_profit = 0.0
        
        # Performance metrics
        self.opportunities_found = 0
        self.opportunities_executed = 0
        self.success_rate = 0.0
        
        # Magic number for position identification
        self.magic_number = 20241201
        
        # Order executor
        self.order_executor = None
        if BrokerOrderExecutor:
            try:
                broker_type = pair_scanner.broker_type.value if hasattr(pair_scanner, 'broker_type') else 'MT5'
                self.order_executor = BrokerOrderExecutor(broker_type, pair_scanner.broker_config)
                self.logger.info(f"🎯 Order Executor initialized for {broker_type}")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not initialize Order Executor: {e}")
        
        # Balanced lot calculator
        self.lot_calculator = None
        if BalancedLotCalculator and DEFAULT_CONTRACT_SIZES:
            try:
                # Initialize with default contract sizes
                self.lot_calculator = BalancedLotCalculator(
                    contract_sizes=config.get('contract_sizes', DEFAULT_CONTRACT_SIZES),
                    exchange_rates={}  # Will be updated with real-time rates
                )
                self.logger.info("📊 Balanced Lot Calculator initialized")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not initialize Balanced Lot Calculator: {e}")
        
        self.logger.info("🔥 Arbitrage Engine initialized")
    
    async def start(self):
        """Start the arbitrage engine"""
        try:
            self.logger.info("🚀 Starting Arbitrage Engine...")
            
            if not self.pair_scanner.is_connected:
                raise Exception("Broker not connected - cannot start engine")
            
            self.status = EngineStatus.STARTING
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start main scanning loop
            await self._main_loop()
            
        except Exception as e:
            self.logger.error(f"❌ Engine start failed: {e}")
            self.status = EngineStatus.ERROR
            raise
    
    async def stop(self):
        """Stop the arbitrage engine"""
        self.logger.info("🛑 Stopping Arbitrage Engine...")
        
        self.is_running = False
        self.status = EngineStatus.STOPPED
        
        # Close any open positions
        await self._close_all_positions()
        
        self.logger.info("✅ Arbitrage Engine stopped")
    
    async def pause(self):
        """Pause the engine"""
        self.logger.info("⏸️ Pausing Arbitrage Engine...")
        self.status = EngineStatus.PAUSED
    
    async def resume(self):
        """Resume the engine"""
        self.logger.info("▶️ Resuming Arbitrage Engine...")
        self.status = EngineStatus.RUNNING
    
    async def _main_loop(self):
        """Main arbitrage scanning loop"""
        self.status = EngineStatus.RUNNING
        self.logger.info("🔍 Arbitrage scanning started")
        
        while self.is_running:
            try:
                if self.status == EngineStatus.RUNNING:
                    # Scan for opportunities
                    await self._scan_opportunities()
                    
                    # Execute profitable opportunities
                    await self._execute_opportunities()
                    
                    # Monitor existing positions
                    await self._monitor_positions()
                
                # Update performance metrics
                self._update_metrics()
                
                # Small delay to prevent excessive CPU usage
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"❌ Main loop error: {e}")
                await asyncio.sleep(1)
    
    async def _scan_opportunities(self):
        """Scan for triangular arbitrage opportunities"""
        try:
            # Get tradeable pairs
            pairs = self.pair_scanner.get_tradeable_pairs()
            major_pairs = [p for p in pairs if p.category == 'major']
            
            # Find triangular combinations
            triangles = self._find_triangular_combinations(major_pairs)
            
            # Analyze each triangle for opportunities
            new_opportunities = []
            for triangle in triangles:
                opportunity = await self._analyze_triangle(triangle)
                if opportunity and opportunity.is_executable:
                    new_opportunities.append(opportunity)
            
            # Update opportunities list
            self.opportunities = new_opportunities
            self.opportunities_found += len(new_opportunities)
            
            if new_opportunities:
                self.logger.info(f"🎯 Found {len(new_opportunities)} arbitrage opportunities")
            
        except Exception as e:
            self.logger.error(f"❌ Opportunity scanning failed: {e}")
    
    def _find_triangular_combinations(self, pairs) -> List[Tuple[str, str, str]]:
        """Find valid triangular combinations from available pairs"""
        triangles = []
        
        # Extract unique currencies
        currencies = set()
        pair_dict = {}
        
        for pair in pairs:
            base = pair.base_currency
            quote = pair.quote_currency
            currencies.add(base)
            currencies.add(quote)
            pair_dict[f"{base}{quote}"] = pair
            pair_dict[f"{quote}{base}"] = pair  # Reverse pair
        
        # Find triangular combinations
        for curr1 in currencies:
            for curr2 in currencies:
                for curr3 in currencies:
                    if curr1 != curr2 and curr2 != curr3 and curr1 != curr3:
                        # Check if all three pairs exist
                        pair1 = f"{curr1}{curr2}"
                        pair2 = f"{curr2}{curr3}"
                        pair3 = f"{curr3}{curr1}"
                        
                        if (pair1 in pair_dict and 
                            pair2 in pair_dict and 
                            pair3 in pair_dict):
                            triangles.append((pair1, pair2, pair3))
        
        return triangles
    
    async def _analyze_triangle(self, triangle: Tuple[str, str, str]) -> Optional[TriangleOpportunity]:
        """Analyze a triangular combination for arbitrage opportunity"""
        try:
            pair1, pair2, pair3 = triangle
            
            # Get current prices (simplified - would need real-time data)
            prices = await self._get_triangle_prices(pair1, pair2, pair3)
            if not prices:
                return None
            
            price1, price2, price3 = prices
            
            # Calculate forward arbitrage
            forward_result = price1 * price2 * price3
            forward_profit = (forward_result - 1.0) * 10000  # Convert to pips
            
            # Calculate reverse arbitrage
            reverse_result = 1.0 / (price1 * price2 * price3)
            reverse_profit = (reverse_result - 1.0) * 10000  # Convert to pips
            
            # Choose best direction
            if abs(forward_profit) > abs(reverse_profit):
                profit_pips = forward_profit
                direction = 'forward'
            else:
                profit_pips = reverse_profit
                direction = 'reverse'
            
            # Calculate spread costs
            spread_cost = await self._calculate_spread_cost(pair1, pair2, pair3)
            net_profit = profit_pips - spread_cost
            
            # Check if opportunity is profitable
            is_executable = (net_profit > self.min_profit and 
                           spread_cost < self.max_spread_cost)
            
            # Calculate confidence based on profit margin
            confidence = min(1.0, max(0.0, net_profit / (self.min_profit * 2)))
            
            return TriangleOpportunity(
                pair1=pair1,
                pair2=pair2,
                pair3=pair3,
                direction=direction,
                profit_pips=profit_pips,
                profit_percent=profit_pips / 10000,
                spread_cost=spread_cost,
                net_profit=net_profit,
                confidence=confidence,
                timestamp=datetime.now(),
                is_executable=is_executable
            )
            
        except Exception as e:
            self.logger.error(f"❌ Triangle analysis failed: {e}")
            return None
    
    async def _get_triangle_prices(self, pair1: str, pair2: str, pair3: str) -> Optional[Tuple[float, float, float]]:
        """Get current prices for triangle pairs"""
        try:
            # This is a simplified version - in reality, you'd get real-time prices
            # from the broker API
            
            if hasattr(self.pair_scanner, 'mt5'):
                mt5 = self.pair_scanner.mt5
                
                # Get symbol info for each pair
                symbol1 = self._get_broker_symbol(pair1)
                symbol2 = self._get_broker_symbol(pair2)
                symbol3 = self._get_broker_symbol(pair3)
                
                if not all([symbol1, symbol2, symbol3]):
                    return None
                
                # Get current ticks
                tick1 = mt5.symbol_info_tick(symbol1)
                tick2 = mt5.symbol_info_tick(symbol2)
                tick3 = mt5.symbol_info_tick(symbol3)
                
                if not all([tick1, tick2, tick3]):
                    return None
                
                # Use mid prices
                price1 = (tick1.bid + tick1.ask) / 2
                price2 = (tick2.bid + tick2.ask) / 2
                price3 = (tick3.bid + tick3.ask) / 2
                
                return (price1, price2, price3)
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get triangle prices: {e}")
            return None
    
    def _get_broker_symbol(self, standard_pair: str) -> Optional[str]:
        """Convert standard pair name to broker-specific symbol"""
        pair_info = self.pair_scanner.get_pair_by_symbol(standard_pair)
        return pair_info.symbol if pair_info else None
    
    async def _calculate_spread_cost(self, pair1: str, pair2: str, pair3: str) -> float:
        """Calculate total spread cost for triangle execution"""
        try:
            total_spread = 0.0
            
            for pair in [pair1, pair2, pair3]:
                pair_info = self.pair_scanner.get_pair_by_symbol(pair)
                if pair_info:
                    total_spread += pair_info.spread
            
            return total_spread
            
        except Exception as e:
            self.logger.error(f"❌ Spread calculation failed: {e}")
            return 999.0  # High value to prevent execution
    
    async def _execute_opportunities(self):
        """Execute profitable arbitrage opportunities"""
        try:
            executable_opportunities = [
                opp for opp in self.opportunities 
                if opp.is_executable and opp.net_profit > self.min_profit
            ]
            
            # Sort by profitability
            executable_opportunities.sort(key=lambda x: x.net_profit, reverse=True)
            
            # Execute top opportunities (limit concurrent executions)
            max_concurrent = 3
            for i, opportunity in enumerate(executable_opportunities[:max_concurrent]):
                if await self._execute_triangle(opportunity):
                    self.opportunities_executed += 1
                    self.logger.info(f"✅ Executed triangle: {opportunity.net_profit:.1f} pips profit")
            
        except Exception as e:
            self.logger.error(f"❌ Opportunity execution failed: {e}")
    
    async def _execute_triangle(self, opportunity: TriangleOpportunity) -> bool:
        """Execute a triangular arbitrage opportunity"""
        try:
            self.logger.info(f"🎯 Executing triangle: {opportunity.pair1}-{opportunity.pair2}-{opportunity.pair3}")
            
            # Calculate position sizes (now returns dict of pair -> lot_size)
            lot_sizes = self._calculate_position_size(opportunity)
            
            # Execute trades in sequence
            if opportunity.direction == 'forward':
                success = await self._execute_forward_triangle(opportunity, lot_sizes)
            else:
                success = await self._execute_reverse_triangle(opportunity, lot_sizes)
            
            if success:
                self.executed_triangles += 1
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Triangle execution failed: {e}")
            return False
    
    def _calculate_position_size(self, opportunity: TriangleOpportunity) -> Dict[str, float]:
        """Calculate appropriate position sizes based on balanced exposure"""
        
        # Try balanced lot calculation first
        if self.lot_calculator:
            try:
                # Update calculator with current exchange rates
                current_rates = self._get_current_exchange_rates()
                if current_rates:
                    self.lot_calculator.update_rates(current_rates)
                
                # Get position sizing config
                position_config = self.config.get('position_sizing', {})
                target_exposure = position_config.get('target_exposure_per_leg', 10000)
                lot_constraints = self.config.get('lot_constraints', {})
                
                # Calculate balanced lots for triangle
                triangle_pairs = [opportunity.pair1, opportunity.pair2, opportunity.pair3]
                balanced_lots = self.lot_calculator.calculate_triangle_lots(
                    triangle_pairs=triangle_pairs,
                    target_exposure_per_leg=target_exposure,
                    lot_step=lot_constraints.get('lot_step', 0.01),
                    min_lot=lot_constraints.get('min_lot', 0.01),
                    max_lot=lot_constraints.get('max_lot', 100.0),
                    method=BalanceMethod.EQUAL_EXPOSURE
                )
                
                # Validate triangle balance
                is_balanced, message = self.lot_calculator.validate_triangle_balance(
                    balanced_lots, 
                    tolerance=position_config.get('balance_tolerance', 0.05)
                )
                
                if not is_balanced:
                    self.logger.warning(f"⚠️ Triangle imbalance: {message}")
                
                # Get exposure summary
                summary = self.lot_calculator.get_triangle_exposure_summary(balanced_lots)
                self.logger.info(
                    f"📊 Balanced lots: Total=${summary['total_exposure']:,.0f}, "
                    f"Balance={summary['balance_score']:.1f}%"
                )
                
                return balanced_lots
                
            except Exception as e:
                self.logger.error(f"❌ Balanced lot calculation failed: {e}")
        
        # Fallback to simple equal lot sizing
        self.logger.info("📊 Using fallback equal lot sizing")
        return {
            opportunity.pair1: self.base_lot_size,
            opportunity.pair2: self.base_lot_size,
            opportunity.pair3: self.base_lot_size
        }
    
    def _get_current_exchange_rates(self) -> Optional[Dict[str, float]]:
        """Get current exchange rates for lot calculation"""
        try:
            if not hasattr(self.pair_scanner, 'mt5'):
                return None
            
            mt5 = self.pair_scanner.mt5
            rates = {}
            
            # Get rates for major pairs used in calculations
            major_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD']
            
            for pair in major_pairs:
                try:
                    symbol = self._get_broker_symbol(pair)
                    if symbol:
                        tick = mt5.symbol_info_tick(symbol)
                        if tick:
                            rates[pair] = (tick.bid + tick.ask) / 2
                except Exception:
                    continue
            
            return rates if rates else None
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get exchange rates: {e}")
            return None
    
    async def _execute_forward_triangle(self, opportunity: TriangleOpportunity, lot_sizes: Dict[str, float]) -> bool:
        """Execute forward triangle (buy-buy-sell sequence)"""
        if not self.order_executor or not OrderRequest:
            # Fallback to old method
            total_lots = sum(lot_sizes.values())
            self.logger.info(f"📈 Forward triangle execution (legacy): {total_lots:.3f} total lots")
            return True
        
        try:
            # Set connection reference
            if hasattr(self.pair_scanner, 'mt5'):
                self.order_executor.set_connection(self.pair_scanner.mt5)
            
            # Execute triangle with IOC fill mode for speed
            fill_mode = FillMode.IOC if FillMode else None
            
            # Extract lot sizes in order
            volumes = [
                lot_sizes.get(opportunity.pair1, 0.01),
                lot_sizes.get(opportunity.pair2, 0.01),
                lot_sizes.get(opportunity.pair3, 0.01)
            ]
            
            results = await self.order_executor.execute_triangle_arbitrage(
                pair1=opportunity.pair1,
                pair2=opportunity.pair2, 
                pair3=opportunity.pair3,
                volumes=volumes,
                directions=['buy', 'buy', 'sell'],
                fill_mode=fill_mode
            )
            
            # Check if all orders succeeded
            successful_orders = sum(1 for r in results if r.success)
            success_rate = successful_orders / len(results) if results else 0
            
            # Log detailed results
            for i, (pair, volume) in enumerate(zip([opportunity.pair1, opportunity.pair2, opportunity.pair3], volumes)):
                if i < len(results):
                    status = "✅" if results[i].success else "❌"
                    self.logger.info(f"  {status} {pair}: {volume:.3f} lot")
            
            self.logger.info(f"📈 Forward triangle: {successful_orders}/3 orders successful ({success_rate:.1%})")
            
            return success_rate >= 0.67  # At least 2/3 orders must succeed
            
        except Exception as e:
            self.logger.error(f"❌ Forward triangle execution failed: {e}")
            return False
    
    async def _execute_reverse_triangle(self, opportunity: TriangleOpportunity, lot_sizes: Dict[str, float]) -> bool:
        """Execute reverse triangle (sell-sell-buy sequence)"""
        if not self.order_executor or not OrderRequest:
            # Fallback to old method
            total_lots = sum(lot_sizes.values())
            self.logger.info(f"📉 Reverse triangle execution (legacy): {total_lots:.3f} total lots")
            return True
        
        try:
            # Set connection reference
            if hasattr(self.pair_scanner, 'mt5'):
                self.order_executor.set_connection(self.pair_scanner.mt5)
            
            # Execute triangle with IOC fill mode for speed
            fill_mode = FillMode.IOC if FillMode else None
            
            # Extract lot sizes in order
            volumes = [
                lot_sizes.get(opportunity.pair1, 0.01),
                lot_sizes.get(opportunity.pair2, 0.01),
                lot_sizes.get(opportunity.pair3, 0.01)
            ]
            
            results = await self.order_executor.execute_triangle_arbitrage(
                pair1=opportunity.pair1,
                pair2=opportunity.pair2,
                pair3=opportunity.pair3,
                volumes=volumes,
                directions=['sell', 'sell', 'buy'],
                fill_mode=fill_mode
            )
            
            # Check if all orders succeeded
            successful_orders = sum(1 for r in results if r.success)
            success_rate = successful_orders / len(results) if results else 0
            
            # Log detailed results
            for i, (pair, volume) in enumerate(zip([opportunity.pair1, opportunity.pair2, opportunity.pair3], volumes)):
                if i < len(results):
                    status = "✅" if results[i].success else "❌"
                    self.logger.info(f"  {status} {pair}: {volume:.3f} lot")
            
            self.logger.info(f"📉 Reverse triangle: {successful_orders}/3 orders successful ({success_rate:.1%})")
            
            return success_rate >= 0.67  # At least 2/3 orders must succeed
            
        except Exception as e:
            self.logger.error(f"❌ Reverse triangle execution failed: {e}")
            return False
    
    async def _monitor_positions(self):
        """Monitor existing positions and manage them"""
        try:
            # Update position information
            await self._update_positions()
            
            # Check for profit targets and stop losses
            for position in self.active_positions:
                await self._check_position_exit(position)
            
        except Exception as e:
            self.logger.error(f"❌ Position monitoring failed: {e}")
    
    async def _update_positions(self):
        """Update current position information"""
        try:
            if hasattr(self.pair_scanner, 'mt5'):
                mt5 = self.pair_scanner.mt5
                
                # Get positions with our magic number
                positions = mt5.positions_get()
                if positions is not None:
                    self.active_positions = [
                        Position(
                            ticket=pos.ticket,
                            symbol=pos.symbol,
                            type='buy' if pos.type == 0 else 'sell',
                            volume=pos.volume,
                            open_price=pos.price_open,
                            current_price=pos.price_current,
                            profit=pos.profit,
                            swap=pos.swap,
                            commission=pos.commission,
                            open_time=datetime.fromtimestamp(pos.time),
                            magic_number=pos.magic
                        )
                        for pos in positions
                        if pos.magic == self.magic_number
                    ]
            
        except Exception as e:
            self.logger.error(f"❌ Position update failed: {e}")
    
    async def _check_position_exit(self, position: Position):
        """Check if position should be closed"""
        # Simplified exit logic - in reality, you'd have:
        # - Multiple profit levels
        # - Trailing stops
        # - Time-based exits
        # - Correlation-based exits
        
        profit_pips = position.profit / position.volume / 10  # Simplified calculation
        
        if profit_pips > 20:  # Take profit at 20 pips
            await self._close_position(position)
        elif profit_pips < -10:  # Stop loss at -10 pips
            await self._close_position(position)
    
    async def _close_position(self, position: Position):
        """Close a specific position"""
        try:
            if hasattr(self.pair_scanner, 'mt5'):
                mt5 = self.pair_scanner.mt5
                
                # Create close request
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": position.volume,
                    "type": mt5.ORDER_TYPE_SELL if position.type == 'buy' else mt5.ORDER_TYPE_BUY,
                    "position": position.ticket,
                    "magic": self.magic_number,
                    "comment": "Phoenix close",
                }
                
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    self.logger.info(f"✅ Position closed: {position.ticket}")
                    self.total_profit += position.profit
                else:
                    self.logger.error(f"❌ Failed to close position: {result.comment}")
            
        except Exception as e:
            self.logger.error(f"❌ Position close failed: {e}")
    
    async def _close_all_positions(self):
        """Close all open positions"""
        self.logger.info("🔄 Closing all positions...")
        
        for position in self.active_positions:
            await self._close_position(position)
    
    async def emergency_close_all(self):
        """Emergency close all positions"""
        self.logger.warning("🚨 EMERGENCY CLOSE ALL POSITIONS!")
        await self._close_all_positions()
    
    def _update_metrics(self):
        """Update performance metrics"""
        if self.opportunities_found > 0:
            self.success_rate = (self.opportunities_executed / self.opportunities_found) * 100
    
    def get_status(self) -> Dict:
        """Get current engine status"""
        return {
            'status': self.status.value,
            'is_running': self.is_running,
            'start_time': self.start_time,
            'opportunities_found': self.opportunities_found,
            'opportunities_executed': self.opportunities_executed,
            'success_rate': self.success_rate,
            'active_positions': len(self.active_positions),
            'total_profit': self.total_profit,
            'executed_triangles': self.executed_triangles
        }
    
    def get_opportunities(self) -> List[TriangleOpportunity]:
        """Get current opportunities"""
        return self.opportunities.copy()
    
    def get_positions(self) -> List[Position]:
        """Get active positions"""
        return self.active_positions.copy()
    
    def get_order_executor_info(self) -> Dict:
        """Get order executor information"""
        if not self.order_executor:
            return {
                'available': False,
                'broker_type': 'Unknown',
                'supported_fill_modes': [],
                'capabilities': {}
            }
        
        try:
            return {
                'available': True,
                'broker_type': self.order_executor.broker_type,
                'supported_fill_modes': [mode.value for mode in self.order_executor.get_supported_fill_modes()],
                'capabilities': self.order_executor.get_broker_capabilities()
            }
        except Exception as e:
            return {
                'available': False,
                'error': str(e),
                'broker_type': getattr(self.order_executor, 'broker_type', 'Unknown')
            }
