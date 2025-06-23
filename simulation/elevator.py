from .motor import Motor
from .door import Door
from .display import Display
from .sensor import Sensor
from .logger import Logger
from typing import List, TYPE_CHECKING
from .user import User

if TYPE_CHECKING:
    from .elevator_system import ElevatorSystem


class Elevator:
    """
    Representa el ascensor: controla su posición, carga, puertas, dirección y solicitudes.
    """

    def __init__(
        self,
        id: int,
        system: "ElevatorSystem",
        min_floor: int = 1,
        max_floor: int = 10,
        weight_limit_kg: float = 600.0,
        speed_mps: float = 1.0,
    ):
        # Referencia al sistema
        self.system = system

        # Identificación y límites
        self.id = id
        self.min_floor = min_floor
        self.max_floor = max_floor

        # Estado dinámico
        self.current_floor = min_floor
        self.position_m = float(min_floor)
        self.target_floors: List[int] = []
        self.direction = "idle"   # "up", "down", "idle"
        self.is_moving = False

        # Control de puertas
        self.door = Door(id=self.id)
        self._just_opened = False

        # Velocidad
        self.speed_mps = speed_mps

        # Carga
        self.weight_limit_kg = weight_limit_kg
        self.current_weight_kg = 0.0
        self.emergency_state = False

        # Componentes auxiliares
        self.motor = Motor(id=self.id, max_speed=self.speed_mps)
        self.display = Display(id=self.id)
        self.logger = Logger()

        # Pasajeros dentro
        self.passengers: List[User] = []


    def call(self, floor: int) -> None:
        if self.min_floor <= floor <= self.max_floor and floor not in self.target_floors:
            self.target_floors.append(floor)

    def select_floor(self, floor: int) -> None:
        if self.min_floor <= floor <= self.max_floor and floor not in self.target_floors:
            self.target_floors.append(floor)

    def step(self, dt: float) -> None:
        if self.emergency_state:
            return

        # 1) Avanza la animación de la puerta
        self.door.tick(dt)

        # 2) Si justo acabó de abrir, cargo/descargo y cierro
        if self._just_opened:
            self.unload_passengers()
            self.load_passengers()
            self._just_opened = False
            self.door.close()
            return

        # 3) Si la puerta está en transición, esperamos
        if self.door.is_moving():
            return

        # 4) Si la puerta está completamente abierta y no hemos marcado aún
        if self.door.is_open() and not self._just_opened:
            # marcamos para que en el siguiente tick ejecute load/unload
            self._just_opened = True
            return

        # 5) Aquí la puerta está completamente cerrada
        if not self.target_floors:
            self.is_moving = False
            return

        # 6) Movemos hacia la siguiente parada
        self.is_moving = True
        self.move_towards_target(dt)


    def move_towards_target(self, dt: float) -> None:
        if not self.target_floors:
            return

        next_floor = self.target_floors[0]
        self.update_direction()

        # Mover "físico"
        delta = self.speed_mps * dt * (1 if self.direction == "up" else -1)
        self.position_m += delta

        # Actualizar piso actual
        new_floor = int(self.position_m)
        if new_floor != self.current_floor:
            self.current_floor = new_floor

        # Si llegamos o pasamos el destino
        if ((self.direction == "up" and self.position_m >= next_floor) or
            (self.direction == "down" and self.position_m <= next_floor)):
            self.position_m = float(next_floor)
            self.current_floor = next_floor
            self.target_floors.pop(0)
            self.open_door()


    def open_door(self) -> None:
        self.door.open()
        # Al terminar la apertura, en el siguiente step marcaremos _just_opened


    def activate_emergency(self) -> None:
        self.emergency_state = True
        self.is_moving = False
        self.target_floors.clear()
        self.open_door()

    def reset_emergency(self) -> None:
        self.emergency_state = False
        # No devolvemos la puerta a cerrar aquí, se manejará en step()

    def is_idle(self) -> bool:
        return not self.target_floors and not self.is_moving

    def unload_passengers(self) -> None:
        offboard = [u for u in self.passengers
                    if u.destination == self.current_floor]
        for u in offboard:
            self.passengers.remove(u)
            self.current_weight_kg -= u.weight_kg
            u.exit(self.current_floor)
            self.logger.info(f"User {u.id} left at floor {self.current_floor}")

    def load_passengers(self) -> None:
        waiting = self.system.floor_panels[self.current_floor] \
                            .get_waiting_users(self.current_floor,
                                               self.direction)
        for u in waiting:
            self.passengers.append(u)
            self.current_weight_kg += u.weight_kg
            self.internal_panel.press(u.destination)
            self.logger.info(
                f"User {u.id} boarded at floor {self.current_floor} → dest {u.destination}"
            )

    def update_direction(self) -> None:
        if not self.target_floors:
            self.direction = "idle"
            return
        next_floor = self.target_floors[0]
        if next_floor > self.current_floor:
            self.direction = "up"
        elif next_floor < self.current_floor:
            self.direction = "down"
        else:
            self.direction = "idle"
