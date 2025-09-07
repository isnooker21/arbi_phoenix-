"""
🔥 ARBI PHOENIX - Brokers Package
Broker integration modules for the Phoenix system
"""

from .pair_scanner import BrokerPairScanner, BrokerType, CurrencyPair

try:
    from .order_executor import (
        BrokerOrderExecutor, OrderRequest, OrderResult, 
        FillMode, OrderType, OrderStatus
    )
    __all__ = [
        'BrokerPairScanner', 'BrokerType', 'CurrencyPair',
        'BrokerOrderExecutor', 'OrderRequest', 'OrderResult',
        'FillMode', 'OrderType', 'OrderStatus'
    ]
except ImportError:
    __all__ = ['BrokerPairScanner', 'BrokerType', 'CurrencyPair']
