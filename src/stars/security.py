"""Security utilities for input validation and secret redaction"""
import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def validate_k8s_name(name: str) -> bool:
    """Validate Kubernetes resource name (RFC 1123)"""
    pattern = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
    if not re.match(pattern, name):
        logger.error(f"Invalid Kubernetes name: {name}")
        return False
    if len(name) > 253:
        logger.error(f"Name too long: {name}")
        return False
    return True


def validate_namespace(namespace: str) -> bool:
    """Validate namespace name"""
    return validate_k8s_name(namespace)


def validate_threshold(value: int, min_val: int = 0, max_val: int = 100) -> bool:
    """Validate threshold value"""
    if not isinstance(value, int):
        logger.error(f"Threshold must be integer: {value}")
        return False
    if not min_val <= value <= max_val:
        logger.error(f"Threshold out of range: {value}")
        return False
    return True


def sanitize_command(command: str) -> list:
    """Sanitize command for safe execution"""
    # Only allow whitelisted commands
    allowed_commands = ['tars', 'kubectl', 'get', 'describe', 'logs']
    
    parts = command.split()
    if not parts or parts[0] not in allowed_commands:
        raise ValueError(f"Command not allowed: {command}")
    
    # Remove dangerous characters
    dangerous_chars = [';', '|', '&', '>', '<', '`', '$', '(', ')']
    for part in parts:
        if any(char in part for char in dangerous_chars):
            raise ValueError(f"Dangerous character in command: {command}")
    
    return parts


def redact_secrets(text: str) -> str:
    """Redact potential secrets from text"""
    patterns = [
        (r'password[\"\s:=]+([^\s\"]+)', 'password=***REDACTED***'),
        (r'token[\"\s:=]+([^\s\"]+)', 'token=***REDACTED***'),
        (r'api[_-]?key[\"\s:=]+([^\s\"]+)', 'api_key=***REDACTED***'),
        (r'secret[\"\s:=]+([^\s\"]+)', 'secret=***REDACTED***'),
        (r'bearer\s+([^\s]+)', 'bearer ***REDACTED***'),
        (r'(AIza[0-9A-Za-z-_]{35})', '***REDACTED_API_KEY***'),
        (r'(sk-[a-zA-Z0-9]{48})', '***REDACTED_TOKEN***'),
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result


def confirm_destructive_action(action: str, resource: str) -> bool:
    """Confirm destructive actions with user"""
    import typer
    
    message = f"⚠️  This will {action} {resource}. Continue?"
    return typer.confirm(message, default=False)
