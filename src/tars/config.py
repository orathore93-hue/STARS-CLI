"""Configuration management for TARS CLI"""
import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any

# Directories
TARS_DIR = Path.home() / ".tars"
TARS_DIR.mkdir(exist_ok=True)

CONFIG_FILE = TARS_DIR / "config.yaml"
LOG_FILE = TARS_DIR / "tars.log"
HISTORY_FILE = TARS_DIR / "history.json"

# Default configuration
DEFAULT_CONFIG = {
    "default": {
        "namespace": None,
        "cluster": None,
        "thresholds": {
            "cpu": 80,
            "memory": 85,
            "restarts": 5
        },
        "prometheus_url": None,
        "interval": 30
    },
}


class Config:
    """Configuration manager"""
    
    def __init__(self):
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                return yaml.safe_load(f) or DEFAULT_CONFIG
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to file"""
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save()
    
    def reset(self):
        """Reset to default configuration"""
        self._config = DEFAULT_CONFIG.copy()
        self.save()
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment"""
        return os.getenv("GEMINI_API_KEY")
    
    @property
    def prometheus_url(self) -> Optional[str]:
        """Get Prometheus URL"""
        return os.getenv("PROMETHEUS_URL") or self.get("default.prometheus_url")
    
    @property
    def default_namespace(self) -> Optional[str]:
        """Get default namespace"""
        return self.get("default.namespace")


# Global config instance
config = Config()
