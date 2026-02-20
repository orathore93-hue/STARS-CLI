# SSTARS CLI Test Suite

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=tars --cov-report=html

# Run specific test file
pytest tests/unit/test_validation.py -v

# Run with markers
pytest tests/ -m "unit" -v
pytest tests/ -m "integration" -v
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_validation.py   # Input validation tests
│   ├── test_retry.py        # Retry logic tests
│   ├── test_config.py       # Configuration tests
│   └── test_cache.py        # Cache tests
├── integration/
│   ├── __init__.py
│   ├── test_commands.py     # Command integration tests
│   └── test_api_calls.py    # API call tests
└── e2e/
    ├── __init__.py
    └── test_workflows.py    # End-to-end workflow tests
```

## Test Coverage Goals

- Unit Tests: 90%+ coverage
- Integration Tests: Key workflows
- E2E Tests: Critical user journeys

## Continuous Integration

Tests run automatically on:
- Every commit (GitHub Actions)
- Pull requests
- Before releases
