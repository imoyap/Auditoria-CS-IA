# Scripts

Utility scripts for running and managing Auditoria.

## Available Scripts

### `run_api.py`
Start the REST API server.

```bash
python scripts/run_api.py --port 5000 --debug
```

**Options:**
- `--host` — Host to bind to (default: 0.0.0.0)
- `--port` — Port to listen on (default: 5000)
- `--debug` — Enable debug mode
- `--db-path` — Path to database
- `--webhooks-path` — Path to webhooks config

### `test_deployment.py`
Validate local deployment.

```bash
python scripts/test_deployment.py
```

Verifies:
- All modules importable
- Database initializable
- API creatable
- Scheduler functional
- Audits executable

### `deploy.sh` (Linux/macOS)
Deploy to production.

```bash
./scripts/deploy.sh --env production --version 1.0.0
```

### `health-check.sh`
Check system health.

```bash
./scripts/health-check.sh
```

Checks:
- API server running
- Database accessible
- Webhooks functional

### `backup.sh`
Backup database and data.

```bash
./scripts/backup.sh /backups/
```

### `restore.sh`
Restore from backup.

```bash
./scripts/restore.sh /backups/2026-07-28_backup.tar.gz
```

## Adding New Scripts

1. Create script in `scripts/`
2. Use appropriate extension (`.py`, `.sh`)
3. Add documentation above
4. Make executable: `chmod +x script.sh`
5. Update this README

## Common Tasks (via Makefile)

Instead of scripts, use Makefile for common tasks:

```bash
make test          # Run tests
make lint          # Check code style
make format        # Format code
make api           # Start API server
make clean         # Remove artifacts
```

See `Makefile` for all available tasks.
