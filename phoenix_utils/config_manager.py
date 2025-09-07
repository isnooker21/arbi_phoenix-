"""
🔥 ARBI PHOENIX - Configuration Manager
Centralized configuration management for the Phoenix system

"The Phoenix configuration that adapts and evolves"
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    """
    🔥 Phoenix Configuration Manager
    
    Manages all system configurations with hot-reload capability
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.logger = logging.getLogger("ConfigManager")
        self._config_data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            if not self.config_path.exists():
                self.logger.warning(f"⚠️ Config file not found: {self.config_path}")
                self._create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config_data = yaml.safe_load(file) or {}
            
            self.logger.info(f"✅ Configuration loaded from {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load config: {e}")
            self._config_data = self._get_default_config()
    
    def _create_default_config(self):
        """Create default configuration file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            default_config = self._get_default_config()
            
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(default_config, file, default_flow_style=False, indent=2)
            
            self.logger.info(f"📝 Created default config at {self.config_path}")
            self._config_data = default_config
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create default config: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'broker': {
                'name': 'IC_Markets',
                'api_type': 'MT5',
                'server': 'ICMarkets-Demo',
                'login': 'your_login_here',
                'password': 'your_password_here',
                'timeout': 30,
                'retries': 3,
                'auto_connect': True,
                'reconnect_interval': 60
            },
            'trading': {
                'min_arbitrage_profit': 5,
                'max_spread_cost': 8,
                'min_liquidity': 1.0,
                'base_lot_size': 0.01,
                'max_position_risk': 2.0,
                'max_total_exposure': 20.0,
                'auto_start': False,
                'profit_levels': {
                    'quick_scalp': 8,
                    'partial_1': 15,
                    'partial_2': 25,
                    'final_target': 40
                }
            },
            'recovery': {
                'max_recovery_layers': 6,
                'recovery_multiplier': 1.5,
                'strong_correlation': 0.8,
                'medium_correlation': 0.6,
                'weak_correlation': 0.4,
                'recovery_delay': 30,
                'max_recovery_time': 14400
            },
            'gui': {
                'window_title': '🔥 Arbi Phoenix Dashboard',
                'window_width': 1400,
                'window_height': 900,
                'portfolio_update': 1000,
                'triangle_update': 500,
                'recovery_update': 2000,
                'theme': 'dark'
            },
            'logging': {
                'level': 'INFO',
                'file_path': 'data/logs/phoenix.log',
                'max_file_size': '10MB',
                'backup_count': 5
            },
            'risk_management': {
                'max_daily_loss': 10.0,
                'max_drawdown': 20.0,
                'volatility_circuit': 95,
                'correlation_circuit': 0.2,
                'max_positions_per_pair': 3,
                'max_total_positions': 50
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Configuration key path (e.g., 'broker.name')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            keys = key_path.split('.')
            value = self._config_data
            
            for key in keys:
                value = value[key]
            
            return value
            
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Configuration key path
            value: Value to set
        """
        try:
            keys = key_path.split('.')
            config = self._config_data
            
            # Navigate to parent
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # Set value
            config[keys[-1]] = value
            
            self.logger.info(f"📝 Config updated: {key_path} = {value}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to set config {key_path}: {e}")
    
    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(self._config_data, file, default_flow_style=False, indent=2)
            
            self.logger.info(f"💾 Configuration saved to {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save config: {e}")
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
        self.logger.info("🔄 Configuration reloaded")
    
    @property
    def broker_config(self) -> Dict[str, Any]:
        """Get broker configuration"""
        return self.get('broker', {})
    
    @property
    def trading_config(self) -> Dict[str, Any]:
        """Get trading configuration"""
        return self.get('trading', {})
    
    @property
    def recovery_config(self) -> Dict[str, Any]:
        """Get recovery configuration"""
        return self.get('recovery', {})
    
    @property
    def gui_config(self) -> Dict[str, Any]:
        """Get GUI configuration"""
        return self.get('gui', {})
    
    @property
    def profit_config(self) -> Dict[str, Any]:
        """Get profit configuration"""
        return self.get('trading.profit_levels', {})
    
    @property
    def risk_config(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        return self.get('risk_management', {})
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self._config_data.copy()
    
    def is_auto_connect_enabled(self) -> bool:
        """Check if auto-connect is enabled"""
        return self.get('broker.auto_connect', True)
    
    def is_auto_start_enabled(self) -> bool:
        """Check if auto-start trading is enabled"""
        return self.get('trading.auto_start', False)
    
    def update_broker_credentials(self, login: str, password: str, server: str):
        """Update broker credentials"""
        self.set('broker.login', login)
        self.set('broker.password', password)
        self.set('broker.server', server)
        self.save()
        
        self.logger.info("🔐 Broker credentials updated")
    
    def toggle_auto_start(self) -> bool:
        """Toggle auto-start trading"""
        current = self.is_auto_start_enabled()
        self.set('trading.auto_start', not current)
        self.save()
        
        new_state = not current
        self.logger.info(f"🔄 Auto-start trading: {'ON' if new_state else 'OFF'}")
        return new_state
