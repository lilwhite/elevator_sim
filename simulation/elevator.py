from .motor import Motor
from .door import Door
from .display import Display
from .sensor import Sensor
from .logger import Logger

class Elevator:
    """
    Representa el ascensor: controla su posición, carga, puertas, dirección y solicitudes.
    """

    def __init__(
        self,
        id: int,
        min_floor: int = 1,
        max_floor: int = 10,
        weight_limit_kg: float = 1600.0,
        speed_mps: float = 1.0,
    ):
        # Identificación y límites
        self.id: int = id
        self.min_floor: int = min_floor
        self.max_floor: int = max_floor

        # Estado dinámico
        self.current_floor: int = min_floor
        self.position_m: float = float(min_floor)  # metros/floors
        self.target_floors: list[int] = []
        self.direction: str = "idle"  # "up", "down", "idle"
        self.is_moving: bool = False

        # Puertas
        self.door_status: str = "closed"  # "open", "opening", "closing"
        self.door_timer: float = 0.0
        self.speed_mps: float = speed_mps

        # Carga
        self.weight_limit_kg: float = weight_limit_kg
        self.current_weight_kg: float = 0.0
        self.emergency_state: bool = False

        # Componentes internos
        self.motor: Motor = Motor(id=self.id, max_speed=self.speed_mps)
        self.door: Door = Door(id=self.id)
        self.sensors: list[Sensor] = []
        self.display: Display = Display(id=self.id)
        self.logger: Logger = Logger()

    def call(self, floor: int) -> None:
        """Solicitud externa desde un FloorPanel: añade floor a target_floors si es válido."""
        if self.min_floor <= floor <= self.max_floor and floor not in self.target_floors:
            self.target_floors.append(floor)

    def select_floor(self, floor: int) -> None:
        """Solicitud interna desde dentro de la cabina: añade floor a target_floors si es válido."""
        if self.min_floor <= floor <= self.max_floor and floor not in self.target_floors:
            self.target_floors.append(floor)

    def step(self, dt: float) -> None:
        # … lógica de puertas y emergencia …

        # 3) Sin destinos: idle
        if not self.target_floors:
            self.is_moving = False
            return

        # 4) Desplazamiento delegado a move_towards_target
        self.is_moving = True
        self.move_towards_target(dt)


    def move_towards_target(self, dt: float) -> None:
        """
        Mueve la posición usando el motor y actualiza current_floor.
        Si llega al destino, detiene el motor y abre la puerta.
        """
        # Sin destinos, aseguramos que el motor pare
        if not self.target_floors:
            self.motor.stop()
            return

        # 1) Calculamos próximo piso y dirección
        next_floor = self.target_floors[0]
        self.update_direction()
        self.motor.set_direction(self.direction)
        self.motor.set_target_speed(self.speed_mps)
        self.motor.start()

        # 2) Actualizamos motor y posición
        self.motor.update(dt)
        self.position_m = self.motor.get_position()

        # 3) Reflectir posición en current_floor (parte entera)
        new_floor = int(self.position_m)
        if new_floor != self.current_floor:
            self.current_floor = new_floor

        # 4) Comprobar llegada al destino
        arrived_up   = self.direction == "up"   and self.position_m >= next_floor
        arrived_down = self.direction == "down" and self.position_m <= next_floor
        if arrived_up or arrived_down:
            # Alineamos con exactitud de piso
            self.motor.stop()
            self.position_m   = float(next_floor)
            self.current_floor = next_floor
            self.target_floors.pop(0)
            # Abrimos puertas al llegar
            self.open_door()

    def open_door(self) -> None:
        """Inicia la apertura de la puerta."""
        # Llama al componente Door
        self.door.open()
        self.door_status = "opening"
        self.door_timer = self.door.open_duration

    def close_door(self) -> None:
        """Inicia el cierre de la puerta."""
        self.door.close()
        self.door_status = "closing"

    def check_overload(self) -> bool:
        """Devuelve True si el peso supera weight_limit_kg."""
        return self.current_weight_kg > self.weight_limit_kg

    def update_direction(self) -> None:
        """Recalcula self.direction según el primer piso en target_floors."""
        if not self.target_floors:
            self.direction = "idle"
        else:
            next_floor = self.target_floors[0]
            if next_floor > self.current_floor:
                self.direction = "up"
            elif next_floor < self.current_floor:
                self.direction = "down"
            else:
                self.direction = "idle"

    def activate_emergency(self) -> None:
        """Detiene operaciones y abre puertas si es posible."""
        self.emergency_state = True
        self.is_moving = False
        self.target_floors.clear()
        self.open_door()

    def reset_emergency(self) -> None:
        """Sale del estado de emergencia."""
        self.emergency_state = False
        # Restablecer estado de puerta si estaba abierta
        if self.door_status == "opening":
            self.door_status = "closed"
            self.door_timer = 0.0

    def is_idle(self) -> bool:
        """True si no hay peticiones y no se está moviendo."""
        return len(self.target_floors) == 0 and not self.is_moving
