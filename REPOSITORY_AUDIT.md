# Repository Audit & Reorganization Plan

**Date**: 2026-07-28  
**Status**: AUDIT COMPLETE - REORGANIZATION RECOMMENDED  
**Severity**: MEDIUM (Organizational, not functional)

---

## 📋 CURRENT STATE ANALYSIS

### File Distribution (Current)

```
📁 Root (/)
├── 📄 README.md
├── 📄 ANALYSIS.md
├── 📄 ADVANCED_FEATURES.md
├── 📄 API.md
├── 📄 CLAUDE.md
├── 📄 CRITICAL_ANALYSIS.md
├── 📄 DEPLOYMENT.md
├── 📄 DEPLOYMENT_REPORT.md
├── 📄 EXECUTIVE_SUMMARY.md
├── 📄 IMPLEMENTATION_PLAN.md
├── 📄 PROJECT_SUMMARY.md
├── 📄 SUMMARY.txt
├── 📄 run_api.py
├── 📄 test_deployment.py
├── 📄 pyproject.toml
├── 📄 .gitignore
├── 📊 auditoria_report.json
├── 🗂️ .claude/ (4 files)
├── 🗂️ auditoria/ (26 files)
├── 🗂️ examples/ (2 files)
├── 🗂️ reports/ (1 file)
├── 🗂️ tests/ (1 file)
└── 🗂️ .pytest_cache/

Total Files: ~50
Total Dirs: 8
```

### Issues Identified

#### 1. **Documentation Chaos** 🔴
**Problem**: 10 markdown files in root directory
```
Root Level:
  ANALYSIS.md
  ADVANCED_FEATURES.md
  API.md
  CLAUDE.md
  CRITICAL_ANALYSIS.md
  DEPLOYMENT.md
  DEPLOYMENT_REPORT.md
  EXECUTIVE_SUMMARY.md
  IMPLEMENTATION_PLAN.md
  PROJECT_SUMMARY.md
  SUMMARY.txt
```

**Impact**:
- ❌ Hard to find specific docs
- ❌ No clear hierarchy
- ❌ User confusion (which to read first?)
- ❌ Not scalable

**Fix**: Create `docs/` directory with subdirectories

---

#### 2. **Generated Files in Root** 🟡
**Problem**: Test/generated artifacts in root
```
Root Level:
  auditoria_report.json  (generated)
  test_deployment.py     (test script)
  run_api.py            (script)
```

**Impact**:
- ⚠️ Clutters repository
- ⚠️ Confuses source vs generated
- ⚠️ Should be in scripts/ or data/

**Fix**: Move to appropriate directories

---

#### 3. **Missing Key Files** 🟡
**Problem**: No standardized project files
```
Missing:
  ✗ .gitignore (exists but not comprehensive)
  ✗ CHANGELOG.md
  ✗ CONTRIBUTING.md
  ✗ LICENSE (should be included)
  ✗ requirements.txt (using pyproject.toml, good)
  ✗ Makefile (for common tasks)
  ✗ docker-compose.yml (for local dev)
```

**Impact**:
- ⚠️ Onboarding harder
- ⚠️ Contributing unclear
- ⚠️ Local setup not documented

**Fix**: Add missing standard files

---

#### 4. **Configuration Files Location** 🟡
**Problem**: Config scattered or missing
```
Current:
  .claude/settings.json  (good)
  pyproject.toml        (good)
  
Missing/Scattered:
  ✗ No config/ directory for app configs
  ✗ No environment templates
  ✗ No logging configuration
  ✗ No monitoring config
```

**Impact**:
- ⚠️ Hard to customize deployment
- ⚠️ Secrets management unclear

**Fix**: Create `config/` directory with examples

---

#### 5. **Test Organization** 🟡
**Problem**: Single test file, no structure
```
tests/
  └── test_auditoria.py  (monolithic)

Missing:
  ✗ tests/unit/
  ✗ tests/integration/
  ✗ tests/fixtures/
  ✗ tests/conftest.py
  ✗ tests/README.md
```

