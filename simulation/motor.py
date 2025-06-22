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
        # Clampa la velocidad dentro de los límites permitidos
        self.target_speed = max(-self.max_speed, min(self.max_speed, speed))

    def set_direction(self, dir: str) -> None:
        """Establece la dirección de movimiento ("up", "down" o "stopped")."""
        if dir in ("up", "down", "stopped"):
            self.direction = dir

    def start(self) -> None:
        """Activa el motor para alcanzar la velocidad objetivo según la dirección."""
        if not self.power_on:
            return
        if self.direction == "up":
            self.target_speed = abs(self.target_speed)
        elif self.direction == "down":
            self.target_speed = -abs(self.target_speed)
        else:
            self.target_speed = 0.0

    def stop(self) -> None:
        """Detiene el motor desacelerando hasta 0."""
        self.target_speed = 0.0

    def brake(self) -> None:
        """Aplica frenado de emergencia."""
        self.braking = True
        self.target_speed = 0.0

    def update(self, dt: float) -> None:
        """Actualiza velocidad y posición según el paso de tiempo."""
        # No hace nada si el motor está apagado
        if not self.power_on:
            return
        # Calcular cambio de velocidad
        delta_v = self.acceleration * dt
        # Acelerar o desacelerar hacia target_speed
        if self.current_speed < self.target_speed:
            self.current_speed = min(self.current_speed + delta_v, self.target_speed, self.max_speed)
        elif self.current_speed > self.target_speed:
            self.current_speed = max(self.current_speed - delta_v, self.target_speed, -self.max_speed)
        # Actualizar posición
        self.position_m += self.current_speed * dt
        # Actualizar dirección basada en velocidad
        if self.current_speed > 0:
            self.direction = "up"
        elif self.current_speed < 0:
            self.direction = "down"
        else:
            self.direction = "stopped"

    def is_idle(self) -> bool:
        """
        True si el motor está parado y sin velocidad objetivo.
        """
        if not self.power_on:
            return True
        return self.current_speed == 0.0 and self.target_speed == 0.0

    def get_position(self) -> float:
        """Devuelve la posición vertical actual."""
        return self.position_m
