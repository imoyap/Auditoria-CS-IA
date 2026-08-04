"""Verificaciones de certificados SSL/TLS."""

from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone

from auditoria.checks.base import BaseCheck
from auditoria.checks.registry import register_check
from auditoria.core.models import Finding, Severity, Status


@register_check
class SslTlsCheck(BaseCheck):
    name = "ssl"
    category = "cifrado"
    description = "Audita certificados SSL/TLS del objetivo HTTPS"

    def run(self) -> list[Finding]:
        host = self.target
        port = int(self.config.get("ssl_port", 443))

        # Solo auditar si parece un host remoto o se fuerza HTTPS
        if host in ("localhost", "127.0.0.1") and not self.config.get("force_ssl"):
            return [
                Finding(
                    check_id="SSL-001",
                    title="Auditoría SSL/TLS omitida",
                    description="Use --target con un dominio HTTPS o configure force_ssl.",
                    severity=Severity.INFO,
                    status=Status.SKIP,
                )
            ]

        return self._audit_certificate(host, port)

    def _audit_certificate(self, host: str, port: int) -> list[Finding]:
        findings: list[Finding] = []

        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    protocol = ssock.version()
        except ssl.SSLCertVerificationError as exc:
            return [
                Finding(
                    check_id="SSL-001",
                    title="Certificado SSL inválido",
                    description=str(exc),
                    severity=Severity.CRITICAL,
                    status=Status.FAIL,
                    recommendation="Instale un certificado válido de una CA confiable.",
                    references=["https://www.ssl.com/guide/what-is-an-ssl-certificate/"],
                )
            ]
        except Exception as exc:
            return [
                Finding(
                    check_id="SSL-001",
                    title="Conexión SSL/TLS fallida",
                    description=f"No se pudo conectar a {host}:{port} — {exc}",
                    severity=Severity.MEDIUM,
                    status=Status.WARN,
                )
            ]

        # Expiración
        not_after = cert.get("notAfter")
        if not_after:
            expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc
            )
            days_left = (expiry - datetime.now(timezone.utc)).days
            if days_left < 0:
                findings.append(
                    Finding(
                        check_id="SSL-002",
                        title="Certificado expirado",
                        description=f"El certificado expiró hace {abs(days_left)} días.",
                        severity=Severity.CRITICAL,
                        status=Status.FAIL,
                        evidence={"expiry": not_after, "days_left": days_left},
                        recommendation="Renueve el certificado inmediatamente.",
                    )
                )
            elif days_left < 30:
                findings.append(
                    Finding(
                        check_id="SSL-002",
                        title="Certificado próximo a expirar",
                        description=f"El certificado expira en {days_left} días.",
                        severity=Severity.HIGH,
                        status=Status.WARN,
                        evidence={"expiry": not_after, "days_left": days_left},
                        recommendation="Programe la renovación del certificado.",
                    )
                )
            else:
                findings.append(
                    Finding(
                        check_id="SSL-002",
                        title="Validez del certificado",
                        description=f"Certificado válido por {days_left} días más.",
                        severity=Severity.INFO,
                        status=Status.PASS,
                        evidence={"expiry": not_after, "days_left": days_left},
                    )
                )

        # Protocolo TLS
        if protocol and protocol in ("TLSv1", "TLSv1.1", "SSLv3", "SSLv2"):
            findings.append(
                Finding(
                    check_id="SSL-003",
                    title="Protocolo TLS obsoleto",
                    description=f"Se negoció {protocol}, considerado inseguro.",
                    severity=Severity.HIGH,
                    status=Status.FAIL,
                    evidence={"protocol": protocol},
                    recommendation="Deshabilite TLS 1.0/1.1 y use TLS 1.2 o superior.",
                    references=["https://datatracker.ietf.org/doc/rfc8996/"],
                )
            )
        else:
            findings.append(
                Finding(
                    check_id="SSL-003",
                    title="Protocolo TLS",
                    description=f"Protocolo negociado: {protocol}",
                    severity=Severity.INFO,
                    status=Status.PASS,
                    evidence={"protocol": protocol},
                )
            )

        # Información del emisor
        issuer = dict(x[0] for x in cert.get("issuer", []))
        subject = dict(x[0] for x in cert.get("subject", []))
        findings.append(
            Finding(
                check_id="SSL-004",
                title="Información del certificado",
                description=f"Emitido por {issuer.get('organizationName', 'desconocido')} "
                f"para {subject.get('commonName', host)}",
                severity=Severity.INFO,
                status=Status.PASS,
                evidence={"issuer": issuer, "subject": subject},
            )
        )

        return findings