**Impact**:
- ⚠️ Tests not organized by type
- ⚠️ Hard to run specific test suites
- ⚠️ Fixtures not reusable

**Fix**: Restructure tests into subdirectories

---

#### 6. **Scripts & Utilities Scattered** 🟡
**Problem**: Scripts in various places
```
Current:
  run_api.py           (root)
  test_deployment.py   (root)
  
Should be in:
  scripts/run_api.py
  scripts/test_deployment.py
  scripts/deploy.sh
  scripts/backup.sh
  scripts/health_check.sh
```

**Impact**:
- ⚠️ Hard to find utility scripts
- ⚠️ No clear deployment process

**Fix**: Create `scripts/` directory

---

#### 7. **Data & Reports Location** 🟡
**Problem**: Generated data in root
```
Root:
  auditoria_report.json
  
reports/:
  informe.json
```

**Impact**:
- ⚠️ Mixing generated with source
- ⚠️ Should not be in git

**Fix**: Create `data/` for outputs, add to .gitignore

---

#### 8. **Architecture Documentation** 🟡
**Problem**: Architecture scattered across multiple files
```
Docs covering architecture:
  CRITICAL_ANALYSIS.md       (architecture proposal)
  CLAUDE.md                  (integration)
  IMPLEMENTATION_PLAN.md     (implementation)
  PROJECT_SUMMARY.md         (summary)
```

**Impact**:
- ⚠️ No single source of truth
- ⚠️ Redundancy

**Fix**: Consolidate into `docs/architecture/`

---

## 🎯 PROPOSED REPOSITORY STRUCTURE

### Ideal Organization

