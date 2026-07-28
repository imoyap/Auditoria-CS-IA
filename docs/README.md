# Auditoria-CS-IA Documentation

Welcome to the documentation for Auditoria-CS-IA — an autonomous security audit framework powered by AI.

## 📚 Documentation Structure

### [Getting Started](guides/)
- **[Quick Start](guides/quick-start.md)** — Get up and running in 5 minutes
- **[Installation](guides/installation.md)** — Install and configure
- **[Basic Usage](guides/usage.md)** — Your first audit

### [Guides & References](guides/)
- **[API Reference](guides/api-reference.md)** — REST API endpoints
- **[CLI Reference](guides/cli-reference.md)** — Command-line commands
- **[Configuration](operations/configuration.md)** — Configure the system

### [Architecture & Design](architecture/)
- **[System Overview](architecture/overview.md)** — How it works
- **[Module Breakdown](architecture/modules.md)** — What each module does
- **[Data Flow](architecture/data-flow.md)** — How data flows through the system
- **[Design Decisions](architecture/decisions.md)** — Why we made certain choices

### [Operations & Deployment](operations/)
- **[Deployment Guide](operations/deployment.md)** — Deploy to production
- **[Configuration](operations/configuration.md)** — Environment setup
- **[Monitoring](operations/monitoring.md)** — Observability & alerting
- **[Troubleshooting](operations/troubleshooting.md)** — Solve common issues
- **[Runbooks](operations/runbooks/)** — Incident response procedures

### [Development](development/)
- **[Dev Environment Setup](development/setup.md)** — Setup for developers
- **[Testing Guide](development/testing.md)** — Write and run tests
- **[Contributing](../CONTRIBUTING.md)** — How to contribute
- **[Code Style](development/code-style.md)** — Coding standards

### [Advanced Topics](advanced/)
- **[Extending (Custom Checks)](advanced/extending.md)** — Add your own checks
- **[Performance Tuning](advanced/performance.md)** — Optimize for your use case
- **[Security Considerations](advanced/security.md)** — Security best practices
- **[Roadmap v1.0 → v2.0](advanced/roadmap.md)** — Future improvements

### [Reference](reference/)
- **[Glossary](reference/glossary.md)** — Common terms explained
- **[FAQ](reference/faq.md)** — Frequently asked questions
- **[Specifications](reference/specifications.md)** — Formal requirements

---

## 🚀 Quick Navigation

**I want to...**
- Get started quickly → [Quick Start](guides/quick-start.md)
- Understand the system → [Architecture Overview](architecture/overview.md)
- Deploy to production → [Deployment Guide](operations/deployment.md)
- Add a custom check → [Extending Guide](advanced/extending.md)
- Contribute code → [Contributing Guide](../CONTRIBUTING.md)
- Troubleshoot an issue → [Troubleshooting](operations/troubleshooting.md)
- Learn about v2.0 → [Roadmap](advanced/roadmap.md)

---

## 📖 Reading Order

### For Users
1. [Quick Start](guides/quick-start.md) — Get it running
2. [Basic Usage](guides/usage.md) — Learn how to use it
3. [Configuration](operations/configuration.md) — Customize for your needs
4. [Troubleshooting](operations/troubleshooting.md) — Fix problems

### For Operators
1. [System Overview](architecture/overview.md) — Understand the system
2. [Deployment Guide](operations/deployment.md) — Deploy it
3. [Monitoring](operations/monitoring.md) — Keep it healthy
4. [Runbooks](operations/runbooks/) — Handle incidents

### For Developers
1. [Dev Setup](development/setup.md) — Setup environment
2. [Architecture Overview](architecture/overview.md) — Understand design
3. [Code Style](development/code-style.md) — Follow standards
4. [Testing Guide](development/testing.md) — Write tests
5. [Contributing](../CONTRIBUTING.md) — Submit changes

### For Architects
1. [System Overview](architecture/overview.md) — Understand design
2. [Module Breakdown](architecture/modules.md) — Know each component
3. [Data Flow](architecture/data-flow.md) — See the flow
4. [Design Decisions](architecture/decisions.md) — Understand why
5. [Roadmap](advanced/roadmap.md) — Plan future work

---

## 💡 Key Concepts

### Audit Modules
- **System** — Check OS security configuration
- **Network** — Test network accessibility
- **SSL/TLS** — Validate certificate security
- **Filesystem** — Check file permissions
- **Secrets** — Detect exposed credentials

### Interfaces
- **CLI** — Command-line interface for manual audits
- **REST API** — HTTP API for integration
- **MCP Server** — Model Context Protocol for AI integration
- **Skills** — Claude Code integration

### Architecture
- **Engine** — Orchestrates audit execution
- **Checks** — Individual audit modules
- **Reporter** — Generates multi-format reports
- **Storage** — Persists results
- **Scheduler** — Runs audits on schedule

---

## 🆘 Getting Help

- **Questions?** Check the [FAQ](reference/faq.md)
- **Not working?** See [Troubleshooting](operations/troubleshooting.md)
- **Need to contribute?** Read [Contributing](../CONTRIBUTING.md)
- **Report bugs** on [GitHub Issues](https://github.com/yourusername/Auditoria-CS-IA/issues)

---

**Last Updated**: 2026-07-28  
**Version**: 1.0.0
