from .elevator import Elevator
from .user import User
from .floor_panel import FloorPanel
from .logger import Logger

class Controller:
    """
    Orquesta la lógica de movimiento del ascensor y gestiona las solicitudes.
    """

    def __init__(
        self,
        id: int,
        elevator: Elevator,
        floor_panels: list[FloorPanel],
        logger: Logger,
    ):
        # Identificador único del controlador
        self.id: int = id
        # Ascensor gestionado
        self.elevator: Elevator = elevator
        # Paneles de llamada externa
        self.floor_panels: list[FloorPanel] = floor_panels
        # Sistema de log
        self.logger: Logger = logger
        # lista de solicitudes externas
        self.pending_requests: list[int] = []
        # Tiempo interno del controlador
        self.time: float = 0.0

    def run_tick(self, dt: float) -> None:
        """Avanza un ciclo de simulación de dt segundos."""
        pass

    def handle_requests(self) -> None:
        """Procesa las solicitudes internas y externas pendientes."""
        pass

    def add_external_request(self, floor: int) -> None:
        """Añade una solicitud de llamada desde un panel exterior."""
        pass

    def add_internal_request(self, floor: int) -> None:
        """Añade una solicitud desde dentro del ascensor."""
        pass

    def update_users(self) -> None:
        """Gestiona las acciones de los usuarios (entrar, salir, llamar)."""
        pass

    def log_event(self, event: str) -> None:
        """Envía un evento al logger."""
        pass

    def reset(self) -> None:
        """Reinicia el controlador a su estado inicial."""
        pass

    def get_active_calls(self) -> list[int]:
        """Devuelve los pisos que han solicitado el ascensor."""
        pass
