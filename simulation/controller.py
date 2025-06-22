from typing import List
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
        floor_panels: List[FloorPanel],
        logger: Logger,
    ):
        # Identificador único del controlador
        self.id: int = id
        # Ascensor gestionado
        self.elevator: Elevator = elevator
        # Paneles de llamada externa
        self.floor_panels: List[FloorPanel] = floor_panels
        # Sistema de log
        self.logger: Logger = logger
        # Lista de solicitudes externas
        self.pending_requests: List[int] = []
        # Tiempo interno del controlador
        self.time: float = 0.0

    def run_tick(self, dt: float) -> None:
        """Avanza un ciclo de simulación de dt segundos."""
        # Procesar solicitudes pendientes
        self.handle_requests()
        # Avanzar simulación del ascensor
        self.elevator.step(dt)
        # Actualizar tiempo
        self.time += dt

    def handle_requests(self) -> None:
        """Procesa las solicitudes internas y externas pendientes."""
        # Enviar cada petición al ascensor y registrar evento
        for floor in self.pending_requests:
            # Llamada externa -> uso de call
            self.elevator.call(floor)
            self.logger.log(f"External request: floor {floor}", level="DEBUG")
        # Limpiar lista de pendientes
        self.pending_requests.clear()

    def add_external_request(self, floor: int) -> None:
        """Añade una solicitud de llamada desde un panel exterior."""
        if floor not in self.pending_requests:
            self.pending_requests.append(floor)
            self.logger.log(f"Added external request: floor {floor}", level="INFO")

    def add_internal_request(self, floor: int) -> None:
        """Añade una solicitud desde dentro del ascensor."""
        if floor not in self.pending_requests:
            self.pending_requests.append(floor)
            self.logger.log(f"Added internal request: floor {floor}", level="INFO")

    def update_users(self) -> None:
        """Gestiona las acciones de los usuarios (entrar, salir, llamar)."""
        # Módulo opcional: lógica de usuarios
        pass

    def log_event(self, event: str) -> None:
        """Envía un evento al logger."""
        self.logger.log(event, level="INFO")

    def reset(self) -> None:
        """Reinicia el controlador a su estado inicial."""
        self.pending_requests.clear()
        # Limpiar peticiones del ascensor también
        self.elevator.target_floors.clear()
        self.logger.log("Controller reset", level="INFO")
        self.time = 0.0

    def get_active_calls(self) -> List[int]:
        """Devuelve los pisos que han solicitado el ascensor."""
        return list(self.pending_requests)
