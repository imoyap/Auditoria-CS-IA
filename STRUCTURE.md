# Repository Structure

Complete guide to the Auditoria-CS-IA repository structure.

## Root Level Files

```
.
├── README.md                 # Project overview & quick start
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
├── STRUCTURE.md              # This file - directory guide
├── REPOSITORY_AUDIT.md       # Audit & reorganization plan
│
├── pyproject.toml            # Python project configuration
├── .gitignore                # Git ignore rules
├── Makefile                  # Common tasks
├── docker-compose.yml        # Docker compose for local dev
└── .claude/                  # Claude Code integration
    ├── settings.json         # Harness configuration
    └── skills/               # Custom Claude Code skills
        ├── quick-audit.md
        ├── audit-status.md
        ├── audit-api.md
        └── audit-report.md
```

## Source Code

```
auditoria/                  # Main package
├── __init__.py
├── cli.py                  # Command-line interface
│
├── core/                   # Core functionality
│   ├── __init__.py
│   ├── engine.py           # Audit orchestration engine
│   ├── models.py           # Data models (Finding, Report, etc.)
│   └── reporter.py         # Multi-format report generation
│
├── checks/                 # Audit check modules
│   ├── __init__.py
│   ├── base.py             # BaseCheck abstract class
│   ├── registry.py         # Check registration system
│   ├── system.py           # System checks
│   ├── network.py          # Network checks
│   ├── ssl_tls.py          # SSL/TLS checks
│   ├── filesystem.py       # Filesystem checks
│   └── secrets.py          # Secrets detection
│
├── ai/                     # AI/LLM integration
│   ├── __init__.py
│   ├── analyzer.py         # Claude API integration
│   └── prompts.py          # Prompt templates
│
├── api/                    # REST API
│   ├── __init__.py
│   ├── server.py           # Flask application
│   └── webhooks.py         # Webhook management
│
├── mcp/                    # Model Context Protocol
│   ├── __init__.py
│   ├── server.py           # MCP server
│   └── tools.py            # Tool definitions
│
├── scheduler/              # Task scheduling
│   ├── __init__.py
│   └── executor.py         # Scheduler implementation
│
├── storage/                # Data persistence
│   ├── __init__.py
│   └── database.py         # SQLite manager
│
└── templates/              # Report templates
    └── report.html
```

## Documentation

```
docs/                       # Full documentation
├── README.md               # Documentation index
│
├── guides/                 # User guides
│   ├── quick-start.md
│   ├── installation.md
│   ├── usage.md
│   ├── api-reference.md
│   └── cli-reference.md
│
├── architecture/           # Technical architecture
│   ├── overview.md         # System design
│   ├── modules.md          # Module breakdown
│   ├── data-flow.md        # Data flow diagram
│   └── decisions.md        # ADRs (Architecture Decision Records)
│
├── operations/             # Operations & deployment
│   ├── deployment.md       # Deployment guide
│   ├── configuration.md    # Configuration guide
│   ├── monitoring.md       # Monitoring setup
│   ├── troubleshooting.md  # Troubleshooting
│   └── runbooks/
│       ├── incident-response.md
│       ├── scaling.md
│       └── backup-restore.md
│
├── development/            # Developer guides
│   ├── setup.md            # Dev environment setup
│   ├── testing.md          # Testing guide
│   ├── contributing.md     # Contributing guide
│   └── code-style.md       # Code standards
│
├── advanced/               # Advanced topics
│   ├── extending.md        # Custom checks
│   ├── performance.md      # Performance tuning
│   ├── security.md         # Security considerations
│   └── roadmap.md          # v1.0 → v2.0 roadmap
│
└── reference/              # Reference materials
    ├── glossary.md         # Term definitions
    ├── faq.md              # Frequently asked questions
    └── specifications.md   # Formal specifications
```

## Tests

```
tests/                      # Test suite
├── conftest.py             # Pytest configuration
├── README.md               # Testing guide
│
├── fixtures/               # Test fixtures
│   ├── __init__.py
│   ├── audit_fixtures.py
│   ├── mock_data.py
│   └── sample_reports/
│
├── unit/                   # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_engine.py
│   ├── test_checks.py
│   ├── test_analyzer.py
│   └── test_*.py
│
├── integration/            # Integration tests
│   ├── __init__.py
│   ├── test_audit_workflow.py
│   ├── test_api.py
│   └── test_database.py
│
└── e2e/                    # End-to-end tests
    ├── __init__.py
    └── test_full_audit.py
```

