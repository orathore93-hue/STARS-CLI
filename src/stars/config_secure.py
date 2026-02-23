"""Secure configuration management with OS keychain integration"""
import os
import stat
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings
import yaml

logger = logging.getLogger(__name__)

# Directories with secure permissions
STARS_DIR: Path = Path.home() / ".stars"
STARS_DIR.mkdir(exist_ok=True, mode=0o700)

CONFIG_FILE: Path = STARS_DIR / "config.yaml"
LOG_FILE: Path = STARS_DIR / "tars.log"
HISTORY_FILE: Path = STARS_DIR / "history.json"
AUDIT_LOG: Path = STARS_DIR / "audit.log"
CONSENT_FILE: Path = STARS_DIR / "ai_consent"
LOGS_DIR: Path = STARS_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True, mode=0o700)

# Ensure secure permissions
for file_path in [CONFIG_FILE, LOG_FILE, HISTORY_FILE, AUDIT_LOG]:
    if file_path.exists():
        os.chmod(file_path, 0o600)


# ============================================================================
# KEYCHAIN INTEGRATION
# ============================================================================

def _get_keyring() -> Optional[object]:
    """Get keyring backend with fallback handling"""
    try:
        import keyring
        # Test if keyring is accessible
        keyring.get_keyring()
        return keyring
    except Exception as e:
        logger.debug(f"Keyring unavailable: {e}")
        return None


def save_api_key_secure(key: str) -> bool:
    """
    Save API key to OS keychain securely.
    
    Args:
        key: The API key to store
        
    Returns:
        True if saved to keychain, False if fallback to env var needed
    """
    kr = _get_keyring()
    if kr:
        try:
            kr.set_password("stars-cli", "gemini_api_key", key)
            logger.info("API key saved to OS keychain")
            return True
        except Exception as e:
            logger.warning(f"Failed to save to keychain: {e}")
    
    logger.info("Keychain unavailable - use GEMINI_API_KEY environment variable")
    return False


def get_api_key_secure() -> Optional[str]:
    """
    Retrieve API key from OS keychain with environment variable fallback.
    
    Priority:
    1. OS keychain (macOS Keychain, Windows Credential Manager, Linux Secret Service)
    2. GEMINI_API_KEY environment variable
    3. None
    
    Returns:
        API key or None if not found
    """
    # Try keychain first
    kr = _get_keyring()
    if kr:
        try:
            key = kr.get_password("stars-cli", "gemini_api_key")
            if key:
                logger.debug("API key retrieved from OS keychain")
                return key
        except Exception as e:
            logger.debug(f"Keychain read failed: {e}")
    
    # Fallback to environment variable
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        logger.debug("API key retrieved from environment variable")
        return key
    
    logger.debug("No API key found in keychain or environment")
    return None


def delete_api_key_secure() -> bool:
    """
    Delete API key from OS keychain.
    
    Returns:
        True if deleted, False if not found or error
    """
    kr = _get_keyring()
    if kr:
        try:
            kr.delete_password("stars-cli", "gemini_api_key")
            logger.info("API key deleted from OS keychain")
            return True
        except Exception as e:
            logger.debug(f"Failed to delete from keychain: {e}")
    return False


# ============================================================================
# CONSENT MANAGEMENT
# ============================================================================

def check_ai_consent() -> bool:
    """
    Check if user has consented to AI data sharing.

    Returns False if the consent file is missing OR if its permissions are
    more permissive than 0o600 (which indicates possible tampering).
    """
    if not CONSENT_FILE.exists():
        return False
    mode = stat.S_IMODE(CONSENT_FILE.stat().st_mode)
    if mode != 0o600:
        logger.warning(
            f"AI consent file has insecure permissions {oct(mode)}; "
            "treating as absent. Run 'stars privacy grant' to re-create it."
        )
        return False
    return True


def grant_ai_consent() -> None:
    """Record user consent for AI data sharing using atomic file creation."""
    from datetime import datetime
    import os as _os

    content = f"AI consent granted: {datetime.utcnow().isoformat()}\n"
    # Atomic create with 0o600 from the first byte — no chmod-after-write race.
    fd = _os.open(str(CONSENT_FILE), _os.O_WRONLY | _os.O_CREAT | _os.O_TRUNC, 0o600)
    with _os.fdopen(fd, 'w') as f:
        f.write(content)


def revoke_ai_consent() -> None:
    """Revoke user consent for AI data sharing"""
    if CONSENT_FILE.exists():
        CONSENT_FILE.unlink()


