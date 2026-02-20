# Contributing to STARS CLI

Thank you for your interest in contributing to STARS CLI! This document provides guidelines and requirements for contributions.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork the repository**
   ```bash
   gh repo fork orathore93-hue/STARS-CLI
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/STARS-CLI.git
   cd STARS-CLI
   ```

3. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install pre-commit hooks**
   ```bash
   cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch Naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `security/` - Security improvements
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements

### 2. Make Changes

**Code Style:**
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused and small

**Example:**
```python
def get_pod_status(namespace: str, pod_name: str) -> dict:
    """
    Get the status of a specific pod.
    
    Args:
        namespace: Kubernetes namespace
        pod_name: Name of the pod
        
    Returns:
        Dictionary containing pod status information
        
    Raises:
        KubernetesError: If pod not found or API error
    """
    try:
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(pod_name, namespace)
        return {"status": pod.status.phase}
    except ApiException as e:
        raise KubernetesError(f"Failed to get pod status: {e}")
```

### 3. Test Your Changes

```bash
# Run test suite
python3 test_cli.py

# Test specific command
stars your-command --help
stars your-command --test-args

# Check for security issues
bandit -r src/

# Verify no secrets
git diff | grep -iE "api_key|password|secret"
```

### 4. Commit Changes

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `security` - Security improvement
- `refactor` - Code refactoring
- `test` - Test updates
- `ci` - CI/CD changes

**Example:**
```bash
git commit -m "feat(cli): Add pod restart command

Implements pod restart functionality with safety checks:
- Validates pod exists before restart
- Confirms with user for production namespaces
- Logs restart action to incident manager

Closes #123"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a PR on GitHub with:
- Clear title and description
- Reference related issues
- Screenshots/examples if applicable
- Checklist of changes

## Pull Request Requirements

### Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No secrets or credentials in code
- [ ] Security scan passed
- [ ] Commit messages follow convention

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs
   - Security scans execute
   - Tests must pass
   - Code coverage maintained

2. **Code Review**
   - At least one approval required
   - Address all review comments
   - Resolve merge conflicts

3. **Merge**
   - Squash and merge preferred
   - Delete branch after merge

## Security Guidelines

### DO ✅

- Use OS keychain for credentials
- Validate all user inputs
- Handle errors gracefully
- Log security events
- Use parameterized queries
- Encrypt sensitive data

### DON'T ❌

- Hardcode credentials
- Log sensitive information
- Trust user input without validation
- Ignore security warnings
- Commit secrets to repository
- Use deprecated libraries

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Go to https://github.com/orathore93-hue/STARS-CLI/security/advisories
2. Click "Report a vulnerability"
3. Provide detailed description
4. Wait for private response

## Testing Guidelines

### Unit Tests

```python
import pytest
from stars.commands import get_pod_status

def test_get_pod_status_success():
    """Test successful pod status retrieval"""
    status = get_pod_status("default", "test-pod")
    assert status["status"] == "Running"

def test_get_pod_status_not_found():
    """Test pod not found error"""
    with pytest.raises(KubernetesError):
        get_pod_status("default", "nonexistent-pod")
```

### Integration Tests

```python
def test_health_command_integration():
    """Test health command end-to-end"""
    result = subprocess.run(
        ["stars", "health", "--namespace", "default"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Health Check" in result.stdout
```

### Test Coverage

Aim for:
- Overall: 80%+
- New features: 90%+
- Security functions: 100%

## Documentation Guidelines

### Code Documentation

```python
def complex_function(param1: str, param2: int) -> dict:
    """
    One-line summary of function.
    
    Detailed description of what the function does,
    including any important behavior or side effects.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        KubernetesError: When API call fails
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["status"])
        "success"
    """
```

### User Documentation

Update relevant docs:
- `README.md` - User-facing features
- `ARCHITECTURE.md` - Design decisions
- `SECURITY.md` - Security implications
- `CHANGELOG.md` - User-visible changes

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0) - Breaking changes
- **MINOR** (0.1.0) - New features, backward compatible
- **PATCH** (0.0.1) - Bug fixes, backward compatible

### Creating a Release

1. **Update version**
   ```bash
   # Update src/stars/__init__.py
   __version__ = "0.2.0"
   ```

2. **Update CHANGELOG.md**
   ```markdown
   ## [0.2.0] - 2026-02-21
   
   ### Added
   - New feature X
   
   ### Fixed
   - Bug Y
   ```

3. **Create tag**
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

4. **GitHub Actions will:**
   - Build binaries
   - Run security scans
   - Generate checksums
   - Create GitHub release

## Getting Help

- **Questions:** Open a discussion on GitHub
- **Bugs:** Open an issue with reproduction steps
- **Features:** Open an issue with use case description
- **Security:** Use private security advisory

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in commit history

Thank you for contributing to STARS CLI! 🌟
