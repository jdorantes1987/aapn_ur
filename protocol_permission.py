from typing import Protocol, Dict, Optional, Set


class Permission(Protocol):
    """
    Protocolo que define las acciones permitidas sobre un recurso.
    """

    def can_read(self) -> bool: ...

    def can_create(self) -> bool: ...

    def can_update(self) -> bool: ...

    def can_delete(self) -> bool: ...


class Role(Protocol):
    """
    Protocolo que define un rol de usuario.
    """

    @property
    def name(self) -> str: ...

    # Verifica si el rol tiene un permiso específico para un proceso dado
    def has_permission_for(self, process_name: str, action: str) -> bool: ...
