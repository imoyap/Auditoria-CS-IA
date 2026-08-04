# Skill: audit-status

Check the status and history of scheduled audit tasks.

## Trigger
Use this skill when the user wants to see what audits are scheduled, when they last ran, or their execution status.

## Usage
```
/audit-status [--task TASK_NAME] [--history] [--target TARGET]
```

## Examples
```
/audit-status --list
/audit-status --task daily-prod-audit
/audit-status --task daily-prod-audit --history --limit 5
/audit-status --target example.com --history
```

## Parameters
- `--list` (optional): List all scheduled tasks
- `--task` (optional): Show status of specific task
- `--history` (optional): Show execution history
- `--target` (optional): Filter audits by target
- `--limit` (optional): Limit history entries (default: 10)

## What it does
1. Connects to scheduler database
2. Queries task status and execution history
3. Displays formatted table with Rich
4. Shows last execution, next scheduled time, and any errors
5. Optionally displays AI analyses from recent audits

## Integration
Uses `AuditScheduler` and `DatabaseManager` for data retrieval.
