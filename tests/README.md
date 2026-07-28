# Test Suite

Testing guide for Auditoria-CS-IA.

## Structure

```
tests/
├── conftest.py           # Pytest configuration & shared fixtures
├── fixtures/             # Reusable test fixtures
│   ├── audit_fixtures.py
│   ├── mock_data.py
│   └── sample_reports/
├── unit/                 # Unit tests
├── integration/          # Integration tests
└── e2e/                  # End-to-end tests
```

## Running Tests

### All tests
```bash
pytest
```

### With coverage
```bash
pytest --cov=auditoria --cov-report=html tests/
```

### Specific suite
```bash
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest tests/e2e/              # End-to-end tests only
```

### Specific test
```bash
pytest tests/unit/test_engine.py::test_audit_execution
```

### Verbose output
```bash
pytest -v
```

## Writing Tests

See [Development Guide](../docs/development/testing.md) for detailed testing guidelines.

### Test Naming
- `test_*.py` — Test file naming
- `Test*` — Test class naming
- `test_*` — Test function naming

### Example
```python
def test_audit_engine_creates_job():
    """Verify audit engine creates job successfully."""
    engine = AuditEngine(target="localhost")
    report = engine.run()
    assert report.target == "localhost"
    assert report.risk_score >= 0
```

## Coverage Goals

- **Overall**: >90%
- **Core modules**: >95%
- **Checks**: >85%
- **API**: >90%

Check coverage:
```bash
pytest --cov=auditoria --cov-report=term-missing tests/
```

## Continuous Integration

Tests run automatically on:
- Every push
- Every pull request
- Before release

See `.github/workflows/tests.yml` for CI configuration.
