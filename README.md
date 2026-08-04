# Auditoria-CS-IA

🔒 **Plataforma autónoma de auditoría asistida por IA**

Framework modular de auditoría de ciberseguridad y conformidad escrito en Python. Automatiza análisis de seguridad en sistemas, redes, certificados SSL/TLS, permisos de archivos y secretos usando Claude API como motor de análisis inteligente.

## 🚀 Características

### Core
- **Auditoría Autónoma** — Ejecución programada sin intervención manual
- **IA Integrada** — Análisis inteligente con Claude API
- **Arquitectura Extensible** — Añade nuevos módulos heredando de `BaseCheck`
- **5 módulos integrados** — sistema, red, SSL/TLS, filesystem y secretos

### API & Integración
- **REST API** — 18 endpoints para control y webhooks
- **MCP Server** — 9 herramientas para integración con Claude
- **Claude Code Skills** — Integración nativa con herramientas de Claude

### Almacenamiento & Reportes
- **SQLite Persistencia** — Histórico completo de auditorías
- **Reportes Multi-formato** — JSON, HTML, Markdown y consola (Rich)
- **Puntuación de Riesgo** — Calculada por severidad de hallazgos
- **Trazabilidad Completa** — Cada hallazgo con timestamp y metadata

### DevOps
- **Docker & Compose** — Stack local con PostgreSQL, Prometheus, Grafana
- **Kubernetes Ready** — Manifests para producción
- **Monitoreo** — Integración con Prometheus + Grafana
- **CI/CD** — GitHub Actions scaffolding

## 📦 Stack Técnico

- **Python 3.10+** — Flask, APScheduler, SQLAlchemy
- **Claude API** — Análisis inteligente y procesamiento de hallazgos
- **Base de Datos** — SQLite (dev) / PostgreSQL (prod)
- **Contenedores** — Docker & Kubernetes
- **Monitoreo** — Prometheus + Grafana
- **CI/CD** — GitHub Actions

## ⚡ Inicio Rápido

```bash
# Clonar
git clone https://github.com/cherrera0001/Auditoria-CS-IA.git
cd Auditoria-CS-IA

# Instalar
make install

# Ejecutar
docker-compose up -d

# Ver documentación
cat docs/README.md
```

## 📚 Documentación

```
docs/
├── guides/              → Guías de usuario
├── architecture/        → Diseño técnico
├── operations/          → Deployment y monitoreo
├── development/         → Setup para desarrolladores
├── advanced/            → Temas avanzados
└── reference/           → Especificaciones y FAQs
```

Documentación completa en `docs/README.md`

## 💻 Uso

### CLI
```bash
# Auditoría completa
auditoria audit

# Auditar dominio
auditoria audit --target example.com --modules network ssl

# Buscar secretos
auditoria audit --scan-path ./proyecto --modules secrets

# Exportar informes
auditoria audit --output-json report.json --output-html report.html
```

### REST API
```bash
# Iniciar servidor
python scripts/run_api.py --port 5000

# Ejecutar auditoría
curl -X POST http://localhost:5000/api/audit \
  -H "Content-Type: application/json" \
  -d '{"modules": ["system", "network"]}'
```

### MCP Integration
```python
from auditoria.mcp.server import MCPAuditServer

server = MCPAuditServer()
await server.start()
```

## 🧩 Módulos de Auditoría

| Módulo       | Categoría | Descripción |
|-------------|-----------|------------|
| `system`    | sistema   | Firewall, antivirus, privilegios, SO |
| `network`   | red       | DNS, puertos, conectividad |
| `ssl`       | cifrado   | Certificados, TLS, expiración |
| `filesystem`| archivos  | Permisos inseguros, archivos sensibles |
| `secrets`   | secretos  | Credenciales en código, tokens |

## 🔧 Crear Módulo Personalizado

```python
from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity

@register_check
class MiCheck(BaseCheck):
    name = "mi-check"
    category = "custom"
    description = "Mi verificación"

    def run(self) -> list[Finding]:
        return [Finding(...)]
```

Registra en `auditoria/checks/__init__.py`

## Módulos de auditoría

| Módulo       | Categoría | Descripción                                      |
|-------------|-----------|--------------------------------------------------|
| `system`    | sistema   | Firewall, antivirus, privilegios, info del SO    |
| `network`   | red       | DNS, escaneo de puertos comunes                  |
| `ssl`       | cifrado   | Certificados, expiración, protocolos TLS         |
| `filesystem`| archivos  | Archivos sensibles con permisos inseguros        |
| `secrets`   | secretos  | Detección de credenciales en código fuente       |

## Crear un módulo personalizado

```python
from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

@register_check
class MiCheck(BaseCheck):
    name = "mi-check"
    category = "custom"
    description = "Mi verificación personalizada"

    def run(self) -> list[Finding]:
        return [
            Finding(
                check_id="CUSTOM-001",
                title="Ejemplo",
                description="Descripción del hallazgo",
                severity=Severity.MEDIUM,
                status=Status.WARN,
                recommendation="Acción recomendada",
            )
        ]
```

Importa el módulo en `auditoria/checks/__init__.py` para registrarlo.

## Estructura del proyecto

```
Auditoria-CS-IA/
├── auditoria/
│   ├── cli.py              # Interfaz de línea de comandos
│   ├── core/
│   │   ├── engine.py       # Motor de ejecución
│   │   ├── models.py       # Modelos de datos
│   │   └── reporter.py     # Generadores de informes
│   ├── checks/
│   │   ├── base.py         # Clase base BaseCheck
│   │   ├── registry.py     # Registro de módulos
│   │   ├── system.py
│   │   ├── network.py
│   │   ├── ssl_tls.py
│   │   ├── filesystem.py
│   │   └── secrets.py
│   └── templates/
│       └── report.html
├── tests/
├── pyproject.toml
└── requirements.txt
```

## Códigos de salida

| Código | Significado                          |
|--------|--------------------------------------|
| 0      | Sin hallazgos críticos ni altos      |
| 1      | Hallazgos de severidad alta          |
| 2      | Hallazgos de severidad crítica       |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Licencia

MIT