# ============================================================================
# AUDIT LOGGING
# ============================================================================

def audit_log(action: str, resource: str, namespace: str, user: Optional[str] = None) -> None:
    """
    Log actions for audit trail with secure permissions.

    All user-supplied fields are sanitised: newlines, carriage returns, and
    null bytes are stripped to prevent audit-log injection attacks.

    Args:
        action: Action performed (e.g., 'delete', 'scale', 'restart')
        resource: Resource affected (e.g., 'pod/nginx', 'deployment/api')
        namespace: Kubernetes namespace
        user: User performing action (defaults to $USER)
    """
    import json
    from datetime import datetime

    # --- Input sanitisation -------------------------------------------------
    _CONTROL = str.maketrans('', '', '\n\r\x00')

    def _sanitise(value: str, max_len: int = 512) -> str:
        if not isinstance(value, str):
            value = str(value)
        cleaned = value.translate(_CONTROL).strip()
        if len(cleaned) > max_len:
            raise ValueError(
                f"audit_log field too long ({len(cleaned)} chars, max {max_len})"
            )
        return cleaned

    action    = _sanitise(action,    max_len=64)
    resource  = _sanitise(resource,  max_len=512)
    namespace = _sanitise(namespace, max_len=63)

    if user is None:
        user = os.getenv('USER', 'unknown')
    user = _sanitise(user, max_len=64)
    # -------------------------------------------------------------------------

    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user': user,
        'action': action,
        'resource': resource,
        'namespace': namespace,
    }

    # Atomic open with mode 0o600 — no post-write chmod race window.
    fd = os.open(
        str(AUDIT_LOG),
        os.O_WRONLY | os.O_CREAT | os.O_APPEND,
        0o600,
    )
    with os.fdopen(fd, 'a') as f:
        f.write(json.dumps(entry) + '\n')


# ============================================================================
# CONFIGURATION MODELS
# ============================================================================

class ThresholdsConfig(BaseModel):
    """Resource threshold configuration"""
    cpu: int = Field(default=80, ge=0, le=100, description="CPU usage threshold %")
    memory: int = Field(default=85, ge=0, le=100, description="Memory usage threshold %")
    restarts: int = Field(default=5, ge=0, description="Pod restart threshold")


class TarsSettings(BaseSettings):
    """STARS CLI settings with secure API key handling"""
    
    # Kubernetes
    default_namespace: Optional[str] = Field(default=None, env='STARS_NAMESPACE')
    default_cluster: Optional[str] = Field(default=None, env='STARS_CLUSTER')
    
    # Prometheus
    prometheus_url: Optional[str] = Field(default=None, env='PROMETHEUS_URL')
    
    # Thresholds
    thresholds: ThresholdsConfig = Field(default_factory=ThresholdsConfig)
    
    # Monitoring
    interval: int = Field(default=30, ge=1, description="Monitoring interval in seconds")
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
    
    @validator('prometheus_url')
    def validate_prometheus_url(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Prometheus URL must start with http:// or https://')
        return v
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get API key from secure storage (keychain or env)"""
        return get_api_key_secure()


class Config:
    """Configuration manager with file persistence and secure key storage"""
    
    def __init__(self) -> None:
        self.settings: TarsSettings = TarsSettings()
        self._load_from_file()
    
    def _load_from_file(self) -> None:
        """Load additional config from YAML file"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                data = yaml.safe_load(f) or {}
                if 'thresholds' in data:
                    self.settings.thresholds = ThresholdsConfig(**data['thresholds'])
                if 'interval' in data:
                    self.settings.interval = data['interval']
    
    def save(self) -> None:
        """Save configuration to file (excludes API keys), using atomic write."""
        data = {
            'thresholds': self.settings.thresholds.dict(),
            'interval': self.settings.interval,
        }
        tmp_path = str(CONFIG_FILE) + '.tmp'
        fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        os.replace(tmp_path, CONFIG_FILE)
    
    def get(self, key: str, default: Optional[object] = None) -> Optional[object]:
        """Get configuration value by dot notation"""
        try:
            value = self.settings
            for part in key.split('.'):
                value = getattr(value, part)
            return value
        except AttributeError:
            return default
    
    def set(self, key: str, value: object) -> None:
        """Set configuration value"""
        parts = key.split('.')
        if len(parts) == 2 and parts[0] == 'thresholds':
            setattr(self.settings.thresholds, parts[1], value)
        else:
            setattr(self.settings, key, value)
        self.save()


# Global config instance
config: Config = Config()
