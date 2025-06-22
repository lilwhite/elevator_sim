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
        # Duración de apertura antes de cerrar automáticamente (s) y también para cierre
        self.open_duration: float = open_duration
        # Indica si la puerta está bloqueada por objeto o sensor de seguridad
        self.blocked: bool = False
        # Cierre automático tras apertura (no usado por defecto)
        self.auto_close: bool = True
        # Bloqueo por emergencia
        self.emergency_locked: bool = False

    def open(self) -> None:
        """Inicia la secuencia de apertura de la puerta."""
        # Siempre permite apertura
        self.status = "opening"
        self.timer = self.open_duration

    def close(self) -> None:
        """Inicia la secuencia de cierre de la puerta."""
        # Solo cierra si no está bloqueada ni en emergencia
        if self.blocked or self.emergency_locked:
            return
        self.status = "closing"
        self.timer = self.open_duration

    def force_open(self) -> None:
        """Abre la puerta ignorando condiciones normales (emergencia o bloqueo)."""
        self.status = "open"
        self.timer = 0.0

    def lock_emergency(self) -> None:
        """Bloquea la puerta en estado de emergencia."""
        self.emergency_locked = True

    def unlock_emergency(self) -> None:
        """Desbloquea la puerta tras emergencia."""
        self.emergency_locked = False

    def set_blocked(self, value: bool) -> None:
        """Establece estado de bloqueo por sensor o manual."""
        self.blocked = value

    def tick(self, dt: float) -> None:
        """Avanza el temporizador, actualiza `status` si la acción finaliza."""
        if self.status == "opening":
            self.timer -= dt
            if self.timer <= 0:
                self.status = "open"
                self.timer = 0.0
        elif self.status == "closing":
            self.timer -= dt
            if self.timer <= 0:
                # Al cerrar, el bloqueo debe impedir reapertura accidental
                self.status = "closed"
                self.timer = 0.0

    def is_open(self) -> bool:
        """True si la puerta está completamente abierta."""
        return self.status == "open"

    def is_closed(self) -> bool:
        """True si la puerta está completamente cerrada."""
        return self.status == "closed"

    def is_moving(self) -> bool:
        """True si la puerta está en transición de apertura/cierre."""
        return self.status in ("opening", "closing")
