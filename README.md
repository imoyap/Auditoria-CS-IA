# Auditoria-CS-IA

Framework modular de auditoría de ciberseguridad escrito en Python. Permite evaluar sistemas, redes, certificados SSL/TLS, permisos de archivos y secretos expuestos, generando informes en consola, JSON y HTML.

## Características

- **Arquitectura extensible** — Añade nuevos módulos heredando de `BaseCheck`
- **5 módulos integrados** — sistema, red, SSL/TLS, filesystem y secretos
- **Informes multi-formato** — consola (Rich), JSON y HTML
- **Puntuación de riesgo** — calculada por severidad de hallazgos
- **Multiplataforma** — Windows, Linux y macOS

## Instalación

```bash
cd Auditoria-CS-IA
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -e .
```

## Uso rápido

```bash
# Auditoría completa del sistema local
auditoria audit

# Auditar un dominio (red + SSL)
auditoria audit --target example.com --modules network ssl

# Escanear un proyecto en busca de secretos
auditoria audit --scan-path ./mi-proyecto --modules secrets filesystem

# Exportar informes
auditoria audit --output-json informe.json --output-html informe.html

# Listar módulos disponibles
auditoria list
```

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
