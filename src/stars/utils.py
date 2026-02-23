"""Utility functions for formatting and display"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from typing import List, Dict, Any, Optional
import logging
import re

console = Console()
logger = logging.getLogger(__name__)

# Sensitive data patterns for redaction
# Each tuple is (compiled_regex, replacement_string).
# IMPORTANT: replacements are plain strings, not backreference templates —
# do NOT use \1 or group references here unless you also update the sub() calls.
SENSITIVE_PATTERNS = [
    # Key=value style secrets (covers YAML, JSON, env-var formats)
    (re.compile(r'password\s*["\s:=]+\s*[^\s",}\]]+', re.IGNORECASE), 'password=<REDACTED>'),
    (re.compile(r'token\s*["\s:=]+\s*[^\s",}\]]+', re.IGNORECASE), 'token=<REDACTED>'),
    (re.compile(r'api[_-]?key\s*["\s:=]+\s*[^\s",}\]]+', re.IGNORECASE), 'api_key=<REDACTED>'),
    (re.compile(r'secret\s*["\s:=]+\s*[^\s",}\]]+', re.IGNORECASE), 'secret=<REDACTED>'),
    # HTTP auth headers (Bearer tokens, Basic auth, etc.)
    (re.compile(r'bearer\s+[A-Za-z0-9\-_=.+/]{8,}', re.IGNORECASE), 'bearer <REDACTED>'),
    (re.compile(r'authorization\s*:\s*\S+', re.IGNORECASE), 'authorization: <REDACTED>'),
    # AWS IAM access keys — always exactly AKIA + 16 uppercase alphanum
    (re.compile(r'AKIA[0-9A-Z]{16}'), '<REDACTED_AWS_KEY>'),
    # PEM private keys (multi-line)
    (re.compile(
        r'-----BEGIN\s[A-Z ]*PRIVATE KEY-----.*?-----END\s[A-Z ]*PRIVATE KEY-----',
        re.DOTALL | re.IGNORECASE,
    ), '<REDACTED_PRIVATE_KEY>'),
    # Kubernetes / JWT tokens — eyJ prefix, three dot-separated base64url segments.
    # Pattern intentionally broad so it catches tokens inside JSON string values.
    (re.compile(r'eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}'), '<REDACTED_JWT>'),
    # Generic high-entropy base64 blobs (≥40 chars) on their own "token".
    # Use word-boundary-like anchors that don't consume surrounding whitespace.
    (re.compile(r'(?<![A-Za-z0-9+/])([A-Za-z0-9+/]{40,}={0,2})(?![A-Za-z0-9+/=])'), '<REDACTED_BASE64>'),
]


def redact_sensitive_data(text: Optional[str]) -> Optional[str]:
    """
    Redact sensitive information from text before sending to AI or logging.

    Args:
        text: Text that may contain sensitive data (None is accepted and returned as-is).

    Returns:
        Text with sensitive data replaced by placeholder tokens, or None/empty
        unchanged.
    """
    if not text:
        return text

    redacted = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)

    return redacted


def create_table(title: str, columns: List[str]) -> Table:
    """Create a formatted table"""
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col)
    return table


def print_error(message: str):
    """Print error message"""
    console.print(f"[bold red]✗[/bold red] {message}")
    logger.error(message)


def print_success(message: str):
    """Print success message"""
    console.print(f"[bold green]✓[/bold green] {message}")
    logger.info(message)


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")
    logger.warning(message)


def print_info(message: str):
    """Print info message"""
    console.print(f"{message}")
    logger.info(message)


def print_panel(content: str, title: str = ""):
    """Print content in a panel"""
    console.print(Panel(content, title=title, border_style="cyan"))


def format_pod_status(status: str) -> str:
    """Format pod status with color"""
    status_colors = {
        "Running": "green",
        "Pending": "yellow",
        "Failed": "red",
        "Unknown": "dim",
        "Succeeded": "green",
        "CrashLoopBackOff": "red",
    }
    color = status_colors.get(status, "white")
    return f"[{color}]{status}[/{color}]"


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f}PB"


def truncate_string(s: str, max_length: int = 50) -> str:
    """Truncate string with ellipsis"""
    return s if len(s) <= max_length else s[:max_length-3] + "..."
