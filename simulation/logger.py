from typing import Callable, list

class Logger:
    """
    Registra eventos y acciones del sistema para trazabilidad y depuración.
    """

    def __init__(
        self,
        log_level: str = "INFO",
        timestamp_fn: Callable[[], float] = None,
    ):
        # lista de mensajes de log
        self.logs: list[str] = []
        # Si el logger está activo
        self.enabled: bool = True
        # Nivel mínimo de severidad: "DEBUG", "INFO", "WARNING", "ERROR"
        self.log_level: str = log_level
        # Función para obtener timestamp
        self.timestamp_fn: Callable[[], float] = timestamp_fn or (lambda: 0.0)

    def log(self, message: str, level: str = "INFO") -> None:
        """Agrega una nueva entrada al log si cumple el nivel mínimo."""
        pass

    def show_history(self, n: int = None) -> list[str]:
        """Devuelve los últimos n registros (o todos si n es None)."""
        pass

    def clear(self) -> None:
        """Limpia todos los registros."""
        pass

    def enable(self) -> None:
        """Activa el sistema de log."""
        pass

    def disable(self) -> None:
        """Desactiva el sistema de log."""
        pass

    def set_level(self, level: str) -> None:
        """Define el nivel mínimo de severidad registrado."""
        pass

    def export(self, path: str) -> None:
        """Exporta los logs a un archivo de texto."""
        pass
