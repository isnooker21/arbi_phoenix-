"""
🔥 ARBI PHOENIX - Order Executor
Universal order execution system supporting multiple brokers and fill modes

"The Phoenix executor that adapts to every broker"
"""

import asyncio
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import time

class FillMode(Enum):
    """Order fill modes"""
    IOC = "IOC"                    # Immediate or Cancel
    FOK = "FOK"                    # Fill or Kill  
    GTC = "GTC"                    # Good Till Cancelled
    DAY = "DAY"                    # Day order
    MARKET = "MARKET"              # Market execution
    INSTANT = "INSTANT"            # Instant execution
    REQUEST = "REQUEST"            # Request execution

class OrderType(Enum):
    """Order types"""
    MARKET_BUY = "market_buy"
    MARKET_SELL = "market_sell"
    LIMIT_BUY = "limit_buy"
    LIMIT_SELL = "limit_sell"
    STOP_BUY = "stop_buy"
    STOP_SELL = "stop_sell"

class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    FILLED = "filled"
    PARTIAL = "partial"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

@dataclass
class OrderRequest:
    """Universal order request"""
    symbol: str
    order_type: OrderType
    volume: float
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    fill_mode: FillMode = FillMode.MARKET
    magic_number: Optional[int] = None
    comment: str = "Phoenix Order"
    expiration: Optional[datetime] = None
    deviation: int = 10  # Price deviation in points

@dataclass
class OrderResult:
    """Universal order result"""
    success: bool
    order_id: Optional[int] = None
    ticket: Optional[int] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_volume: float = 0.0
    filled_price: Optional[float] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    slippage: float = 0.0
    commission: float = 0.0
    swap: float = 0.0

