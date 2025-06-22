# simulation/elevator.py

from .motor          import Motor
from .door           import Door
from .display        import Display
from .sensor         import Sensor
from .logger         import Logger
from typing          import list

class Elevator:
    def __init__(
        self,
        id: int,
        min_floor: int = 1,
        max_floor: int = 10,
        weight_limit_kg: float = 1600.0,
        speed_mps: float = 1.0,
    ):
        # Identificación y límites
        self.id                 : int           = id
        self.min_floor          : int           = min_floor
        self.max_floor          : int           = max_floor

        # Estado dinámico
        self.current_floor      : int           = min_floor
        self.position_m         : float         = float(min_floor)  # metros
        self.target_floors      : list[int]     = []
        self.direction          : str           = "idle"            # "up", "down", "idle"
        self.is_moving          : bool          = False

        # Puertas
        self.door_status        : str           = "closed"          # "open", "opening", "closing"
        self.door_timer         : float         = 0.0
        self.speed_mps          : float         = speed_mps

        # Carga
        self.weight_limit_kg    : float         = weight_limit_kg
        self.current_weight_kg  : float         = 0.0
        self.emergency_state    : bool          = False

        # Componentes internos
        self.motor              : Motor         = Motor(id=self.id, max_speed=self.speed_mps)
        self.door               : Door          = Door(id=self.id)
        self.sensors            : list[Sensor]  = []
        self.display            : Display       = Display(id=self.id)
        self.logger             : Logger        = Logger()

    def call(self, floor: int) -> None:
        """Solicitud externa desde un FloorPanel."""
        pass

    def select_floor(self, floor: int) -> None:
        """Solicitud interna desde dentro de la cabina."""
        pass

    def step(self, dt: float) -> None:
        """Avanza el estado del ascensor dt segundos."""
        pass

    def move_towards_target(self) -> None:
        """Mueve la posición y actualiza current_floor."""
        pass

    def open_door(self) -> None:
        """Inicia la apertura de la puerta."""
        pass

    def close_door(self) -> None:
        """Inicia el cierre de la puerta."""
        pass

    def check_overload(self) -> bool:
        """Devuelve True si el peso supera weight_limit_kg."""
        pass

    def update_direction(self) -> None:
        """Recalcula self.direction según target_floors."""
        pass

    def activate_emergency(self) -> None:
        """Detiene operaciones y abre puertas si es posible."""
        pass

    def reset_emergency(self) -> None:
        """Sale del estado de emergencia."""
        pass

    def is_idle(self) -> bool:
        """True si no hay peticiones ni movimiento."""
        pass
