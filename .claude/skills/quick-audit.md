# Skill: quick-audit

Ejecuta una auditoría rápida de seguridad sobre un objetivo.

## Trigger
Use this skill when the user wants to quickly audit a system, network, or application for security issues.

## Usage
```
/quick-audit <target> [--modules MODULE1 MODULE2] [--ai]
```

## Examples
```
/quick-audit localhost --ai
/quick-audit example.com --modules network ssl --ai
/quick-audit /path/to/project --modules secrets filesystem
```

## Parameters
- `target` (required): Objective to audit (hostname, IP, domain, or path)
- `--modules` (optional): Specific modules to run (system, network, ssl, filesystem, secrets)
- `--ai` (optional): Include AI analysis of findings
- `--json` (optional): Output as JSON

## What it does
1. Validates target and configuration
2. Executes audit engine with specified modules
3. Optionally enriches findings with AI analysis
4. Displays results in console with Rich formatting
5. Returns exit code based on severity (0=safe, 1=high findings, 2=critical)

## Integration
This skill uses the core `AuditEngine` and optionally `AuditAnalyzer` for intelligent insights.
