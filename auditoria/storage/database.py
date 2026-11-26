"""Gestor de base de datos SQLite para auditorías."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from auditoria.core.models import AuditReport


def _to_db_timestamp(value: Any) -> Any:
    """Serializa datetime como hacía el adaptador por defecto de sqlite3
    (deprecado en Python 3.12): ISO 8601 con espacio como separador."""
    if isinstance(value, datetime):
        return value.isoformat(" ")
    return value


class DatabaseManager:
    """Gestiona persistencia de auditorías en SQLite."""

    def __init__(self, db_path: str | Path = "auditoria.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self) -> None:
        """Crea tablas si no existen."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            started_at TIMESTAMP NOT NULL,
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

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER NOT NULL,
            check_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            recommendation TEXT,
            evidence TEXT,
            references_list TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (audit_id) REFERENCES audits(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id INTEGER NOT NULL,
            finding_id INTEGER,
            analysis_type TEXT NOT NULL,
            content TEXT NOT NULL,
            model_used TEXT,
            tokens_used INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (audit_id) REFERENCES audits(id),
            FOREIGN KEY (finding_id) REFERENCES findings(id)
        )
        """)

        conn.commit()
        conn.close()

    def save_audit(self, report: AuditReport) -> int:
        """Guarda una auditoría completa. Returns: audit_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        summary = report.summary
        modules = ", ".join(set(r.module for r in report.results))

        cursor.execute("""
        INSERT INTO audits (
            target, started_at, finished_at, risk_score, modules,
            total_findings, critical, high, medium, low, report_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report.target,
            _to_db_timestamp(report.started_at),
            _to_db_timestamp(report.finished_at),
            report.risk_score,
            modules,
            summary.get("total_findings", 0),
            summary.get("critical", 0),
            summary.get("high", 0),
            summary.get("medium", 0),
            summary.get("low", 0),
            json.dumps(report.to_dict(), default=str),
        ))

        audit_id = cursor.lastrowid

        for finding in report.all_findings:
            cursor.execute("""
            INSERT INTO findings (
                audit_id, check_id, title, description, severity, status,
                recommendation, evidence, references_list
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_id,
                finding.check_id,
                finding.title,
                finding.description,
                finding.severity.value,
                finding.status.value,
                finding.recommendation,
                json.dumps(finding.evidence),
                json.dumps(finding.references),
            ))

        conn.commit()
        conn.close()
        return audit_id

    def save_ai_analysis(
        self,
        audit_id: int,
        analysis_type: str,
        content: str,
        finding_id: Optional[int] = None,
        model_used: str = "claude-3-5-sonnet-20241022",
        tokens_used: int = 0,
    ) -> int:
        """Guarda análisis de IA. Returns: analysis_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO ai_analyses (
            audit_id, finding_id, analysis_type, content, model_used, tokens_used
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            audit_id,
            finding_id,
            analysis_type,
            content,
            model_used,
            tokens_used,
        ))

        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return analysis_id

    def get_audit(self, audit_id: int) -> Optional[dict]:
        """Obtiene auditoría por ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return dict(result)
        return None

    def list_audits(self, target: Optional[str] = None, limit: int = 50) -> list[dict]:
        """Lista auditorías. Filtrar por target si se especifica."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if target:
            cursor.execute(
                "SELECT * FROM audits WHERE target = ? ORDER BY created_at DESC LIMIT ?",
                (target, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM audits ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )

        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_findings_for_audit(self, audit_id: int) -> list[dict]:
        """Obtiene todos los hallazgos de una auditoría."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM findings WHERE audit_id = ? ORDER BY severity DESC",
            (audit_id,),
        )

        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_ai_analyses(self, audit_id: int) -> list[dict]:
        """Obtiene análisis de IA para una auditoría."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM ai_analyses WHERE audit_id = ? ORDER BY created_at DESC",
            (audit_id,),
        )

        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]

    def get_trends(self, target: str, days: int = 30) -> dict[str, Any]:
        """Analiza tendencias de vulnerabilidades en el tiempo."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            DATE(started_at) as date,
            COUNT(*) as audits,
            SUM(critical) as critical,
            SUM(high) as high,
            SUM(medium) as medium,
            SUM(low) as low,
            AVG(risk_score) as avg_risk
        FROM audits
        WHERE target = ? AND created_at >= datetime('now', '-' || ? || ' days')
        GROUP BY DATE(started_at)
        ORDER BY date DESC
        """, (target, days))

        results = cursor.fetchall()
        conn.close()

        return {
            "target": target,
            "period_days": days,
            "trends": [dict(row) for row in results],
        }
