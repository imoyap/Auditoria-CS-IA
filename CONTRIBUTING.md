# Contributing to Auditoria-CS-IA

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional. We welcome contributors from all backgrounds.

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/Auditoria-CS-IA.git
cd Auditoria-CS-IA
```

### 2. Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -e ".[dev,api]"
```

### 3. Read Documentation
- [Architecture Overview](docs/architecture/overview.md)
- [Development Setup](docs/development/setup.md)
- [Code Style Guide](docs/development/code-style.md)

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow code style guidelines
- Add tests for new functionality
- Update documentation if needed

### 3. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=auditoria tests/

# Run specific test suite
pytest tests/unit/
```

### 4. Lint & Format
```bash
# Format code
black auditoria/ tests/

# Check linting
flake8 auditoria/ tests/

# Type checking
mypy auditoria/
```

### 5. Commit Changes
```bash
git add .
git commit -m "feat: description of changes

Longer explanation if needed.

Closes #123 (if applicable)"
```

### 6. Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub with:
- Clear title
- Description of changes
- Link to issues if applicable
- Testing instructions

## Types of Contributions

### 1. Bug Reports
- Describe the bug clearly
- Include steps to reproduce
- Share expected vs actual behavior
- Attach logs if possible

### 2. Feature Requests
- Explain use case
- Provide examples
- Discuss potential implementation

### 3. Code Contributions
- Fork the repository
- Follow development workflow
- Ensure tests pass
- Keep commits atomic

### 4. Documentation
- Fix typos
- Improve clarity
- Add examples
- Update guides

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Max line length: 100 characters
- Use f-strings for formatting

### Commit Messages
- Start with verb (feat, fix, docs, test, refactor)
- Write concise summary (50 chars max)
- Add explanation if needed
- Reference issues: `Closes #123`

### Comments
- Only comment WHY, not WHAT
- Keep comments brief
- Update comments with code

## Testing Requirements

### Unit Tests
- Test individual functions
- Mock external dependencies
- Aim for >90% coverage

### Integration Tests
- Test component interaction
- Use real databases (in-memory for tests)
- Test error paths

### End-to-End Tests
- Test full workflows
- Close to production setup
- Validate user experience

## Pull Request Process

1. **Ensure tests pass**: `pytest`
2. **Verify coverage**: Coverage >90% for new code
3. **Check linting**: `flake8` passes
4. **Update docs**: If API/behavior changed
5. **Link issues**: Reference related issues
6. **Descriptive PR**: Clear title and description

## Adding a New Audit Module

See [docs/advanced/extending.md](docs/advanced/extending.md) for detailed guide.

Quick summary:
1. Create file in `auditoria/checks/mycheck.py`
2. Extend `BaseCheck`
3. Implement `run()` method
4. Register with `@register_check` decorator
5. Add tests in `tests/unit/test_mycheck.py`
6. Update documentation

## Reporting Security Issues

**Do not** open public issues for security vulnerabilities.

Email security@example.com with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Project documentation

## Questions?

- Check [FAQ](docs/reference/faq.md)
- Read [Architecture](docs/architecture/overview.md)
- Open a GitHub Discussion

Thank you for contributing to Auditoria-CS-IA! 🙏