```
Auditoria-CS-IA/
│
├── 📄 README.md                    # Project overview
├── 📄 CHANGELOG.md                 # Version history
├── 📄 CONTRIBUTING.md              # Contribution guide
├── 📄 LICENSE                      # MIT License
│
├── 📋 pyproject.toml               # Python project config
├── 📋 setup.py                     # Setup (if needed)
├── 📋 .gitignore                   # Git ignore rules
│
├── 📁 .claude/                     # Claude Code integration
│   ├── settings.json               # Harness config
│   └── skills/                     # Custom skills
│       ├── quick-audit.md
│       ├── audit-status.md
│       ├── audit-api.md
│       └── audit-report.md
│
├── 📁 .github/                     # GitHub (NEW)
│   ├── workflows/
│   │   ├── tests.yml
│   │   ├── lint.yml
│   │   └── deploy.yml
│   └── ISSUE_TEMPLATE/
│
├── 📁 docs/                        # Documentation (REORGANIZED)
│   ├── README.md                   # Docs index
│   ├── index.html                  # Built docs
│   │
│   ├── guides/
│   │   ├── quick-start.md          # README excerpt
│   │   ├── installation.md         # Installation
│   │   ├── usage.md                # Usage guide
│   │   ├── api-reference.md        # API docs
│   │   └── cli-reference.md        # CLI docs
│   │
│   ├── architecture/
│   │   ├── overview.md             # System design
│   │   ├── modules.md              # Module breakdown
│   │   ├── data-flow.md            # Data flow diagram
│   │   └── decisions.md            # ADRs (Architecture Decision Records)
│   │
│   ├── operations/
│   │   ├── deployment.md           # Deployment guide
│   │   ├── configuration.md        # Configuration
│   │   ├── monitoring.md           # Monitoring & observability
│   │   ├── troubleshooting.md      # Troubleshooting
│   │   └── runbooks/
│   │       ├── incident-response.md
│   │       ├── scaling.md
│   │       └── backup-restore.md
│   │
│   ├── development/
│   │   ├── setup.md                # Dev environment
│   │   ├── testing.md              # Testing guide
│   │   ├── contributing.md         # Contributing
│   │   └── code-style.md           # Code standards
│   │
│   ├── advanced/
│   │   ├── extending.md            # Adding custom checks
│   │   ├── performance.md          # Performance tuning
│   │   ├── security.md             # Security considerations
│   │   └── roadmap.md              # v1.0 → v2.0 roadmap
│   │
│   └── reference/
│       ├── glossary.md             # Term definitions
│       ├── faq.md                  # Frequently asked questions
│       └── specifications.md       # Formal specs
│
├── 📁 auditoria/                   # Main package (ORGANIZED)
│   ├── __init__.py                 # Package init
│   │
│   ├── core/                       # Core functionality
│   │   ├── __init__.py
│   │   ├── engine.py               # Audit engine
│   │   ├── models.py               # Data models
│   │   └── reporter.py             # Report generation
│   │
│   ├── checks/                     # Audit checks
│   │   ├── __init__.py
│   │   ├── base.py                 # Base check class
│   │   ├── registry.py             # Check registry
│   │   ├── system.py               # System checks
│   │   ├── network.py              # Network checks
│   │   ├── ssl_tls.py              # SSL/TLS checks
│   │   ├── filesystem.py           # Filesystem checks
│   │   └── secrets.py              # Secrets checks
│   │
│   ├── ai/                         # AI/LLM integration
│   │   ├── __init__.py
│   │   ├── analyzer.py             # AI analyzer
│   │   └── prompts.py              # Prompt templates
│   │
│   ├── api/                        # REST API
│   │   ├── __init__.py
│   │   ├── server.py               # Flask app
│   │   └── webhooks.py             # Webhook manager
│   │
│   ├── mcp/                        # MCP server
│   │   ├── __init__.py
│   │   ├── server.py               # MCP server
│   │   └── tools.py                # Tool definitions
│   │
│   ├── scheduler/                  # Task scheduler
│   │   ├── __init__.py
│   │   └── executor.py             # Scheduler executor
│   │
│   ├── storage/                    # Data persistence
│   │   ├── __init__.py
│   │   └── database.py             # Database manager
│   │
│   ├── cli.py                      # CLI interface
│   │
│   └── templates/                  # Report templates
│       └── report.html
│
├── 📁 tests/                       # Test suite (REORGANIZED)
│   ├── __init__.py
│   ├── conftest.py                 # Pytest config
│   ├── README.md                   # Testing guide
│   │
│   ├── fixtures/                   # Test fixtures
│   │   ├── __init__.py
│   │   ├── audit_fixtures.py
│   │   ├── mock_data.py
│   │   └── sample_reports/
│   │
│   ├── unit/                       # Unit tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_engine.py
│   │   ├── test_checks.py
│   │   └── test_analyzer.py
│   │
│   ├── integration/                # Integration tests
│   │   ├── __init__.py
│   │   ├── test_audit_workflow.py
│   │   ├── test_api.py
│   │   └── test_database.py
│   │
│   └── e2e/                        # End-to-end tests
│       ├── __init__.py
│       └── test_full_audit.py
│
├── 📁 scripts/                     # Utility scripts (NEW)
│   ├── run_api.py                  # Start API server
│   ├── test_deployment.py          # Deployment tests
│   ├── deploy.sh                   # Deployment script
│   ├── health-check.sh             # Health check
│   ├── backup.sh                   # Database backup
│   └── restore.sh                  # Restore from backup
│
├── 📁 config/                      # Configuration files (NEW)
│   ├── README.md
│   ├── development.env.example     # Dev config template
│   ├── production.env.example      # Prod config template
│   ├── logging.yaml                # Logging configuration
│   ├── prometheus.yml              # Monitoring config
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── configmap.yaml
│
├── 📁 examples/                    # Example code
│   ├── README.md
│   ├── mcp_integration.py
│   ├── rest_client.py
│   ├── custom_check.py             # Example custom check
│   └── advanced_usage.py           # Advanced examples
│
├── 📁 data/                        # Generated data (NEW)
│   ├── .gitkeep
│   ├── audit-results/              # Audit outputs
│   ├── reports/                    # Generated reports
│   └── logs/                       # Application logs
│
└── 📁 docker/                      # Docker config (NEW)
    ├── Dockerfile
    ├── docker-compose.yml
    ├── Dockerfile.prod
    └── entrypoint.sh
```

---

