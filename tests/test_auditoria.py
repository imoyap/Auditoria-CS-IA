"""Tests del framework de auditoría."""

from auditoria.core.models import AuditReport, Finding, Severity, Status


def test_finding_to_dict():
    finding = Finding(
        check_id="TEST-001",
        title="Test",
        description="Descripción",
        severity=Severity.HIGH,
        status=Status.FAIL,
    )
    data = finding.to_dict()
    assert data["severity"] == "high"
    assert data["status"] == "fail"


def test_audit_report_risk_score():
    report = AuditReport.create(target="localhost")
    report.results.append(
        __import__("auditoria.core.models", fromlist=["CheckResult"]).CheckResult(
            module="test",
            category="test",
            findings=[
                Finding("T-1", "A", "desc", Severity.CRITICAL, Status.FAIL),
                Finding("T-2", "B", "desc", Severity.LOW, Status.WARN),
            ],
        )
    )
    assert report.risk_score > 0
    assert report.summary["total_findings"] == 2


def test_registry_lists_checks():
    from auditoria.checks.registry import get_checks, list_available_checks

    checks = get_checks()
    assert "system" in checks
    assert "network" in checks
    assert len(list_available_checks()) >= 5


def test_system_check_runs():
    from auditoria.checks.system import SystemCheck

    check = SystemCheck(target="localhost")
    findings = check.run()
    assert len(findings) >= 1
    assert any(f.check_id == "SYS-001" for f in findings)
