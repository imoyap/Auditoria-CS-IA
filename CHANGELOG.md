# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multi-agent orchestration framework (planned for v2.0)
- Spec-driven testing architecture (planned for v2.0)
- Data-driven decision making engine (planned for v2.0)

### Changed
- Reorganized repository structure for scalability

### Fixed
- SQL syntax error in database schema (references keyword)

## [1.0.0] - 2026-07-27

### Added
- Core audit framework with modular checks
- 5 audit modules: system, network, ssl, filesystem, secrets
- REST API with 18 endpoints
- MCP Server with 9 tools
- 4 Claude Code skills
- SQLite persistence with audit history
- Async webhook notification system
- Audit scheduler for cron-based execution
- HTML/JSON report generation
- Comprehensive documentation (10 guides)
- Harness integration (.claude/settings.json)

### Features
- CLI interface (audit, list, schedule, dashboard, report, mcp)
- Multi-format reporting (console, JSON, HTML)
- Risk scoring and severity classification
- Executive summary generation with Claude API
- Webhook HMAC-SHA256 verification
- Task history tracking

---

## Release Notes

### v1.0.0 (Initial Release)
**Date**: 2026-07-27  
**Status**: STABLE PROTOTYPE

#### What's Included
- ✅ 5 functional audit modules
- ✅ Multi-interface support (CLI, REST, MCP, Skills)
- ✅ Comprehensive documentation
- ✅ Local deployment validated
- ✅ Professional code structure

#### Known Limitations
- ⚠️ Synchronous execution only
- ⚠️ No formal specifications
- ⚠️ Limited security features (no RBAC)
- ⚠️ Basic observability
- ⚠️ Single-threaded

#### Next Phase (v2.0 - Planned)
- Async/queue-based execution
- Multi-agent architecture
- Formal specifications
- Comprehensive observability
- Security hardening

---

## Future Roadmap

### Q3 2026 - v1.1 (Minor improvements)
- Enhanced test coverage
- Performance optimization
- Documentation updates

### Q4 2026 - v2.0 (Major refactor)
- Multi-agent system
- Data-driven operations
- Design system for reports
- Enterprise security features
- Production SLOs

### 2027 - v3.0+ (Long-term)
- Dashboard web UI
- SIEM integration
- ML-based risk prediction
- Automated remediation
- Compliance reporting (PCI-DSS, HIPAA, ISO27001)