## 📊 BEFORE → AFTER COMPARISON

### File Count by Category

| Category | Before | After | Change |
|----------|--------|-------|--------|
| Docs in root | 10 | 0 | -10 |
| Docs total | 10 | 25+ | +15 |
| Test files | 1 | 8+ | +7 |
| Scripts | 2 (in root) | 6 (in scripts/) | Organized |
| Config | 1 | 5+ | Better organized |
| Examples | 2 | 4+ | Expanded |
| Total organization | Chaotic | Clear hierarchy | Much better |

---

## 🔄 REORGANIZATION STEPS

### Phase 1: Create Directory Structure

```bash
# Create directories
mkdir -p docs/{guides,architecture,operations,development,advanced,reference}
mkdir -p docs/operations/runbooks
mkdir -p tests/{fixtures,unit,integration,e2e}
mkdir -p scripts
mkdir -p config/kubernetes
mkdir -p examples
mkdir -p data/{audit-results,reports,logs}
mkdir -p docker
mkdir -p .github/workflows
```

### Phase 2: Move Documentation

```bash
# Move user-facing guides to docs/guides/
docs/guides/quick-start.md          ← README excerpt
docs/guides/installation.md         ← README section
docs/guides/usage.md                ← README section
docs/guides/api-reference.md        ← API.md
docs/guides/cli-reference.md        ← Extract from CLAUDE.md

# Move architecture docs
docs/architecture/overview.md       ← CRITICAL_ANALYSIS.md (condensed)
docs/architecture/modules.md        ← PROJECT_SUMMARY.md (modules section)
docs/architecture/decisions.md      ← IMPLEMENTATION_PLAN.md

# Move operational docs
docs/operations/deployment.md       ← DEPLOYMENT.md
docs/operations/configuration.md    ← New
docs/operations/monitoring.md       ← New

# Move advanced/reference
docs/advanced/roadmap.md            ← IMPLEMENTATION_PLAN.md
docs/reference/glossary.md          ← New
docs/reference/specifications.md    ← New (formal specs)
```

### Phase 3: Reorganize Source Code

```bash
# Already organized - verify structure
auditoria/core/       ✓ OK
auditoria/checks/     ✓ OK
auditoria/ai/         ✓ OK
auditoria/api/        ✓ OK
auditoria/mcp/        ✓ OK
auditoria/scheduler/  ✓ OK
auditoria/storage/    ✓ OK
```

### Phase 4: Reorganize Tests

```bash
# Move tests to subdirectories
tests/unit/test_models.py
tests/unit/test_engine.py
tests/unit/test_checks.py
tests/integration/test_audit_workflow.py
tests/integration/test_api.py
tests/e2e/test_full_audit.py
```

### Phase 5: Move Scripts

```bash
scripts/run_api.py                  ← run_api.py
scripts/test_deployment.py          ← test_deployment.py
scripts/deploy.sh                   ← New
scripts/health-check.sh             ← New
```

### Phase 6: Create Missing Standard Files

```bash
# Add these files
CHANGELOG.md                        # Version history
CONTRIBUTING.md                     # Contribution guide
.github/ISSUE_TEMPLATE/bug.md      # Bug report template
.github/ISSUE_TEMPLATE/feature.md  # Feature request template
docker-compose.yml                  # Local development
Makefile                            # Common tasks
```

### Phase 7: Update .gitignore

```bash
# Add to .gitignore
data/
*.db
*.db-wal
*.db-shm
*.log
.env.local
*.pyc
__pycache__/
.pytest_cache/
venv_test/
htmlcov/
.coverage
*.egg-info/
dist/
build/
.DS_Store
*.swp
*.swo
*~
```

---

## 📋 MASTER DOCUMENTATION INDEX

After reorganization, create `docs/README.md`:

