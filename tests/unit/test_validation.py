"""
TARS CLI - Unit Tests for Validation Functions
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Mock console to avoid output during tests
class MockConsole:
    def print(self, *args, **kwargs):
        pass

# Import after mocking
import tars
tars.console = MockConsole()

from tars import validate_k8s_name, validate_namespace, validate_threshold, sanitize_command


class TestValidateK8sName:
    """Test Kubernetes name validation"""
    
    def test_valid_names(self):
        """Test valid Kubernetes names"""
        assert validate_k8s_name("my-pod", "pod") == True
        assert validate_k8s_name("nginx-deployment", "deployment") == True
        assert validate_k8s_name("app-123", "app") == True
        assert validate_k8s_name("a", "resource") == True
    
    def test_invalid_names(self):
        """Test invalid Kubernetes names"""
        assert validate_k8s_name("", "pod") == False
        assert validate_k8s_name("UPPERCASE", "pod") == False
        assert validate_k8s_name("has_underscore", "pod") == False
        assert validate_k8s_name("-starts-with-dash", "pod") == False
        assert validate_k8s_name("ends-with-dash-", "pod") == False
        assert validate_k8s_name("a" * 254, "pod") == False  # Too long


class TestValidateNamespace:
    """Test namespace validation"""
    
    def test_valid_namespaces(self):
        """Test valid namespace names"""
        assert validate_namespace("default") == True
        assert validate_namespace("kube-system") == True
        assert validate_namespace("production") == True
    
    def test_invalid_namespaces(self):
        """Test invalid namespace names"""
        assert validate_namespace("") == False
        assert validate_namespace("INVALID") == False


class TestValidateThreshold:
    """Test threshold validation"""
    
    def test_valid_thresholds(self):
        """Test valid threshold values"""
        assert validate_threshold(50, 0, 100, "cpu") == True
        assert validate_threshold(0, 0, 100, "cpu") == True
        assert validate_threshold(100, 0, 100, "cpu") == True
        assert validate_threshold(1.5, 0, 10, "memory") == True
    
    def test_invalid_thresholds(self):
        """Test invalid threshold values"""
        assert validate_threshold(-1, 0, 100, "cpu") == False
        assert validate_threshold(101, 0, 100, "cpu") == False
        assert validate_threshold(50, 60, 100, "cpu") == False


class TestSanitizeCommand:
    """Test command sanitization"""
    
    def test_safe_commands(self):
        """Test safe commands pass through"""
        assert sanitize_command("ls -la") == "ls -la"
        assert sanitize_command("kubectl get pods") == "kubectl get pods"
    
    def test_dangerous_commands(self):
        """Test dangerous patterns are removed"""
        assert ";" not in sanitize_command("ls; rm -rf /")
        assert "&&" not in sanitize_command("ls && rm file")
        assert "|" not in sanitize_command("cat file | grep secret")
        assert "`" not in sanitize_command("echo `whoami`")
        assert "$" not in sanitize_command("echo $SECRET")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
