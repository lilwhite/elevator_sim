class Door:
    """
    Gestiona la apertura y cierre de las puertas del ascensor.
    """

    def __init__(
        self,
        id: int,
        open_duration: float = 5.0,
    ):
        # Identificador único de la puerta
        self.id: int = id
        # Estado actual: "open", "closed", "opening", "closing"
        self.status: str = "closed"
        # Temporizador de acción (s)
        self.timer: float = 0.0
        # Duración de apertura antes de cerrar automáticamente (s)
        self.open_duration: float = open_duration
        # Indica si la puerta está bloqueada por sensor/manual
        self.blocked: bool = False
        # Cierre automático tras apertura
        self.auto_close: bool = True
        # Bloqueo por emergencia
        self.emergency_locked: bool = False

    def open(self) -> None:
        """Inicia la secuencia de apertura de la puerta."""
        pass

    def close(self) -> None:
        """Inicia la secuencia de cierre de la puerta."""
        pass

    def force_open(self) -> None:
        """Abre la puerta ignorando condiciones normales (emergencia)."""
        pass

    def lock_emergency(self) -> None:
        """Bloquea la puerta en estado de emergencia."""
        pass

    def unlock_emergency(self) -> None:
        """Desbloquea la puerta tras emergencia."""
        pass

    def set_blocked(self, value: bool) -> None:
        """Establece estado de bloqueo por sensor o manual."""
        pass

    def tick(self, dt: float) -> None:
        """Avanza el temporizador, actualiza `status` si la acción finaliza."""
        pass

    def is_open(self) -> bool:
        """True si la puerta está completamente abierta."""
        pass

    def is_closed(self) -> bool:
        """True si la puerta está completamente cerrada."""
        pass

    def is_moving(self) -> bool:
        """True si la puerta está en transición de apertura/cierre."""
        pass
