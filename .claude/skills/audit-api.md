# Skill: audit-api

Start and manage the Auditoria REST API server.

## Trigger
Use when the user wants to start the API server, configure webhooks, or access audits via REST.

## Usage
```
/audit-api [start|stop|status] [--host HOST] [--port PORT] [--debug]
```

## Examples
```
/audit-api start
/audit-api start --port 8000 --debug
/audit-api status
/audit-api stop
```

## Parameters
- `start` (default): Start API server
- `stop`: Stop running API server
- `status`: Show API server status
- `--host` (optional): Host to bind to (default: 0.0.0.0)
- `--port` (optional): Port to listen on (default: 5000)
- `--debug` (optional): Enable debug mode

## Endpoints Available
Once running:
- `POST /api/v1/audits` - Execute audit
- `GET /api/v1/audits` - List audits
- `POST /api/v1/webhooks` - Register webhook
- `POST /api/v1/tasks` - Create scheduled task
- Full REST API documented in API.md

## What it does
1. Validates port availability
2. Initializes Flask app with all routes
3. Connects to SQLite database
4. Loads scheduler and webhook manager
5. Provides API for external integrations

## Integration
Launches server from `auditoria/api/server.py` with full integration to:
- DatabaseManager (audit persistence)
- AuditScheduler (task management)
- WebhookManager (notifications)
- AuditEngine + AuditAnalyzer (execution)
