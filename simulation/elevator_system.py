# simulation/elevator_system.py

from .controller import Controller
from .floor_panel import FloorPanel
from .user import User
from .logger import Logger
from typing import List, Dict

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .elevator import Elevator


class ElevatorSystem:
    def __init__(
        self,
        min_floor: int = 1,
        max_floor: int = 10,
        logger: Logger = None,
    ):
        self.min_floor = min_floor
        self.max_floor = max_floor
        # import dinámico para evitar circular
        from .elevator import Elevator
        self.elevators: list[Elevator] = []
        self.controllers: List[Controller] = []
        self.floor_panels: Dict[int, FloorPanel] = {}
        self.users: List[User] = []
        self.logger: Logger = logger or Logger()
        self.time: float = 0.0

        # paneles de planta
        self.floor_panel: Dict[int, FloorPanel] = {
            f: FloorPanel(
                id=f,
                floor=f,
                min_floor=self.min_floor,
                max_floor=self.max_floor
            )
            for f in range(self.min_floor, self.max_floor + 1)        
        }

    def populate_panels(self) -> None:
        """Crea un FloorPanel por cada piso entre min_floor y max_floor."""
        for floor in range(self.min_floor, self.max_floor + 1):
            panel = FloorPanel(
                id=floor,
                floor=floor,
                min_floor=self.min_floor,
                max_floor=self.max_floor,
            )
            self.floor_panels[floor] = panel

    def add_elevator(self, elevator: "Elevator", controller: Controller) -> None:
        self.elevators.append(elevator)
        # Vinculamos el listado global de usuarios al controlador
        controller.users = self.users
        self.controllers.append(controller)

    def add_user(self, user: User) -> None:
        """Añade un usuario al sistema."""
        self.users.append(user)

    def dispatch_request(self, floor: int, direction: str) -> None:
        """
        Asigna una llamada externa a un controlador.
        De momento, despacha siempre al primer controlador.
        """
        if not self.controllers:
            return
        ctrl = self.controllers[0]
        ctrl.add_external_request(floor)
        self.logger.log(f"Dispatched external call for floor {floor}", "INFO")

    def run_tick(self, dt: float) -> None:
        """
        Ejecuta un ciclo de simulación de dt segundos:
        - Incrementa el tiempo global.
        - Llama a run_tick(dt) de cada controlador.
        """
        self.time += dt
        for ctrl in self.controllers:
            ctrl.run_tick(dt)

    def get_elevator_status(self) -> List[Dict]:
        """
        Devuelve una lista de diccionarios con el estado de cada ascensor:
        id, current_floor y direction.
        """
        status = []
        for elev in self.elevators:
            status.append({
                "id": elev.id,
                "current_floor": elev.current_floor,
                "direction": elev.direction,
            })
        return status

    def reset(self) -> None:
        """
        Reinicia el sistema a su estado inicial:
        limpia ascensores, controladores, paneles, usuarios y tiempo.
        """
        self.elevators.clear()
        self.controllers.clear()
        self.floor_panels.clear()
        self.users.clear()
        self.time = 0.0
        self.logger.log("ElevatorSystem reset", "INFO")

