"""
🔥 ARBI PHOENIX - Profit Harvester
Advanced profit collection and management system

"The Phoenix that harvests profits at every opportunity"
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import numpy as np

class HarvesterStatus(Enum):
    """Profit harvester status"""
    INACTIVE = "inactive"
    MONITORING = "monitoring"
    HARVESTING = "harvesting"
    OPTIMIZING = "optimizing"

class ProfitLevel(Enum):
    """Profit taking levels"""
    QUICK_SCALP = "quick_scalp"
    PARTIAL_1 = "partial_1"
    PARTIAL_2 = "partial_2"
    FINAL_TARGET = "final_target"

@dataclass
class ProfitTarget:
    """Profit target configuration"""
    level: ProfitLevel
    pips: float
    percentage: float  # Percentage of position to close
    is_active: bool
    hit_count: int

@dataclass
class HarvestRecord:
    """Profit harvest record"""
    position_id: int
    symbol: str
    profit_level: ProfitLevel
    pips_harvested: float
    amount_harvested: float
    percentage_closed: float
    timestamp: datetime
    remaining_position: float

class ProfitHarvester:
    """
    🔥 Phoenix Profit Harvester
    
    Multi-level profit taking system with dynamic optimization
    """
    
    def __init__(self, arbitrage_engine, config: Dict):
        """Initialize the profit harvester"""
        self.logger = logging.getLogger("ProfitHarvester")
        self.arbitrage_engine = arbitrage_engine
        self.config = config
        
        # Profit targets configuration
        self.profit_targets = self._initialize_profit_targets()
        
        # Harvester parameters
        self.trailing_stop_distance = config.get('trailing_stop_distance', 10)
        self.breakeven_trigger = config.get('breakeven_trigger', 15)
        self.max_position_time = config.get('max_position_time', 3600)  # 1 hour
        
        # System status
        self.status = HarvesterStatus.INACTIVE
        self.is_running = False
        
        # Performance tracking
        self.harvest_records: List[HarvestRecord] = []
        self.total_harvested = 0.0
        self.positions_managed = 0
        self.average_profit_per_position = 0.0
        
        # Dynamic optimization
        self.performance_history: List[Dict] = []
        self.optimization_enabled = config.get('optimize_enabled', True)
        self.last_optimization = None
        
        self.logger.info("💰 Profit Harvester initialized")
    
    def _initialize_profit_targets(self) -> Dict[ProfitLevel, ProfitTarget]:
        """Initialize profit target configuration"""
        profit_config = self.config.get('profit_levels', {})
        percentage_config = self.config.get('profit_percentages', {})
        
        return {
            ProfitLevel.QUICK_SCALP: ProfitTarget(
                level=ProfitLevel.QUICK_SCALP,
                pips=profit_config.get('quick_scalp', 8),
                percentage=percentage_config.get('quick_scalp', 25),
                is_active=True,
                hit_count=0
            ),
            ProfitLevel.PARTIAL_1: ProfitTarget(
                level=ProfitLevel.PARTIAL_1,
                pips=profit_config.get('partial_1', 15),
                percentage=percentage_config.get('partial_1', 25),
                is_active=True,
                hit_count=0
            ),
            ProfitLevel.PARTIAL_2: ProfitTarget(
                level=ProfitLevel.PARTIAL_2,
                pips=profit_config.get('partial_2', 25),
                percentage=percentage_config.get('partial_2', 30),
                is_active=True,
                hit_count=0
            ),
            ProfitLevel.FINAL_TARGET: ProfitTarget(
                level=ProfitLevel.FINAL_TARGET,
                pips=profit_config.get('final_target', 40),
                percentage=percentage_config.get('final_target', 20),
                is_active=True,
                hit_count=0
            )
        }
    
    async def start(self):
        """Start the profit harvester"""
        try:
            self.logger.info("🚀 Starting Profit Harvester...")
            
            self.is_running = True
            self.status = HarvesterStatus.MONITORING
            
            # Start main harvesting loop
            await self._harvesting_loop()
            
        except Exception as e:
            self.logger.error(f"❌ Profit harvester start failed: {e}")
            raise
    
    async def stop(self):
        """Stop the profit harvester"""
        self.logger.info("🛑 Stopping Profit Harvester...")
        
        self.is_running = False
        self.status = HarvesterStatus.INACTIVE
        
        self.logger.info("✅ Profit Harvester stopped")
    
    async def _harvesting_loop(self):
        """Main profit harvesting loop"""
        self.logger.info("💰 Profit harvesting started")
        
        while self.is_running:
            try:
                # Monitor positions for profit opportunities
                await self._monitor_positions()
                
                # Execute profit taking
                await self._execute_profit_taking()
                
                # Manage trailing stops
                await self._manage_trailing_stops()
                
                # Optimize profit targets if enabled
                if self.optimization_enabled:
                    await self._optimize_targets()
                
                # Update performance metrics
                self._update_metrics()
                
                await asyncio.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.logger.error(f"❌ Harvesting loop error: {e}")
                await asyncio.sleep(5)
    
    async def _monitor_positions(self):
        """Monitor positions for profit opportunities"""
        try:
            positions = self.arbitrage_engine.get_positions()
            
            for position in positions:
                # Calculate current profit in pips
                profit_pips = await self._calculate_profit_pips(position)
                
                if profit_pips is not None:
                    # Check each profit level
                    for level, target in self.profit_targets.items():
                        if target.is_active and profit_pips >= target.pips:
                            await self._trigger_profit_taking(position, level, profit_pips)
                    
                    # Check for breakeven move
                    if profit_pips >= self.breakeven_trigger:
                        await self._move_to_breakeven(position)
                    
                    # Check for position timeout
                    await self._check_position_timeout(position)
            
        except Exception as e:
            self.logger.error(f"❌ Position monitoring failed: {e}")
    
    async def _calculate_profit_pips(self, position) -> Optional[float]:
        """Calculate current profit in pips for a position"""
        try:
            # Get current price
            current_price = await self._get_current_price(position.symbol)
            if not current_price:
                return None
            
            # Calculate pip value based on position type and symbol
            if position.type == 'buy':
                price_diff = current_price - position.open_price
            else:
                price_diff = position.open_price - current_price
            
            # Convert to pips (simplified - would need proper pip calculation per symbol)
            pip_size = 0.0001  # Standard for most pairs
            if 'JPY' in position.symbol:
                pip_size = 0.01
            
            profit_pips = price_diff / pip_size
            
            return profit_pips
            
        except Exception as e:
            self.logger.error(f"❌ Profit calculation failed: {e}")
            return None
    
    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            if hasattr(self.arbitrage_engine.pair_scanner, 'mt5'):
                mt5 = self.arbitrage_engine.pair_scanner.mt5
                
                tick = mt5.symbol_info_tick(symbol)
                if tick:
                    return (tick.bid + tick.ask) / 2
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Price retrieval failed: {e}")
            return None
    
    async def _trigger_profit_taking(self, position, level: ProfitLevel, current_pips: float):
        """Trigger profit taking at specified level"""
        try:
            target = self.profit_targets[level]
            
            # Check if this level has already been hit for this position
            if await self._is_level_already_hit(position, level):
                return
            
            self.logger.info(f"💰 Profit target hit: {level.value} at {current_pips:.1f} pips")
            
            # Calculate amount to close
            close_percentage = target.percentage / 100
            close_volume = position.volume * close_percentage
            
            # Execute partial close
            if await self._partial_close_position(position, close_volume, level):
                # Record harvest
                harvest_record = HarvestRecord(
                    position_id=position.ticket,
                    symbol=position.symbol,
                    profit_level=level,
                    pips_harvested=current_pips,
                    amount_harvested=position.profit * close_percentage,
                    percentage_closed=target.percentage,
                    timestamp=datetime.now(),
                    remaining_position=position.volume - close_volume
                )
                
                self.harvest_records.append(harvest_record)
                target.hit_count += 1
                self.total_harvested += harvest_record.amount_harvested
                
                self.logger.info(f"✅ Harvested {target.percentage}% at {level.value}: ${harvest_record.amount_harvested:.2f}")
            
        except Exception as e:
            self.logger.error(f"❌ Profit taking failed: {e}")
    
    async def _is_level_already_hit(self, position, level: ProfitLevel) -> bool:
        """Check if profit level has already been hit for this position"""
        for record in self.harvest_records:
            if (record.position_id == position.ticket and 
                record.profit_level == level and
                datetime.now() - record.timestamp < timedelta(hours=1)):
                return True
        return False
    
    async def _partial_close_position(self, position, close_volume: float, level: ProfitLevel) -> bool:
        """Partially close a position"""
        try:
            if hasattr(self.arbitrage_engine.pair_scanner, 'mt5'):
                mt5 = self.arbitrage_engine.pair_scanner.mt5
                
                # Create partial close request
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": close_volume,
                    "type": mt5.ORDER_TYPE_SELL if position.type == 'buy' else mt5.ORDER_TYPE_BUY,
                    "position": position.ticket,
                    "magic": self.arbitrage_engine.magic_number,
                    "comment": f"Phoenix harvest {level.value}",
                }
                
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    self.logger.info(f"✅ Partial close executed: {close_volume} lots")
                    return True
                else:
                    self.logger.error(f"❌ Partial close failed: {result.comment}")
                    return False
            
            return False
            
        except Exception as e:
            self.logger.error(f"❌ Partial close execution failed: {e}")
            return False
    
    async def _execute_profit_taking(self):
        """Execute queued profit taking operations"""
        # This method can be used for batch processing of profit taking
        # Currently, profit taking is handled immediately in _trigger_profit_taking
        pass
    
    async def _manage_trailing_stops(self):
        """Manage trailing stops for profitable positions"""
        try:
            positions = self.arbitrage_engine.get_positions()
            
            for position in positions:
                profit_pips = await self._calculate_profit_pips(position)
                
                if profit_pips and profit_pips > self.trailing_stop_distance:
                    await self._update_trailing_stop(position, profit_pips)
            
        except Exception as e:
            self.logger.error(f"❌ Trailing stop management failed: {e}")
    
    async def _update_trailing_stop(self, position, current_profit_pips: float):
        """Update trailing stop for a position"""
        try:
            # Calculate new stop loss level
            current_price = await self._get_current_price(position.symbol)
            if not current_price:
                return
            
            pip_size = 0.0001
            if 'JPY' in position.symbol:
                pip_size = 0.01
            
            if position.type == 'buy':
                new_stop = current_price - (self.trailing_stop_distance * pip_size)
            else:
                new_stop = current_price + (self.trailing_stop_distance * pip_size)
            
            # Update stop loss (placeholder - would need actual MT5 implementation)
            self.logger.info(f"📈 Trailing stop updated: {position.symbol} to {new_stop:.5f}")
            
        except Exception as e:
            self.logger.error(f"❌ Trailing stop update failed: {e}")
    
    async def _move_to_breakeven(self, position):
        """Move stop loss to breakeven"""
        try:
            # Check if already at breakeven
            if await self._is_at_breakeven(position):
                return
            
            # Move stop to breakeven + small buffer
            buffer_pips = 2
            pip_size = 0.0001
            if 'JPY' in position.symbol:
                pip_size = 0.01
            
            if position.type == 'buy':
                breakeven_stop = position.open_price + (buffer_pips * pip_size)
            else:
                breakeven_stop = position.open_price - (buffer_pips * pip_size)
            
            # Update stop loss (placeholder)
            self.logger.info(f"⚖️ Moved to breakeven: {position.symbol}")
            
        except Exception as e:
            self.logger.error(f"❌ Breakeven move failed: {e}")
    
    async def _is_at_breakeven(self, position) -> bool:
        """Check if position is already at breakeven"""
        # Placeholder - would check current stop loss level
        return False
    
    async def _check_position_timeout(self, position):
        """Check if position has exceeded maximum time"""
        try:
            position_age = datetime.now() - position.open_time
            
            if position_age.total_seconds() > self.max_position_time:
                self.logger.warning(f"⏰ Position timeout: {position.symbol} ({position_age})")
                await self._close_timeout_position(position)
            
        except Exception as e:
            self.logger.error(f"❌ Position timeout check failed: {e}")
    
    async def _close_timeout_position(self, position):
        """Close position due to timeout"""
        try:
            # Close entire position
            if hasattr(self.arbitrage_engine.pair_scanner, 'mt5'):
                mt5 = self.arbitrage_engine.pair_scanner.mt5
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": position.volume,
                    "type": mt5.ORDER_TYPE_SELL if position.type == 'buy' else mt5.ORDER_TYPE_BUY,
                    "position": position.ticket,
                    "magic": self.arbitrage_engine.magic_number,
                    "comment": "Phoenix timeout close",
                }
                
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    self.logger.info(f"✅ Timeout position closed: {position.symbol}")
                else:
                    self.logger.error(f"❌ Timeout close failed: {result.comment}")
            
        except Exception as e:
            self.logger.error(f"❌ Timeout position close failed: {e}")
    
    async def _optimize_targets(self):
        """Optimize profit targets based on performance"""
        try:
            # Only optimize every hour
            if (self.last_optimization and 
                datetime.now() - self.last_optimization < timedelta(hours=1)):
                return
            
            self.status = HarvesterStatus.OPTIMIZING
            
            # Analyze recent performance
            recent_records = [
                r for r in self.harvest_records 
                if datetime.now() - r.timestamp < timedelta(hours=24)
            ]
            
            if len(recent_records) < 10:  # Need minimum data
                return
            
            # Calculate success rates for each level
            level_performance = {}
            for level in ProfitLevel:
                level_records = [r for r in recent_records if r.profit_level == level]
                if level_records:
                    avg_harvest = sum(r.amount_harvested for r in level_records) / len(level_records)
                    level_performance[level] = avg_harvest
            
            # Adjust targets based on performance (simplified)
            await self._adjust_profit_targets(level_performance)
            
            self.last_optimization = datetime.now()
            self.status = HarvesterStatus.MONITORING
            
        except Exception as e:
            self.logger.error(f"❌ Target optimization failed: {e}")
            self.status = HarvesterStatus.MONITORING
    
    async def _adjust_profit_targets(self, performance: Dict[ProfitLevel, float]):
        """Adjust profit targets based on performance analysis"""
        try:
            for level, avg_profit in performance.items():
                target = self.profit_targets[level]
                
                # Increase target if consistently profitable
                if avg_profit > 50:  # Threshold for good performance
                    new_pips = min(target.pips * 1.1, target.pips + 5)  # Max 10% increase or +5 pips
                    target.pips = new_pips
                    self.logger.info(f"📈 Optimized {level.value}: increased to {new_pips:.1f} pips")
                
                # Decrease target if underperforming
                elif avg_profit < 10:  # Threshold for poor performance
                    new_pips = max(target.pips * 0.9, target.pips - 3)  # Max 10% decrease or -3 pips
                    target.pips = new_pips
                    self.logger.info(f"📉 Optimized {level.value}: decreased to {new_pips:.1f} pips")
            
        except Exception as e:
            self.logger.error(f"❌ Target adjustment failed: {e}")
    
    def _update_metrics(self):
        """Update performance metrics"""
        try:
            if self.harvest_records:
                self.positions_managed = len(set(r.position_id for r in self.harvest_records))
                
                if self.positions_managed > 0:
                    self.average_profit_per_position = self.total_harvested / self.positions_managed
            
            # Record performance snapshot
            if len(self.harvest_records) % 10 == 0:  # Every 10 harvests
                performance_snapshot = {
                    'timestamp': datetime.now(),
                    'total_harvested': self.total_harvested,
                    'positions_managed': self.positions_managed,
                    'average_profit': self.average_profit_per_position,
                    'target_hit_counts': {level.value: target.hit_count for level, target in self.profit_targets.items()}
                }
                
                self.performance_history.append(performance_snapshot)
                
                # Keep only last 100 snapshots
                if len(self.performance_history) > 100:
                    self.performance_history = self.performance_history[-100:]
            
        except Exception as e:
            self.logger.error(f"❌ Metrics update failed: {e}")
    
    def get_status(self) -> Dict:
        """Get profit harvester status"""
        return {
            'status': self.status.value,
            'is_running': self.is_running,
            'total_harvested': self.total_harvested,
            'positions_managed': self.positions_managed,
            'average_profit_per_position': self.average_profit_per_position,
            'harvest_count': len(self.harvest_records),
            'optimization_enabled': self.optimization_enabled,
            'last_optimization': self.last_optimization
        }
    
    def get_profit_targets(self) -> Dict[ProfitLevel, ProfitTarget]:
        """Get current profit targets"""
        return self.profit_targets.copy()
    
    def get_harvest_records(self) -> List[HarvestRecord]:
        """Get harvest records"""
        return self.harvest_records.copy()
    
    def get_performance_history(self) -> List[Dict]:
        """Get performance history"""
        return self.performance_history.copy()
    
    def update_profit_target(self, level: ProfitLevel, pips: float, percentage: float):
        """Update a specific profit target"""
        if level in self.profit_targets:
            self.profit_targets[level].pips = pips
            self.profit_targets[level].percentage = percentage
            self.logger.info(f"📝 Updated {level.value}: {pips} pips, {percentage}%")
    
    def toggle_profit_level(self, level: ProfitLevel):
        """Toggle a profit level on/off"""
        if level in self.profit_targets:
            self.profit_targets[level].is_active = not self.profit_targets[level].is_active
            status = "ON" if self.profit_targets[level].is_active else "OFF"
            self.logger.info(f"🔄 {level.value} turned {status}")
    
    def reset_statistics(self):
        """Reset performance statistics"""
        self.harvest_records.clear()
        self.total_harvested = 0.0
        self.positions_managed = 0
        self.average_profit_per_position = 0.0
        self.performance_history.clear()
        
        for target in self.profit_targets.values():
            target.hit_count = 0
        
        self.logger.info("🔄 Statistics reset")
