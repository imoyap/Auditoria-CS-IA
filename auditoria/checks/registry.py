"""Registro central de módulos de auditoría."""

from __future__ import annotations

from auditoria.checks.base import BaseCheck

_REGISTRY: dict[str, type[BaseCheck]] = {}


def register_check(cls: type[BaseCheck]) -> type[BaseCheck]:
    """Decorador para registrar un módulo de auditoría."""
    _REGISTRY[cls.name] = cls
    return cls


def get_checks() -> dict[str, type[BaseCheck]]:
    _ensure_loaded()
    return dict(_REGISTRY)


def list_available_checks() -> list[str]:
    return sorted(get_checks().keys())


def list_categories() -> list[str]:
    return sorted({c.category for c in get_checks().values()})


def _ensure_loaded() -> None:
    if _REGISTRY:
        return
    # Importación tardía para registrar todos los checks
    import auditoria.checks  # noqa: F401