```markdown
# Auditoria-CS-IA Documentation

## Getting Started
- [Quick Start](guides/quick-start.md)
- [Installation](guides/installation.md)
- [Basic Usage](guides/usage.md)

## Guides
- [API Reference](guides/api-reference.md)
- [CLI Reference](guides/cli-reference.md)
- [Configuration](operations/configuration.md)

## Architecture
- [System Overview](architecture/overview.md)
- [Module Breakdown](architecture/modules.md)
- [Data Flow](architecture/data-flow.md)
- [Design Decisions](architecture/decisions.md)

## Operations
- [Deployment](operations/deployment.md)
- [Monitoring](operations/monitoring.md)
- [Troubleshooting](operations/troubleshooting.md)
- [Runbooks](operations/runbooks/)

## Development
- [Setup Dev Environment](development/setup.md)
- [Testing Guide](development/testing.md)
- [Contributing](development/contributing.md)
- [Code Style](development/code-style.md)

## Advanced
- [Extending (Custom Checks)](advanced/extending.md)
- [Performance Tuning](advanced/performance.md)
- [Security](advanced/security.md)
- [Roadmap v1.0 → v2.0](advanced/roadmap.md)

## Reference
- [Glossary](reference/glossary.md)
- [FAQ](reference/faq.md)
- [Specifications](reference/specifications.md)
```

---

## ✅ REORGANIZATION CHECKLIST

### Documentation
- [ ] Create `docs/` directory structure
- [ ] Move docs to appropriate subdirectories
- [ ] Update README.md (shorten, link to docs)
- [ ] Create docs/README.md (master index)
- [ ] Update internal links in docs
- [ ] Create CHANGELOG.md
- [ ] Create CONTRIBUTING.md

### Code
- [ ] Verify auditoria/ structure (already good)
- [ ] Update imports if paths change
- [ ] Run tests to verify nothing broke

### Tests
- [ ] Create tests/unit/, tests/integration/
- [ ] Move test files to appropriate directories
- [ ] Create tests/conftest.py
- [ ] Create tests/fixtures/
- [ ] Create tests/README.md

### Scripts & Config
- [ ] Create scripts/ directory
- [ ] Move run_api.py, test_deployment.py to scripts/
- [ ] Create config/ directory with templates
- [ ] Create Makefile with common tasks
- [ ] Create docker-compose.yml

### Standard Files
- [ ] Add CONTRIBUTING.md
- [ ] Add LICENSE (MIT)
- [ ] Add CHANGELOG.md
- [ ] Add .github/workflows/ (if not present)
- [ ] Update .gitignore comprehensively

### Generated Files
- [ ] Create data/ directory
- [ ] Move auditoria_report.json to data/
- [ ] Add data/ to .gitignore
- [ ] Clean up root directory

### Verification
- [ ] All imports still work
- [ ] All tests pass
- [ ] All scripts executable
- [ ] README links correct
- [ ] Docs navigation works
- [ ] Git status clean (except generated data/)

---

## 🎯 EXPECTED OUTCOMES

### After Reorganization

```
✅ Clear navigation hierarchy
✅ Easy to find specific documentation
✅ Professional project structure
✅ Scalable for growth
✅ Standard practice compliance
✅ Better onboarding experience
✅ Clean git repository
✅ Organized test suite
✅ Clear deployment process
✅ Centralized configuration
```

---

## 📈 LONG-TERM BENEFITS

### Maintainability
- Easier to find files
- Clear purpose for each directory
- Reduced cognitive load

### Scalability
- Room for more docs/tests/examples
- Professional structure attracts contributors
- Easier team onboarding

### Quality
- Tests organized by type
- Fixtures reusable
- Configuration centralized

### Operations
- Clear deployment process
- Runbooks organized
- Monitoring configuration centralized

---

## 🚀 NEXT STEPS

1. **Review this plan** — Agree on structure
2. **Execute Phase 1-3** — Create directories, move files
3. **Update imports** — Verify nothing breaks
4. **Run tests** — Ensure functionality intact
5. **Commit** — "refactor: reorganize repository structure"
6. **Execute Phase 4-7** — Add missing files, update docs
7. **Final review** — Clean up, verify completeness

---

**Estimated effort**: 4-6 hours  
**Risk level**: LOW (mostly moves, no code changes)  
**Benefit**: HIGH (professional structure, easier maintenance)
