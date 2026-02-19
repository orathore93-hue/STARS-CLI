"""Unit tests for configuration module"""
import pytest
from pathlib import Path
from tars.config import Config, DEFAULT_CONFIG


class TestConfig:
    def test_default_config(self):
        config = Config()
        assert config.get("default.thresholds.cpu") == 80
        assert config.get("default.thresholds.memory") == 85
    
    def test_get_nested_value(self):
        config = Config()
        assert config.get("default.thresholds.cpu") == 80
        assert config.get("nonexistent.key", "default") == "default"
    
    def test_set_value(self):
        config = Config()
        config.set("default.namespace", "production")
        assert config.get("default.namespace") == "production"
    
    def test_reset(self):
        config = Config()
        config.set("default.namespace", "test")
        config.reset()
        assert config.get("default.namespace") is None
