"""Verificaciones del sistema operativo y configuración de seguridad."""

from __future__ import annotations

import os
import platform
import subprocess
import sys

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status


@register_check
class SystemCheck(BaseCheck):
    name = "system"
    category = "sistema"
    description = "Audita configuración básica del sistema operativo"

    def run(self) -> list[Finding]:
        findings: list[Finding] = []
        findings.append(self._check_os_updates())
        findings.append(self._check_admin_privileges())
        if sys.platform == "win32":
            findings.extend(self._check_windows_security())
        else:
            findings.extend(self._check_unix_security())
        return findings

    def _check_os_updates(self) -> Finding:
        os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
        return Finding(
            check_id="SYS-001",
            title="Información del sistema operativo",
            description=f"Sistema detectado: {os_info}",
            severity=Severity.INFO,
            status=Status.PASS,
            evidence={"os": os_info, "architecture": platform.machine()},
            recommendation="Mantenga el sistema operativo actualizado con parches de seguridad.",
        )

    def _check_admin_privileges(self) -> Finding:
        is_admin = self._running_as_admin()
        if is_admin:
            return Finding(
                check_id="SYS-002",
                title="Ejecución con privilegios elevados",
                description="La auditoría se ejecuta con privilegios de administrador.",
                severity=Severity.MEDIUM,
                status=Status.WARN,
                recommendation="Ejecute auditorías con una cuenta de usuario estándar cuando sea posible.",
            )
        return Finding(
            check_id="SYS-002",
            title="Privilegios de ejecución",
            description="La auditoría se ejecuta sin privilegios de administrador.",
            severity=Severity.INFO,
            status=Status.PASS,
        )

    def _check_windows_security(self) -> list[Finding]:
        findings: list[Finding] = []

        # Firewall
        fw_result = self._run_cmd(
            ["netsh", "advfirewall", "show", "allprofiles", "state"]
        )
        fw_enabled = "ON" in (fw_result or "").upper()
        findings.append(
            Finding(
                check_id="SYS-003",
                title="Estado del Firewall de Windows",
                description="Firewall activo en todos los perfiles"
                if fw_enabled
                else "El firewall de Windows no está activo en todos los perfiles.",
                severity=Severity.HIGH if not fw_enabled else Severity.INFO,
                status=Status.PASS if fw_enabled else Status.FAIL,
                evidence={"firewall_output": (fw_result or "")[:500]},
                recommendation="Active el Firewall de Windows en perfiles Dominio, Privado y Público.",
                references=["https://learn.microsoft.com/windows/security/operating-system-security/network-security/windows-firewall/"],
            )
        )

        # Windows Defender
        defender = self._run_cmd(
            ["powershell", "-NoProfile", "-Command",
             "Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled | ConvertTo-Json"]
        )
        defender_active = defender and "true" in defender.lower()
        findings.append(
            Finding(
                check_id="SYS-004",
                title="Protección antivirus (Windows Defender)",
                description="Windows Defender con protección en tiempo real activa"
                if defender_active
                else "Antivirus o protección en tiempo real desactivada.",
                severity=Severity.HIGH if not defender_active else Severity.INFO,
                status=Status.PASS if defender_active else Status.FAIL,
                evidence={"defender_status": (defender or "no disponible")[:500]},
                recommendation="Active Windows Defender y la protección en tiempo real.",
            )
        )

        return findings

    def _check_unix_security(self) -> list[Finding]:
        findings: list[Finding] = []

        # Umask
        umask = os.umask(0o022)
        os.umask(umask)
        umask_str = oct(umask)
        insecure = umask < 0o022
        findings.append(
            Finding(
                check_id="SYS-003",
                title="Umask del sistema",
                description=f"Umask actual: {umask_str}",
                severity=Severity.MEDIUM if insecure else Severity.INFO,
                status=Status.WARN if insecure else Status.PASS,
                evidence={"umask": umask_str},
                recommendation="Configure umask 022 o más restrictivo (027/077).",
            )
        )

        return findings

    @staticmethod
    def _running_as_admin() -> bool:
        if sys.platform == "win32":
            try:
                import ctypes
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            except Exception:
                return False
        return os.geteuid() == 0

    @staticmethod
    def _run_cmd(cmd: list[str]) -> str | None:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            return result.stdout + result.stderr
        except Exception:
            return None