class BrokerOrderExecutor:
    """
    🔥 Universal Order Executor
    
    Supports multiple brokers with different fill modes and execution types
    """
    
    def __init__(self, broker_type: str, broker_config: Dict):
        """Initialize the order executor"""
        self.logger = logging.getLogger("OrderExecutor")
        self.broker_type = broker_type.upper()
        self.broker_config = broker_config
        
        # Execution parameters
        self.default_fill_mode = FillMode(broker_config.get('default_fill_mode', 'MARKET'))
        self.max_deviation = broker_config.get('max_deviation', 10)
        self.execution_timeout = broker_config.get('execution_timeout', 5.0)
        self.retry_attempts = broker_config.get('retry_attempts', 3)
        self.retry_delay = broker_config.get('retry_delay', 0.1)
        
        # Broker-specific settings
        self.broker_settings = self._load_broker_settings()
        
        # Connection reference
        self.connection = None
        
        self.logger.info(f"🎯 Order Executor initialized for {self.broker_type}")
    
    def _load_broker_settings(self) -> Dict:
        """Load broker-specific execution settings"""
        settings = {
            'MT5': {
                'supported_fill_modes': [FillMode.MARKET, FillMode.IOC, FillMode.FOK],
                'market_execution': True,
                'instant_execution': True,
                'request_execution': True,
                'max_deviation': 50,
                'min_volume': 0.01,
                'volume_step': 0.01
            },
            'MT4': {
                'supported_fill_modes': [FillMode.MARKET, FillMode.INSTANT],
                'market_execution': False,
                'instant_execution': True,
                'request_execution': True,
                'max_deviation': 30,
                'min_volume': 0.01,
                'volume_step': 0.01
            },
            'CTRADER': {
                'supported_fill_modes': [FillMode.MARKET, FillMode.IOC, FillMode.FOK, FillMode.GTC],
                'market_execution': True,
                'instant_execution': True,
                'request_execution': False,
                'max_deviation': 100,
                'min_volume': 0.01,
                'volume_step': 0.01
            },
            'IB': {
                'supported_fill_modes': [FillMode.IOC, FillMode.FOK, FillMode.GTC, FillMode.DAY],
                'market_execution': True,
                'instant_execution': False,
                'request_execution': False,
                'max_deviation': 0,
                'min_volume': 1,
                'volume_step': 1
            },
            'OANDA': {
                'supported_fill_modes': [FillMode.IOC, FillMode.FOK, FillMode.GTC],
                'market_execution': True,
                'instant_execution': True,
                'request_execution': False,
                'max_deviation': 50,
                'min_volume': 1,
                'volume_step': 1
            },
            'FXCM': {
                'supported_fill_modes': [FillMode.MARKET, FillMode.IOC, FillMode.GTC],
                'market_execution': True,
                'instant_execution': False,
                'request_execution': False,
                'max_deviation': 20,
                'min_volume': 1000,
                'volume_step': 1000
            }
        }
        
        return settings.get(self.broker_type, settings['MT5'])
    
    def set_connection(self, connection):
        """Set broker connection reference"""
        self.connection = connection
        self.logger.info(f"🔗 Connection set for {self.broker_type}")
    
    async def execute_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute order with broker-specific handling"""
        start_time = time.time()
        
        try:
            self.logger.info(f"🎯 Executing {order_request.order_type.value} order: {order_request.symbol} {order_request.volume}")
            
            # Validate order request
            if not self._validate_order_request(order_request):
                return OrderResult(
                    success=False,
                    status=OrderStatus.REJECTED,
                    error_message="Order validation failed"
                )
            
            # Adjust fill mode if not supported
            adjusted_fill_mode = self._adjust_fill_mode(order_request.fill_mode)
            if adjusted_fill_mode != order_request.fill_mode:
                self.logger.info(f"🔄 Adjusted fill mode: {order_request.fill_mode.value} → {adjusted_fill_mode.value}")
                order_request.fill_mode = adjusted_fill_mode
            
            # Execute with retry mechanism
            for attempt in range(self.retry_attempts):
                try:
                    result = await self._execute_broker_order(order_request)
                    
                    if result.success:
                        execution_time = time.time() - start_time
                        result.execution_time = execution_time
                        self.logger.info(f"✅ Order executed successfully in {execution_time:.3f}s")
                        return result
                    
                    if attempt < self.retry_attempts - 1:
                        self.logger.warning(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                        await asyncio.sleep(self.retry_delay)
                    
                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        self.logger.warning(f"⚠️ Attempt {attempt + 1} error: {e}, retrying...")
                        await asyncio.sleep(self.retry_delay)
                    else:
                        raise
            
            return OrderResult(
                success=False,
                status=OrderStatus.REJECTED,
                error_message="All retry attempts failed"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"❌ Order execution failed: {e}")
            return OrderResult(
                success=False,
                status=OrderStatus.REJECTED,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def _validate_order_request(self, order_request: OrderRequest) -> bool:
        """Validate order request"""
        try:
            # Check volume
            min_volume = self.broker_settings['min_volume']
            volume_step = self.broker_settings['volume_step']
            
            if order_request.volume < min_volume:
                self.logger.error(f"❌ Volume too small: {order_request.volume} < {min_volume}")
                return False
            
            # Check volume step
            if (order_request.volume % volume_step) != 0:
                self.logger.error(f"❌ Invalid volume step: {order_request.volume} not divisible by {volume_step}")
                return False
            
            # Check fill mode support
            if order_request.fill_mode not in self.broker_settings['supported_fill_modes']:
                self.logger.warning(f"⚠️ Fill mode {order_request.fill_mode.value} not supported")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Order validation error: {e}")
            return False
    
    def _adjust_fill_mode(self, requested_fill_mode: FillMode) -> FillMode:
        """Adjust fill mode to broker capabilities"""
        supported_modes = self.broker_settings['supported_fill_modes']
        
        if requested_fill_mode in supported_modes:
            return requested_fill_mode
        
        # Fallback mapping
        fallback_map = {
            FillMode.IOC: [FillMode.MARKET, FillMode.INSTANT],
            FillMode.FOK: [FillMode.IOC, FillMode.MARKET],
            FillMode.MARKET: [FillMode.INSTANT, FillMode.IOC],
            FillMode.INSTANT: [FillMode.MARKET, FillMode.IOC],
            FillMode.GTC: [FillMode.DAY, FillMode.MARKET],
            FillMode.DAY: [FillMode.GTC, FillMode.MARKET],
            FillMode.REQUEST: [FillMode.INSTANT, FillMode.MARKET]
        }
        
        for fallback in fallback_map.get(requested_fill_mode, []):
            if fallback in supported_modes:
                return fallback
        
        # Default to first supported mode
        return supported_modes[0] if supported_modes else FillMode.MARKET
    
    async def _execute_broker_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute order for specific broker"""
        if self.broker_type == 'MT5':
            return await self._execute_mt5_order(order_request)
        elif self.broker_type == 'MT4':
            return await self._execute_mt4_order(order_request)
        elif self.broker_type == 'CTRADER':
            return await self._execute_ctrader_order(order_request)
        elif self.broker_type == 'IB':
            return await self._execute_ib_order(order_request)
        elif self.broker_type == 'OANDA':
            return await self._execute_oanda_order(order_request)
        elif self.broker_type == 'FXCM':
            return await self._execute_fxcm_order(order_request)
        else:
            raise NotImplementedError(f"Broker {self.broker_type} not implemented")
    
    async def _execute_mt5_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute MT5 order with proper fill mode"""
        try:
            if not self.connection:
                raise Exception("MT5 connection not available")
            
            mt5 = self.connection
            
            # Map order types
            order_type_map = {
                OrderType.MARKET_BUY: mt5.ORDER_TYPE_BUY,
                OrderType.MARKET_SELL: mt5.ORDER_TYPE_SELL,
                OrderType.LIMIT_BUY: mt5.ORDER_TYPE_BUY_LIMIT,
                OrderType.LIMIT_SELL: mt5.ORDER_TYPE_SELL_LIMIT,
                OrderType.STOP_BUY: mt5.ORDER_TYPE_BUY_STOP,
                OrderType.STOP_SELL: mt5.ORDER_TYPE_SELL_STOP
            }
            
            # Map fill modes
            fill_type_map = {
                FillMode.MARKET: mt5.ORDER_FILLING_RETURN,
                FillMode.IOC: mt5.ORDER_FILLING_IOC,
                FillMode.FOK: mt5.ORDER_FILLING_FOK
            }
            
            # Create request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": order_request.symbol,
                "volume": order_request.volume,
                "type": order_type_map[order_request.order_type],
                "deviation": order_request.deviation,
                "magic": order_request.magic_number or 0,
                "comment": order_request.comment,
                "type_filling": fill_type_map.get(order_request.fill_mode, mt5.ORDER_FILLING_RETURN)
            }
            
            # Add price for limit/stop orders
            if order_request.price is not None:
                request["price"] = order_request.price
            
            # Add SL/TP
            if order_request.stop_loss:
                request["sl"] = order_request.stop_loss
            if order_request.take_profit:
                request["tp"] = order_request.take_profit
            
            # Execute order
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                return OrderResult(
                    success=True,
                    order_id=result.order,
                    ticket=result.deal,
                    status=OrderStatus.FILLED,
                    filled_volume=result.volume,
                    filled_price=result.price,
                    commission=result.commission,
                    swap=result.swap
                )
            else:
                return OrderResult(
                    success=False,
                    status=OrderStatus.REJECTED,
                    error_code=result.retcode,
                    error_message=result.comment
                )
                
        except Exception as e:
            return OrderResult(
                success=False,
                status=OrderStatus.REJECTED,
                error_message=str(e)
            )
    
    async def _execute_mt4_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute MT4 order (placeholder)"""
        self.logger.info("📝 MT4 order execution - Implementation pending")
        return OrderResult(success=False, error_message="MT4 not implemented")
    
    async def _execute_ctrader_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute cTrader order (placeholder)"""
        self.logger.info("📝 cTrader order execution - Implementation pending")
        return OrderResult(success=False, error_message="cTrader not implemented")
    
    async def _execute_ib_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute Interactive Brokers order (placeholder)"""
        self.logger.info("📝 IB order execution - Implementation pending")
        return OrderResult(success=False, error_message="IB not implemented")
    
    async def _execute_oanda_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute Oanda order (placeholder)"""
        self.logger.info("📝 Oanda order execution - Implementation pending")
        return OrderResult(success=False, error_message="Oanda not implemented")
    
    async def _execute_fxcm_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute FXCM order (placeholder)"""
        self.logger.info("📝 FXCM order execution - Implementation pending")
        return OrderResult(success=False, error_message="FXCM not implemented")
    
    async def execute_triangle_arbitrage(self, 
                                       pair1: str, pair2: str, pair3: str,
                                       volumes: List[float],
                                       directions: List[str],
                                       fill_mode: FillMode = FillMode.IOC) -> List[OrderResult]:
        """Execute triangular arbitrage with simultaneous orders"""
        self.logger.info(f"🎯 Executing triangle arbitrage: {pair1}-{pair2}-{pair3}")
        
        # Create order requests
        orders = []
        for i, (pair, volume, direction) in enumerate(zip([pair1, pair2, pair3], volumes, directions)):
            order_type = OrderType.MARKET_BUY if direction == 'buy' else OrderType.MARKET_SELL
            
            orders.append(OrderRequest(
                symbol=pair,
                order_type=order_type,
                volume=volume,
                fill_mode=fill_mode,
                comment=f"Phoenix Triangle {i+1}/3"
            ))
        
        # Execute all orders simultaneously
        tasks = [self.execute_order(order) for order in orders]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        order_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                order_results.append(OrderResult(
                    success=False,
                    status=OrderStatus.REJECTED,
                    error_message=str(result)
                ))
            else:
                order_results.append(result)
        
        # Log summary
        successful_orders = sum(1 for r in order_results if r.success)
        self.logger.info(f"📊 Triangle execution: {successful_orders}/3 orders successful")
        
        return order_results
    
    def get_supported_fill_modes(self) -> List[FillMode]:
        """Get supported fill modes for current broker"""
        return self.broker_settings['supported_fill_modes']
    
    def get_broker_capabilities(self) -> Dict:
        """Get broker execution capabilities"""
        return {
            'broker_type': self.broker_type,
            'supported_fill_modes': [mode.value for mode in self.broker_settings['supported_fill_modes']],
            'market_execution': self.broker_settings['market_execution'],
            'instant_execution': self.broker_settings['instant_execution'],
            'request_execution': self.broker_settings['request_execution'],
            'max_deviation': self.broker_settings['max_deviation'],
            'min_volume': self.broker_settings['min_volume'],
            'volume_step': self.broker_settings['volume_step']
        }
