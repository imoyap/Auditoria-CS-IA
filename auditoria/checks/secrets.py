"""Detección de secretos y credenciales expuestas."""

from __future__ import annotations

import os
import re
from pathlib import Path

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

SECRET_PATTERNS: list[tuple[str, re.Pattern[str], Severity]] = [
    (
        "AWS Access Key",
        re.compile(r"AKIA[0-9A-Z]{16}"),
        Severity.CRITICAL,
    ),
    (
        "GitHub Token",
        re.compile(r"ghp_[A-Za-z0-9]{36,}"),
        Severity.CRITICAL,
    ),
    (
        "Generic API Key",
        re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
        Severity.HIGH,
    ),
    (
        "Password in config",
        re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{4,}['\"]"),
        Severity.HIGH,
    ),
    (
        "Private Key header",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        Severity.CRITICAL,
    ),
    (
        "JWT Token",
        re.compile(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
        Severity.HIGH,
    ),
    (
        "Connection string with password",
        re.compile(r"(?i)(mongodb|mysql|postgres|redis)://[^:\s]+:[^@\s]+@"),
        Severity.HIGH,
    ),
]

SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml",
    ".env", ".cfg", ".ini", ".toml", ".xml", ".sh", ".ps1", ".bat",
    ".md", ".txt", ".html", ".css",
}


@register_check
class SecretsCheck(BaseCheck):
    name = "secrets"
    category = "secretos"
    description = "Busca credenciales y secretos expuestos en el código"

    def run(self) -> list[Finding]:
        scan_path = Path(self.config.get("scan_path", ".")).resolve()
        max_files = int(self.config.get("max_files", 300))

        if not scan_path.exists():
            return [
                Finding(
                    check_id="SEC-001",
                    title="Ruta de escaneo inválida",
                    description=f"La ruta {scan_path} no existe.",
                    severity=Severity.MEDIUM,
                    status=Status.ERROR,
                )
            ]

        matches = self._scan_for_secrets(scan_path, max_files)

        if not matches:
            return [
                Finding(
                    check_id="SEC-001",
                    title="Escaneo de secretos",
                    description=f"No se detectaron patrones de secretos en {scan_path}.",
                    severity=Severity.INFO,
                    status=Status.PASS,
                    evidence={"scan_path": str(scan_path)},
                    recommendation="Integre herramientas como git-secrets o gitleaks en CI/CD.",
                )
            ]

        critical = [m for m in matches if m["severity"] == Severity.CRITICAL.value]
        return [
            Finding(
                check_id="SEC-001",
                title="Posibles secretos expuestos",
                description=f"Se detectaron {len(matches)} coincidencia(s) de patrones sensibles.",
                severity=Severity.CRITICAL if critical else Severity.HIGH,
                status=Status.FAIL,
                evidence={"matches": matches[:15], "total": len(matches)},
                recommendation="Revoke las credenciales, rote los secretos y use un gestor de secretos.",
                references=[
                    "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/",
                ],
            )
        ]

    def _scan_for_secrets(
        self, root: Path, max_files: int
    ) -> list[dict]:
        matches: list[dict] = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
        scanned = 0

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            for name in filenames:
                path = Path(dirpath) / name
                if path.suffix.lower() not in SCAN_EXTENSIONS and name != ".env":
                    continue

                scanned += 1
                if scanned > max_files:
                    return matches

                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue

                for label, pattern, severity in SECRET_PATTERNS:
                    for match in pattern.finditer(content):
                        # Evitar falsos positivos en archivos de ejemplo
                        if self._is_likely_placeholder(match.group()):
                            continue
                        line_num = content[: match.start()].count("\n") + 1
                        matches.append(
                            {
                                "type": label,
                                "file": str(path.relative_to(root)),
                                "line": line_num,
                                "severity": severity.value,
                                "preview": self._redact(match.group()),
                            }
                        )

        return matches

    @staticmethod
    def _is_likely_placeholder(value: str) -> bool:
        placeholders = {
            "your_api_key", "example", "placeholder", "changeme",
            "xxx", "todo", "fake", "test", "dummy", "sample",
        }
        lower = value.lower()
        return any(p in lower for p in placeholders)

    @staticmethod
    def _redact(value: str) -> str:
        if len(value) <= 8:
            return "***"
        return value[:4] + "***" + value[-4:]
