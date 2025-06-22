from .elevator import Elevator
from .controller import Controller
from .floor_panel import FloorPanel
from .user import User
from .logger import Logger

class ElevatorSystem:
    """
    Gestiona un conjunto de ascensores, controladores, paneles y usuarios en un edificio.
    """

    def __init__(
        self,
        min_floor: int = 1,
        max_floor: int = 10,
    ):
        # Rango de pisos del edificio
        self.min_floor: int = min_floor
        self.max_floor: int = max_floor

        # Componentes del sistema
        self.elevators: list[Elevator] = []
        self.controllers: list[Controller] = []
        self.floor_panels: dict[int, FloorPanel] = {}
        self.users: list[User] = []
        self.logger: Logger = Logger()

        # Tiempo de simulación
        self.time: float = 0.0

    def add_elevator(self, elevator: Elevator, controller: Controller) -> None:
        """Añade un ascensor con su controlador al sistema."""
        pass

    def add_user(self, user: User) -> None:
        """Registra un nuevo usuario en el sistema."""
        pass

    def populate_panels(self) -> None:
        """Crea un FloorPanel por cada piso en el edificio."""
        pass

    def dispatch_request(self, floor: int, direction: str) -> None:
        """Asigna la llamada externa al ascensor más adecuado."""
        pass

    def run_tick(self, dt: float) -> None:
        """Avanza la simulación dt segundos para todos los componentes."""
        pass

    def get_elevator_status(self) -> list[dict]:
        """Devuelve un resumen del estado de cada ascensor."""
        pass

    def reset(self) -> None:
        """Reinicia el estado completo del sistema."""
        pass
