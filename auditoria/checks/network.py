"""Verificaciones de red y conectividad."""

from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import dns.resolver

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status

COMMON_PORTS: dict[int, str] = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    27017: "MongoDB",
}

RISKY_PORTS: set[int] = {21, 23, 445, 3389, 5900, 6379}


@register_check
class NetworkCheck(BaseCheck):
    name = "network"
    category = "red"
    description = "Audita resolución DNS y puertos abiertos en el objetivo"

    def run(self) -> list[Finding]:
        findings: list[Finding] = []
        findings.append(self._check_dns())
        findings.extend(self._scan_ports())
        return findings

    def _check_dns(self) -> Finding:
        try:
            answers = dns.resolver.resolve(self.target, "A")
            ips = [str(r) for r in answers]
            return Finding(
                check_id="NET-001",
                title="Resolución DNS",
                description=f"{self.target} resuelve a: {', '.join(ips)}",
                severity=Severity.INFO,
                status=Status.PASS,
                evidence={"ips": ips},
            )
        except dns.resolver.NXDOMAIN:
            return Finding(
                check_id="NET-001",
                title="Resolución DNS",
                description=f"El dominio {self.target} no existe (NXDOMAIN).",
                severity=Severity.MEDIUM,
                status=Status.WARN,
            )
        except Exception as exc:
            # localhost u otros hosts sin registro A
            try:
                ip = socket.gethostbyname(self.target)
                return Finding(
                    check_id="NET-001",
                    title="Resolución DNS",
                    description=f"{self.target} resuelve a {ip} (resolución local).",
                    severity=Severity.INFO,
                    status=Status.PASS,
                    evidence={"ip": ip},
                )
            except socket.gaierror:
                return Finding(
                    check_id="NET-001",
                    title="Resolución DNS",
                    description=f"No se pudo resolver {self.target}: {exc}",
                    severity=Severity.MEDIUM,
                    status=Status.WARN,
                )

    def _scan_ports(self) -> list[Finding]:
        ports_to_scan = self.config.get("ports", list(COMMON_PORTS.keys()))
        timeout = float(self.config.get("port_timeout", 1.0))
        open_ports: list[dict] = []

        def probe(port: int) -> tuple[int, bool]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                result = sock.connect_ex((self.target, port))
                return port, result == 0
            finally:
                sock.close()

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(probe, p): p for p in ports_to_scan}
            for future in as_completed(futures):
                port, is_open = future.result()
                if is_open:
                    open_ports.append(
                        {"port": port, "service": COMMON_PORTS.get(port, "desconocido")}
                    )

        if not open_ports:
            return [
                Finding(
                    check_id="NET-002",
                    title="Escaneo de puertos comunes",
                    description=f"No se detectaron puertos abiertos en {self.target}.",
                    severity=Severity.INFO,
                    status=Status.PASS,
                    evidence={"scanned_ports": len(ports_to_scan)},
                )
            ]

        risky = [p for p in open_ports if p["port"] in RISKY_PORTS]
        return [
            Finding(
                check_id="NET-002",
                title="Puertos abiertos detectados",
                description=f"Se encontraron {len(open_ports)} puerto(s) abierto(s).",
                severity=Severity.HIGH if risky else Severity.MEDIUM,
                status=Status.WARN if risky else Status.PASS,
                evidence={"open_ports": open_ports},
                recommendation="Cierre puertos innecesarios y restrinja el acceso con firewall.",
            )
        ]
