"""
TARS CLI - Unit Tests for Configuration Management
"""
import pytest
import yaml
import tempfile
from pathlib import Path

class TestConfigManagement:
    """Test configuration management"""
    
    def test_default_config_structure(self):
        """Test default configuration has required keys"""
        from tars import DEFAULT_CONFIG
        
        assert "default" in DEFAULT_CONFIG
        assert "thresholds" in DEFAULT_CONFIG["default"]
        assert "cpu" in DEFAULT_CONFIG["default"]["thresholds"]
        assert "memory" in DEFAULT_CONFIG["default"]["thresholds"]
        assert "restarts" in DEFAULT_CONFIG["default"]["thresholds"]
    
    def test_config_values(self):
        """Test default configuration values"""
        from tars import DEFAULT_CONFIG
        
        assert DEFAULT_CONFIG["default"]["thresholds"]["cpu"] == 80
        assert DEFAULT_CONFIG["default"]["thresholds"]["memory"] == 85
        assert DEFAULT_CONFIG["default"]["thresholds"]["restarts"] == 5


class TestCacheDecorator:
    """Test caching functionality"""
    
    def test_cache_hit(self):
        """Test cache returns cached value"""
        from tars import cached_api_call
        
        call_count = 0
        
        @cached_api_call("test", ttl=60)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "result"
        
        # First call
        result1 = test_func()
        assert result1 == "result"
        assert call_count == 1
        
        # Second call (should use cache)
        result2 = test_func()
        assert result2 == "result"
        assert call_count == 1  # Not incremented
    
    def test_cache_expiry(self):
        """Test cache expires after TTL"""
        import time
        from tars import cached_api_call, _cache, _cache_ttl
        
        # Clear cache
        _cache.clear()
        _cache_ttl.clear()
        
        call_count = 0
        
        @cached_api_call("test_expiry", ttl=1)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "result"
        
        # First call
        result1 = test_func()
        assert call_count == 1
        
        # Wait for cache to expire
        time.sleep(1.1)
        
        # Second call (cache expired)
        result2 = test_func()
        assert call_count == 2  # Incremented


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
