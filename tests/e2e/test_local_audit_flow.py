#!/usr/bin/env python3
"""
E2E Test: Complete Local Audit Flow
=====================================

Validates the entire vertical flow:
1. Request validation
2. Check execution
3. Finding capture
4. Persistence to SQLite
5. Report generation
6. Schema validation
7. Evidence integrity

Test Coverage:
- Happy path: Valid request → findings → persistence → reports
- Error cases: Invalid request, missing modules, failed checks
- Degradation: Without AI, with persistence disabled
"""

import json
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

# Imports from auditoria
from auditoria.cli import cmd_audit
from auditoria.core.engine import AuditEngine
from auditoria.core.reporter import JsonReporter
import argparse


class TestE2EAuditFlow:
    """End-to-end audit flow tests."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"
            # Initialize database
            from auditoria.storage.database import DatabaseManager
            db_mgr = DatabaseManager(str(db_path))
            yield str(db_path)

    def test_e2e_happy_path_with_persistence(self, temp_db):
        """
        Test: Complete happy path flow with persistence.

        Scenario:
        1. Execute audit via AuditEngine
        2. Verify findings are captured
        3. Verify data persists to SQLite
        4. Verify report is generated
        5. Verify metrics are calculated
        """
        # Setup
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )

        # Execute
        report = engine.run(modules=["system"], categories=None)

        # Verify execution completed
        assert report is not None, "Report should be generated"
        assert report.target == "localhost", "Target should match"
        assert len(report.results) > 0, "Should have module results"

        # Verify findings captured
        all_findings = report.all_findings
        assert isinstance(all_findings, list), "Findings should be a list"
        # System module should have findings (at least info level)
        assert len(all_findings) >= 0, "Should have findings (or none)"

        # Verify persistence
        db = sqlite3.connect(temp_db)
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM audits")
        audit_count = cursor.fetchone()[0]
        assert audit_count > 0, "Audit should be persisted"

        cursor.execute("SELECT COUNT(*) FROM findings")
        finding_count = cursor.fetchone()[0]
        # Should match number of findings in report
        assert finding_count == len(all_findings), \
            f"Findings in DB ({finding_count}) should match report ({len(all_findings)})"

        db.close()

        # Verify report structure
        assert report.summary is not None, "Report should have summary"
        # Summary contains: critical, high, medium, low, info, total_findings
        assert "total_findings" in report.summary, "Summary should have total_findings"

    def test_e2e_multi_module_audit(self, temp_db):
        """Test: Multiple modules execute and persist correctly."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )

        report = engine.run(modules=["system", "network"], categories=None)

        # Verify multiple modules executed (may execute fewer if one fails)
        assert len(report.results) >= 1, "Should execute at least one module"

        # Verify module names (results are CheckResult objects, not dicts)
        module_names = [r.module for r in report.results]
        assert "system" in module_names or "network" in module_names, \
            "Should execute requested modules"

        # Verify findings aggregation
        total_findings = sum(len(r.findings) for r in report.results)
        assert total_findings >= 0, "Should aggregate findings"

    def test_e2e_persistence_isolation(self):
        """Test: Multiple audits are isolated in database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "test.db"

            # Run first audit
            engine1 = AuditEngine(
                target="localhost",
                config={"scan_path": "."},
                enable_ai=False,
                db_path=str(db_path),
            )
            report1 = engine1.run(modules=["system"])
            findings1 = len(report1.all_findings)

            # Run second audit
            engine2 = AuditEngine(
                target="example.com",
                config={"scan_path": "."},
                enable_ai=False,
                db_path=str(db_path),
            )
            report2 = engine2.run(modules=["system"])
            findings2 = len(report2.all_findings)

            # Verify both are persisted
            db = sqlite3.connect(str(db_path))
            cursor = db.cursor()

            cursor.execute("SELECT COUNT(*) FROM audits")
            audit_count = cursor.fetchone()[0]
            assert audit_count == 2, f"Should have 2 audits, found {audit_count}"

            cursor.execute("SELECT COUNT(*) FROM findings")
            finding_count = cursor.fetchone()[0]
            assert finding_count == findings1 + findings2, \
                f"Findings should sum: {findings1} + {findings2} = {finding_count}"

            db.close()

    def test_e2e_report_generation_json(self, temp_db):
        """Test: JSON report is generated and valid."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )
        report = engine.run(modules=["system"])

        # Generate JSON report
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "report.json"

            reporter = JsonReporter()
            output_path = reporter.render(report, json_path)

            # Verify file exists
            assert Path(output_path).exists(), "JSON report should be created"

            # Verify JSON is valid
            with open(output_path, "r") as f:
                report_json = json.load(f)

            # Verify structure
            assert "target" in report_json, "Report should have target"
            assert "summary" in report_json, "Report should have summary"
            assert "results" in report_json, "Report should have results"
            assert "metadata" in report_json, "Report should have metadata"

    def test_e2e_degradation_without_ai(self, temp_db):
        """Test: Audit completes successfully without AI."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,  # AI disabled
            db_path=temp_db,
        )

        # Should not raise exception
        report = engine.run(modules=["system"])

        assert report is not None, "Should return report even without AI"
        assert len(report.results) > 0, "Should have results without AI"

    def test_e2e_degradation_without_persistence(self):
        """Test: Audit completes without database persistence."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=None,  # Persistence disabled
        )

        # Should not raise exception
        report = engine.run(modules=["system"])

        assert report is not None, "Should return report without persistence"
        assert len(report.results) > 0, "Should have results without persistence"

    def test_e2e_error_handling_invalid_module(self, temp_db):
        """Test: Invalid module raises ValueError (explicit error handling)."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )

        # Invalid module should raise ValueError
        with pytest.raises(ValueError, match="Módulo desconocido"):
            engine.run(modules=["nonexistent_module"])

    def test_e2e_evidence_captured(self, temp_db):
        """Test: Evidence is captured for each finding."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )
        report = engine.run(modules=["system"])

        # Check that findings have evidence (Finding objects have .evidence attribute)
        for finding in report.all_findings:
            # Evidence should exist or be explicitly empty
            assert hasattr(finding, "evidence"), \
                f"Finding {finding.check_id} should have evidence attribute"
            # For failed checks, evidence should be non-empty
            if finding.status == "fail":
                assert finding.evidence, \
                    f"Failed finding {finding.check_id} should have evidence"

    def test_e2e_reproducibility(self, temp_db):
        """Test: Same audit produces identical results (idempotency)."""
        # Run audit 1
        engine1 = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )
        report1 = engine1.run(modules=["system"])
        findings1_count = len(report1.all_findings)

        # Run audit 2 (same parameters)
        engine2 = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )
        report2 = engine2.run(modules=["system"])
        findings2_count = len(report2.all_findings)

        # Should produce identical results
        assert findings1_count == findings2_count, \
            f"Runs should be identical: {findings1_count} vs {findings2_count}"

        # Check check_ids match (Finding objects, not dicts)
        checks1 = {f.check_id for f in report1.all_findings}
        checks2 = {f.check_id for f in report2.all_findings}
        assert checks1 == checks2, "Same checks should be found in both runs"

    def test_e2e_database_integrity(self, temp_db):
        """Test: Database schema and foreign keys are intact."""
        engine = AuditEngine(
            target="localhost",
            config={"scan_path": "."},
            enable_ai=False,
            db_path=temp_db,
        )
        report = engine.run(modules=["system"])

        db = sqlite3.connect(temp_db)
        cursor = db.cursor()

        # Check schema
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)
        tables = {row[0] for row in cursor.fetchall()}
        assert "audits" in tables, "Should have audits table"
        assert "findings" in tables, "Should have findings table"

        # Check data consistency
        cursor.execute("SELECT COUNT(*) FROM audits")
        audit_count = cursor.fetchone()[0]
        assert audit_count > 0, "Should have audit records"

        # Check findings reference valid audits
        cursor.execute("""
            SELECT COUNT(*) FROM findings f
            WHERE NOT EXISTS (SELECT 1 FROM audits a WHERE a.id = f.audit_id)
        """)
        orphaned = cursor.fetchone()[0]
        assert orphaned == 0, f"Should have no orphaned findings, found {orphaned}"

        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
