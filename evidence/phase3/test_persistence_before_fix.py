#!/usr/bin/env python3
"""
Test: Persistence Bug Reproduction
Goal: Demonstrate that audits are NOT persisted via CLI
Status: Should FAIL before fix, PASS after fix
Date: 2026-07-28
"""

import json
import sqlite3
import subprocess
import tempfile
from pathlib import Path


def test_cli_persistence_broken():
    """
    Test that demonstrates the persistence bug.

    Scenario:
    1. Create temporary directory with temporary database
    2. Execute audit command via CLI (same way users do it)
    3. Query the database
    4. Verify that NO records were persisted

    Expected BEFORE fix: Test FAILS (0 rows, not 1)
    Expected AFTER fix: Test PASSES (1 row, audit is saved)
    """

    # Setup temporary environment
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        db_path = tmpdir_path / "test-audit.db"

        # Initialize database schema
        print(f"\n[SETUP] Creating temporary database: {db_path}")
        db = sqlite3.connect(str(db_path))

        # Create tables manually (same as DatabaseManager does)
        db.execute("""
            CREATE TABLE audits (
                id INTEGER PRIMARY KEY,
                target TEXT NOT NULL,
                started_at TIMESTAMP,
                finished_at TIMESTAMP,
                risk_score REAL,
                modules TEXT,
                total_findings INTEGER,
                critical INTEGER,
                high INTEGER,
                medium INTEGER,
                low INTEGER,
                report_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute("""
            CREATE TABLE findings (
                id INTEGER PRIMARY KEY,
                audit_id INTEGER NOT NULL,
                check_id TEXT NOT NULL,
                title TEXT,
                description TEXT,
                severity TEXT,
                status TEXT,
                recommendation TEXT,
                evidence TEXT,
                references_list TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (audit_id) REFERENCES audits(id)
            )
        """)

        db.commit()
        db.close()

        print(f"[SETUP] Database schema created")

        # Execute audit via CLI (using --db-path if available, otherwise will fail)
        print(f"\n[EXECUTE] Running: auditoria audit --modules system")

        try:
            result = subprocess.run(
                ["auditoria", "audit", "--modules", "system", "--db-path", str(db_path)],
                cwd="C:\\Users\\c4all\\Documents\\Auditoria-CS-IA",
                capture_output=True,
                text=True,
                timeout=30
            )
            print(f"[EXECUTE] Exit code: {result.returncode}")
            print(f"[EXECUTE] Output:\n{result.stdout}")
            if result.stderr:
                print(f"[EXECUTE] Stderr:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            print("[EXECUTE] Command timed out")
            raise

        # Check database for persisted data
        print(f"\n[VERIFY] Querying database...")
        db = sqlite3.connect(str(db_path))

        # Count audits
        audits_count = db.execute("SELECT COUNT(*) FROM audits").fetchone()[0]
        print(f"[VERIFY] Audits table: {audits_count} rows")

        # Count findings
        findings_count = db.execute("SELECT COUNT(*) FROM findings").fetchone()[0]
        print(f"[VERIFY] Findings table: {findings_count} rows")

        db.close()

        # Assertions
        print(f"\n[ASSERT] Checking persistence...")

        # Before fix: This will FAIL because db_path is ignored
        # After fix: This will PASS because audit is saved

        try:
            assert audits_count > 0, f"FAIL: Expected audits to be persisted, but found {audits_count} rows"
            assert findings_count > 0, f"FAIL: Expected findings to be persisted, but found {findings_count} rows"
            print(f"[ASSERT] ✅ PASS: Audit was persisted correctly")
            return True
        except AssertionError as e:
            print(f"[ASSERT] ❌ FAIL: {e}")
            return False


if __name__ == "__main__":
    print("="*60)
    print("TEST: Persistence Bug Reproduction")
    print("="*60)

    success = test_cli_persistence_broken()

    print("\n" + "="*60)
    if success:
        print("RESULT: ✅ PASS (Persistence is working)")
        exit(0)
    else:
        print("RESULT: ❌ FAIL (Persistence is BROKEN)")
        exit(1)
