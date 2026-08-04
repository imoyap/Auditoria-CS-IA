"""Clase base y registro de módulos de auditoría."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from auditoria.core.models import Finding


class BaseCheck(ABC):
    """Contrato que deben implementar todos los módulos de auditoría."""

    name: ClassVar[str]
    category: ClassVar[str]
    description: ClassVar[str] = ""

    def __init__(self, target: str = "localhost", config: dict[str, Any] | None = None):
        self.target = target
        self.config = config or {}

    @abstractmethod
    def run(self) -> list[Finding]:
        """Ejecuta las verificaciones y retorna hallazgos."""

    def _enabled(self, key: str, default: bool = True) -> bool:
        return bool(self.config.get(key, default))
