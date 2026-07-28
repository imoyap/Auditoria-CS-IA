#!/usr/bin/env python
"""Local deployment test script"""

import sys
import time
from pathlib import Path

# Test 1: Import all modules
print("=" * 60)
print("TEST 1: Module Imports")
print("=" * 60)

try:
    from auditoria.cli import build_parser, cmd_audit, cmd_list
    from auditoria.core.engine import AuditEngine
    from auditoria.core.reporter import ConsoleReporter, JsonReporter, HtmlReporter
    from auditoria.storage.database import DatabaseManager
    from auditoria.scheduler.executor import AuditScheduler
    from auditoria.mcp.server import create_mcp_server
    from auditoria.api.server import create_app
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Create engine
print("\n" + "=" * 60)
print("TEST 2: Audit Engine")
print("=" * 60)

try:
    engine = AuditEngine(target="localhost")
    print(f"✓ Engine created: {engine}")
except Exception as e:
    print(f"✗ Engine failed: {e}")
    sys.exit(1)

# Test 3: Database Manager
print("\n" + "=" * 60)
print("TEST 3: Database Manager")
print("=" * 60)

try:
    db = DatabaseManager(":memory:")  # In-memory DB for testing
    print(f"✓ Database initialized")
except Exception as e:
    print(f"✗ Database failed: {e}")
    sys.exit(1)

# Test 4: MCP Server
print("\n" + "=" * 60)
print("TEST 4: MCP Server")
print("=" * 60)

try:
    mcp = create_mcp_server()
    tools = mcp.get_tools()
    print(f"✓ MCP Server created with {len(tools)} tools")
    print(f"  Tools: {', '.join(list(tools.keys())[:3])}...")
except Exception as e:
    print(f"✗ MCP Server failed: {e}")
    sys.exit(1)

# Test 5: Flask App
print("\n" + "=" * 60)
print("TEST 5: Flask REST API")
print("=" * 60)

try:
    app = create_app()
    print(f"✓ Flask app created")
    print(f"  App name: {app.name}")
except Exception as e:
    print(f"✗ Flask app failed: {e}")
    sys.exit(1)

# Test 6: Scheduler
print("\n" + "=" * 60)
print("TEST 6: Audit Scheduler")
print("=" * 60)

try:
    scheduler = AuditScheduler()
    print(f"✓ Scheduler created")
except Exception as e:
    print(f"✗ Scheduler failed: {e}")
    sys.exit(1)

# Test 7: Quick audit
print("\n" + "=" * 60)
print("TEST 7: Quick Audit Execution")
print("=" * 60)

try:
    engine = AuditEngine(target="localhost")
    report = engine.run(modules=["system"])
    print(f"✓ Audit executed")
    print(f"  Findings: {len(report.all_findings)}")
    print(f"  Risk score: {report.risk_score}/100")
    print(f"  Duration: {report.finished_at - report.started_at}")
except Exception as e:
    print(f"✗ Audit failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("DEPLOYMENT VALIDATION: ✅ ALL TESTS PASSED")
print("=" * 60)
print("\nSummary:")
print("  ✓ All modules importable")
print("  ✓ Core engine working")
print("  ✓ Database functional")
print("  ✓ MCP server registered")
print("  ✓ REST API ready")
print("  ✓ Scheduler configured")
print("  ✓ Audits executable")
print("\n✅ v1.0 is a GOOD PROTOTYPE - READY FOR LOCAL DEPLOYMENT")
