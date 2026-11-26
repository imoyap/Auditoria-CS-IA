# Auditoria-CS-IA

## Qué es
Herramienta de auditoría de ciberseguridad asistida por IA (paquete Python `auditoria-cs` v1.0.0, CLI `auditoria`).
Audita sistema, red/DNS/puertos, certificados SSL/TLS, permisos de archivos y secretos en código (módulos que heredan de `BaseCheck`), usa Claude API para analizar hallazgos y entrega informes JSON/HTML/Markdown/consola con puntuación de riesgo. Incluye API REST (Flask), servidor MCP y persistencia SQLite.

## Entorno
- SO: Windows, shell PowerShell. Ruta: C:\Auditoria-CS-IA
- Python 3.12, instalado en modo editable (`pip install -e .` vía `make install`)
- Docker Desktop (WSL2) con Compose v5; se usa `docker compose` (no `docker-compose`, aunque el README lo diga)
- `make` instalado con winget (ezwinports.make)

## Estructura
- `auditoria/cli.py` CLI · `auditoria/core/` motor, modelos, reporter · `auditoria/checks/` módulos (registrar en `checks/__init__.py`) · `auditoria/templates/` plantillas Jinja2
- `scripts/run_api.py` servidor API · `tests/` pytest (`test_auditoria.py`, `e2e/`) · `specs/` roadmap v2.0 · `docs/`

## Git
- Rama de trabajo: `u3-pipeline-agentico` (sigue a `team/u3-pipeline-agentico`).
- Remotos: `origin` = imoyap/Auditoria-CS-IA (fork propio, con escritura); `team` = mcarreral/Auditoria-CS-IA (equipo, sin escritura: cambios vía PR); `upstream` = cherrera0001/Auditoria-CS-IA (original).
- No hacer push sin pedirlo (además está bloqueado en settings.json).

## Pipeline agéntico U3 (rama `u3-pipeline-agentico`)
Actividad de Cierre de la Unidad 3 (Diplomado en Ciberseguridad). Es independiente del framework `auditoria/` y no lo importa.
- Workflow de 10 etapas con gates `gates/G0.md`–`G5.md`; G0, G3 y G5 requieren firma humana real. Nunca firmar un gate en nombre del usuario.
- Roles = subagentes en `.claude/agents/` (recon, analista, verificador, compliance, redactor, contradictor). Solo RECON usa Bash; los demás escriben únicamente vía skills de `.claude/skills/`.
- Orquestador: `harness/orquestador.py` (WIP=1, máx. 30 iteraciones, `--sign-gate`/`--continue`); controles CT-01–07 en `harness/controles/`.
- Alcance: `scope/alcance.yaml` + `scope/allowlist.txt`. No ejecutar nada fuera de la allowlist.
- Datos: `evidencias/` (crudo con hash) → `normalizado/` → `reporte/`. Bitácora append-only en `LEDGER.md` (no reescribir entradas).
- MCP: `.mcp.json` (`mcp/conocimiento_tecnico`, `mcp/conocimiento_normativo`). Requieren `pip install "mcp<2"` (usan `mcp.server.fastmcp`, eliminado en mcp 2.x). La carpeta local `mcp/` tapa al paquete si se ejecuta `python -c` desde la raíz.
- Diseño/estado: `docs/requirements.md`, `docs/design.md`, `docs/tasks.md`; comandos PowerShell en `docs/COMANDOS_VIDEO_POWERSHELL.md`.

## Dependencias principales
cryptography, dnspython, jinja2 (informes), rich (salida de consola), requests, anthropic (SDK). Extras: `dev` (pytest, pytest-cov), `api` (flask).

## Comandos (Makefile)
- Instalar: `make install` · con extras dev+api: `make dev`
- Tests: `make test` (pytest tests/, requiere `make dev`; 14 tests) · cobertura: `make test-cov` (→ htmlcov/index.html)
- Test del pipeline U3 (script propio, no pytest): `python .claude/skills/clasificar/scripts/test_calcular_riesgo.py`
- Lint: `make lint` (flake8 + mypy) · Formato: `make format` (black + isort) — estas herramientas NO están en los extras `dev`; instalarlas aparte
- Ejecutar CLI: `make run` (= `auditoria audit --target localhost`); ej. `auditoria audit --target example.com --modules network ssl`
- API local: `make api` (= `python scripts/run_api.py`, puerto 5000)
- `make clean` usa `rm`/`find` de Unix y BORRA `data/audit-results`, `data/reports`, `data/logs`: no ejecutarlo sin confirmación
- Servicios: `docker compose up -d` · `docker compose ps` · `docker compose logs -f`
  (api:5000, postgres:5432, prometheus:9090, grafana:3000, redis:6379)

## Configuración y secretos
- La clave `ANTHROPIC_API_KEY` va en `.env` (ignorado por git) o como variable de entorno. NUNCA escribirla en código, logs, ejemplos ni commits.
- Otras variables del compose: `DB_PASSWORD`, `GRAFANA_PASSWORD` (tienen valores por defecto de desarrollo).
- No leer ni mostrar el contenido de `.env`.
- `.env` debe estar en `.gitignore`.

## Pendientes conocidos
1. Falta `.env.example` (solo nombres: `ANTHROPIC_API_KEY`, `DB_PASSWORD`, `GRAFANA_PASSWORD`); las reglas deny impiden a Claude crearlo.
4. `docker-compose.yml` construye `docker/Dockerfile`, que no existe en el repo: el servicio `api` no puede arrancar.
5. `docker-compose.yml` monta `config/prometheus.yml`, que no existe (solo hay `config/README.md`).
6. Imágenes `prom/prometheus` y `grafana/grafana` en `:latest`; fijar versiones.
7. `make clean` no funciona en PowerShell/cmd (comandos Unix).## Convenciones
- Responder y documentar en español; identificadores de código en inglés o como ya esté en el repo.
- Antes de cambios grandes, mostrar el plan y esperar confirmación.
- Esta herramienta puede tratar evidencia de clientes (`evidence/`, `data/`): no enviar datos reales a servicios externos ni registrarlos en logs sin enmascarar.
