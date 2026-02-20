"""Unit tests for security module"""
import pytest
from stars.security import (
    validate_k8s_name,
    validate_namespace,
    validate_threshold,
    sanitize_command,
    redact_secrets
)


class TestValidation:
    def test_valid_k8s_name(self):
        assert validate_k8s_name("my-pod") == True
        assert validate_k8s_name("pod123") == True
        assert validate_k8s_name("a") == True
    
    def test_invalid_k8s_name(self):
        assert validate_k8s_name("My-Pod") == False  # uppercase
        assert validate_k8s_name("-pod") == False  # starts with dash
        assert validate_k8s_name("pod-") == False  # ends with dash
        assert validate_k8s_name("pod_name") == False  # underscore
        assert validate_k8s_name("a" * 254) == False  # too long
    
    def test_validate_threshold(self):
        assert validate_threshold(50) == True
        assert validate_threshold(0) == True
        assert validate_threshold(100) == True
        assert validate_threshold(-1) == False
        assert validate_threshold(101) == False
        assert validate_threshold("50") == False  # not int


class TestCommandSanitization:
    def test_allowed_commands(self):
        assert sanitize_command("tars health") == ["tars", "health"]
        assert sanitize_command("kubectl get pods") == ["kubectl", "get", "pods"]
    
    def test_dangerous_commands(self):
        with pytest.raises(ValueError):
            sanitize_command("rm -rf /")
        
        with pytest.raises(ValueError):
            sanitize_command("kubectl get pods; rm file")
        
        with pytest.raises(ValueError):
            sanitize_command("kubectl get pods | grep test")


class TestSecretRedaction:
    def test_redact_password(self):
        text = "password=secret123"
        assert "secret123" not in redact_secrets(text)
        assert "REDACTED" in redact_secrets(text)
    
    def test_redact_api_key(self):
        text = "api_key=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        result = redact_secrets(text)
        assert "AIza" not in result
        assert "REDACTED" in result
    
    def test_redact_token(self):
        text = "token: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        result = redact_secrets(text)
        assert "sk-" not in result
        assert "REDACTED" in result
    
    def test_preserve_non_secrets(self):
        text = "This is a normal message"
        assert redact_secrets(text) == text
