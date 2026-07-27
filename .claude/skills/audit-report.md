# Skill: audit-report

Generate and export detailed audit reports.

## Trigger
Use when the user wants to create comprehensive reports, export findings, or share audit results.

## Usage
```
/audit-report <audit_id> [--format FORMAT] [--ai-insights] [--export PATH]
```

## Examples
```
/audit-report 1
/audit-report 1 --format html --export /tmp/report.html
/audit-report 1 --ai-insights --format json
/audit-report 1 --format pdf --ai-insights
```

## Parameters
- `audit_id` (required): ID of the audit to report on
- `--format` (optional): Output format (console, json, html, pdf) default: console
- `--ai-insights` (optional): Include AI analysis and recommendations
- `--export` (optional): Export to file path
- `--include-evidence` (optional): Include detailed evidence in report

## What it does
1. Retrieves complete audit from database
2. Fetches all findings and AI analyses
3. Generates formatted report (console/JSON/HTML/PDF)
4. Includes:
   - Risk score and summary
   - Findings by severity
   - AI-generated remediation plans
   - Trends and pattern analysis
   - Executive summary for stakeholders
5. Optionally exports to file

## Report Sections
- Executive Summary (AI-generated for stakeholders)
- Risk Assessment
- Findings by Module
- Remediation Priority Plan
- Pattern Analysis
- Compliance References
- Timeline Recommendations

## Integration
Uses:
- DatabaseManager for audit retrieval
- AuditAnalyzer for AI-enhanced insights
- HtmlReporter/JsonReporter for export formats
