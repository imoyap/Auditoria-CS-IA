# Configuration

Configuration files and templates for Auditoria.

## Files

### `development.env.example`
Template for development environment.

Copy and customize:
```bash
cp development.env.example .env.local
```

### `production.env.example`
Template for production environment.

### `logging.yaml`
Logging configuration.

Defines:
- Log levels
- Output formats
- File rotation
- Handler configuration

### `prometheus.yml`
Prometheus monitoring configuration.

Defines:
- Metrics scrape intervals
- Alert rules
- Target endpoints

### `kubernetes/`
Kubernetes deployment manifests.

Contains:
- `deployment.yaml` — Deployment configuration
- `service.yaml` — Service definition
- `configmap.yaml` — ConfigMap for configuration

## Environment Variables

### Required
- `ANTHROPIC_API_KEY` — API key for Claude

### Optional
- `AUDITORIA_DB_PATH` — Database path (default: auditoria.db)
- `AUDITORIA_API_PORT` — API port (default: 5000)
- `LOG_LEVEL` — Logging level (default: INFO)

## Docker Configuration

See `docker-compose.yml` in root for containerized setup.

Brings up:
- API service
- PostgreSQL database
- Prometheus
- Grafana
- Redis (optional)

```bash
docker-compose up -d
```

## Customization

1. Copy example file
2. Edit with your settings
3. Load when running application

Example:
```bash
# In .env file
AUDITORIA_DB_PATH=/var/lib/auditoria/auditoria.db
AUDITORIA_API_PORT=8000
```

Then:
```bash
source .env
python scripts/run_api.py
```

See documentation for configuration details.
