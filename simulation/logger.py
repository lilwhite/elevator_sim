from typing import Callable, List


class Logger:
    """
    Registra eventos y acciones del sistema para trazabilidad y depuración.
    """

    # Mapeo de niveles a valores numéricos para comparación
    _LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
    }

    def __init__(
        self,
        log_level: str = "INFO",
        timestamp_fn: Callable[[], float] = None,
    ):
        # Lista de mensajes de log
        self.logs: List[str] = []
        # Si el logger está activo
        self.enabled: bool = True
        # Nivel mínimo de severidad
        self.log_level: str = log_level
        # Función para obtener timestamp
        self.timestamp_fn: Callable[[], float] = timestamp_fn or (lambda: 0.0)

    def log(self, message: str, level: str = "INFO") -> None:
        """Agrega una nueva entrada al log si el nivel cumple con el mínimo."""
        if not self.enabled:
            return
        lvl = level.upper()
        if lvl not in Logger._LEVELS:
            return
        if Logger._LEVELS[lvl] < Logger._LEVELS.get(self.log_level.upper(), 0):
            return
        timestamp = self.timestamp_fn()
        entry = f"[{timestamp}] {lvl}: {message}"
        self.logs.append(entry)

    def show_history(self, n: int = None) -> List[str]:
        """Devuelve los últimos n registros (o todos si n es None)."""
        if n is None or n >= len(self.logs):
            return list(self.logs)
        return self.logs[-n:]

    def clear(self) -> None:
        """Limpia todos los registros."""
        self.logs.clear()

    def enable(self) -> None:
        """Activa el sistema de log."""
        self.enabled = True

    def disable(self) -> None:
        """Desactiva el sistema de log temporalmente."""
        self.enabled = False

    def set_level(self, level: str) -> None:
        """Cambia el nivel mínimo de severidad que se registrará."""
        lvl = level.upper()
        if lvl in Logger._LEVELS:
            self.log_level = lvl

    def export(self, path: str) -> None:
        """Exporta los logs a un archivo de texto en disco."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                for entry in self.logs:
                    f.write(entry + "\n")
        except Exception:
            pass