## Configuration

```
config/                     # Configuration files
├── README.md               # Configuration guide
├── development.env.example # Dev environment template
├── production.env.example  # Prod environment template
├── logging.yaml            # Logging configuration
├── prometheus.yml          # Prometheus configuration
└── kubernetes/
    ├── deployment.yaml
    ├── service.yaml
    └── configmap.yaml
```

## Scripts & Utilities

```
scripts/                    # Utility scripts
├── README.md               # Scripts guide
├── run_api.py              # Start API server
├── test_deployment.py      # Deployment validation
├── deploy.sh               # Deployment script
├── health-check.sh         # Health check script
├── backup.sh               # Database backup
└── restore.sh              # Restore from backup
```

## Examples

```
examples/                   # Example code
├── README.md
├── mcp_integration.py      # MCP usage example
├── rest_client.py          # REST API client example
├── custom_check.py         # Custom check example
└── advanced_usage.py       # Advanced usage examples
```

## Docker

```
docker/                     # Docker configuration
├── Dockerfile              # Production image
├── Dockerfile.prod         # Production optimized
└── entrypoint.sh           # Container entrypoint
```

## CI/CD

```
.github/                    # GitHub integration
└── workflows/              # GitHub Actions workflows
    ├── tests.yml           # Test automation
    ├── lint.yml            # Linting automation
    └── deploy.yml          # Deployment automation
```

## Data & Reports

```
data/                       # Generated data (git-ignored)
├── audit-results/          # Audit execution outputs
├── reports/                # Generated reports
└── logs/                   # Application logs
```

---

## File Organization Principles

### Root Level
Only these belong in root:
- Project metadata (README, CHANGELOG, LICENSE, etc.)
- Configuration (pyproject.toml, .gitignore, etc.)
- Build/run files (Makefile, docker-compose.yml, etc.)

### Source Code (`auditoria/`)
- Organized by function (core, checks, api, etc.)
- Each module is independent
- Clear dependencies

### Documentation (`docs/`)
- Organized by audience/purpose
- Easy navigation with indexes
- Comprehensive and discoverable

### Tests (`tests/`)
- Organized by test type
- Shared fixtures in `fixtures/`
- Clear structure mirrors source

### Configuration (`config/`)
- Templates with examples
- Environment-specific configs
- Documented with README

### Scripts (`scripts/`)
- Utility scripts for operations
- Documented with help text
- Organized by purpose

### Data (`data/`)
- Never committed to git
- Generated outputs only
- Organized by type

---

## Navigation Examples

### I need to...
- Add a new audit check → `auditoria/checks/newcheck.py`
- Write a test → `tests/unit/test_newcheck.py`
- Update documentation → `docs/guides/` or `docs/architecture/`
- Deploy the system → `scripts/deploy.sh` & `docs/operations/deployment.md`
- Add configuration → `config/` & `docs/operations/configuration.md`
- Create an example → `examples/`

---

## Consistency Checks

To verify the structure:

```bash
# Check directory structure
tree -L 2 -a

# Check documentation completeness
ls -la docs/{guides,architecture,operations,development,advanced,reference}/

# Check test organization
ls -la tests/{unit,integration,e2e,fixtures}/

# Check scripts
ls -la scripts/

# Check configuration
ls -la config/
```

---

## Quick Reference

| Purpose | Location | Example |
|---------|----------|---------|
| Add audit check | `auditoria/checks/` | `ssl_tls.py` |
| Add test | `tests/unit/` or `tests/integration/` | `test_engine.py` |
| Write docs | `docs/` | `docs/guides/usage.md` |
| Configure | `config/` | `logging.yaml` |
| Run task | `Makefile` | `make test` |
| Add example | `examples/` | `custom_check.py` |
| Deploy | `scripts/` | `deploy.sh` |
| Data/output | `data/` | `data/audit-results/` |

---

**Last Updated**: 2026-07-28  
**Version**: 1.0.0
