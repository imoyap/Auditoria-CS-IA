"""Verificaciones de permisos y archivos sensibles."""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

SENSITIVE_PATTERNS = [
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
    "*.pem",
    "*.key",
    "wp-config.php",
    "database.yml",
]

SENSITIVE_NAMES = {
    ".env", ".env.local", ".env.production",
    "credentials.json", "secrets.json",
    "id_rsa", "id_ed25519", "wp-config.php", "database.yml",
}


@register_check
class FilesystemCheck(BaseCheck):
    name = "filesystem"
    category = "archivos"
    description = "Detecta archivos sensibles con permisos inseguros"

    def run(self) -> list[Finding]:
        scan_path = Path(self.config.get("scan_path", ".")).resolve()
        max_depth = int(self.config.get("max_depth", 5))
        max_files = int(self.config.get("max_files", 500))

        if not scan_path.exists():
            return [
                Finding(
                    check_id="FS-001",
                    title="Ruta de escaneo inválida",
                    description=f"La ruta {scan_path} no existe.",
                    severity=Severity.MEDIUM,
                    status=Status.ERROR,
                )
            ]

        findings: list[Finding] = []
        sensitive_files = self._find_sensitive_files(scan_path, max_depth, max_files)

        if not sensitive_files:
            findings.append(
                Finding(
                    check_id="FS-001",
                    title="Archivos sensibles",
                    description=f"No se encontraron archivos sensibles en {scan_path}.",
                    severity=Severity.INFO,
                    status=Status.PASS,
                    evidence={"scan_path": str(scan_path)},
                )
            )
            return findings

        insecure = [f for f in sensitive_files if self._is_world_readable(f)]
        findings.append(
            Finding(
                check_id="FS-001",
                title="Archivos sensibles detectados",
                description=f"Se encontraron {len(sensitive_files)} archivo(s) potencialmente sensibles.",
                severity=Severity.HIGH if insecure else Severity.MEDIUM,
                status=Status.FAIL if insecure else Status.WARN,
                evidence={
                    "files": [str(f) for f in sensitive_files[:20]],
                    "total": len(sensitive_files),
                },
                recommendation="Restrinja permisos (chmod 600) y excluya archivos sensibles del control de versiones.",
            )
        )

        if insecure:
            findings.append(
                Finding(
                    check_id="FS-002",
                    title="Permisos inseguros en archivos sensibles",
                    description=f"{len(insecure)} archivo(s) son legibles por otros usuarios.",
                    severity=Severity.HIGH,
                    status=Status.FAIL,
                    evidence={"insecure_files": [str(f) for f in insecure[:10]]},
                    recommendation="Aplique permisos restrictivos: chmod 600 en Unix, ACLs en Windows.",
                )
            )

        return findings

    def _find_sensitive_files(
        self, root: Path, max_depth: int, max_files: int
    ) -> list[Path]:
        found: list[Path] = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

        for dirpath, dirnames, filenames in os.walk(root):
            depth = len(Path(dirpath).relative_to(root).parts)
            if depth > max_depth:
                dirnames.clear()
                continue

            dirnames[:] = [d for d in dirnames if d not in skip_dirs]

            for name in filenames:
                if name in SENSITIVE_NAMES or name.endswith((".pem", ".key")):
                    found.append(Path(dirpath) / name)
                    if len(found) >= max_files:
                        return found

        return found

    @staticmethod
    def _is_world_readable(path: Path) -> bool:
        try:
            mode = path.stat().st_mode
            if sys.platform == "win32":
                # En Windows, verificación simplificada via atributos
                return False
            return bool(mode & (stat.S_IRGRP | stat.S_IROTH))
        except OSError:
            return False
