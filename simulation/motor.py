class Motor:
    """
    Motor encargado del movimiento vertical del ascensor.
    """

    def __init__(
        self,
        id: int,
        max_speed: float = 1.0,
        acceleration: float = 0.5,
    ):
        # Identificador único del motor
        self.id: int = id
        # Velocidad actual (m/s)
        self.current_speed: float = 0.0
        # Velocidad objetivo (m/s)
        self.target_speed: float = 0.0
        # Aceleración (m/s²)
        self.acceleration: float = acceleration
        # Velocidad máxima permitida (m/s)
        self.max_speed: float = max_speed
        # Dirección actual: "up", "down" o "stopped"
        self.direction: str = "stopped"
        # Posición vertical (m)
        self.position_m: float = 0.0
        # Estado de frenado
        self.braking: bool = False
        # Estado de alimentación
        self.power_on: bool = True

    def set_target_speed(self, speed: float) -> None:
        """Define una nueva velocidad objetivo."""
        pass

    def set_direction(self, dir: str) -> None:
        """Establece la dirección de movimiento ("up" o "down")."""
        pass

    def start(self) -> None:
        """Activa el motor para alcanzar la velocidad objetivo."""
        pass

    def stop(self) -> None:
        """Detiene el motor desacelerando hasta 0."""
        pass

    def brake(self) -> None:
        """Aplica frenado de emergencia."""
        pass

    def update(self, dt: float) -> None:
        """Actualiza velocidad y posición según el paso de tiempo."""
        pass

    def is_idle(self) -> bool:
        """True si el motor está parado y sin velocidad objetivo."""
        pass

    def get_position(self) -> float:
        """Devuelve la posición vertical actual."""
        pass
