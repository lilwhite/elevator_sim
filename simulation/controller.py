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
        floor_panels: list[FloorPanel],
        logger: Logger,
        users: list[User] = None,      # <-- parámetro opcional
    ):
        self.id               = id
        self.elevator         = elevator
        self.floor_panels     = floor_panels
        self.logger           = logger
        self.pending_requests = []
        # Inicializa self.users
        self.users            = users if users is not None else []

    def run_tick(self, dt: float) -> None:
        """
        Avanza un ciclo de simulación de dt segundos:
          • Procesa solicitudes pendientes
          • Mueve el ascensor
          • Gestiona la entrada/salida de usuarios
        """
        # 1) Procesar llamadas
        self.handle_requests()

        # 2) Mover ascensor
        self.elevator.step(dt)

        # 3) Actualizar usuarios (entradas/salidas)
        self.update_users()

        # 4) Incrementar tiempo si lo necesitas aquí
        #	self.time += dt  # si no lo haces en ElevatorSystem

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
        """
        Gestiona las interacciones de los usuarios:
        1) Si un usuario está esperando y el ascensor ha llegado a su piso con puertas OPEN → entra.
        2) Tras entrar, si tiene un destino, se añade la petición interna.
        3) Si un usuario está dentro y el ascensor ha llegado a su destino con puertas OPEN → sale.
        """

        for user in self.users:
            # 1) Entrada al ascensor
            if user.waiting and not user.inside_elevator:
                if (
                    self.elevator.current_floor == user.current_floor
                    and self.elevator.door.is_open()
                ):
                    user.enter_elevator()
                    self.log_event(
                        f"User {user.id} entered elevator at floor {user.current_floor}"
                    )
                    # 2) Petición interna tras entrar
                    if user.destination_floor is not None:
                        self.add_internal_request(user.destination_floor)

            # 3) Salida del ascensor
            if (
                user.inside_elevator
                and user.destination_floor == self.elevator.current_floor
                and self.elevator.door.is_open()
            ):
                user.exit_elevator()
                self.log_event(
                    f"User {user.id} exited elevator at floor {self.elevator.current_floor}"
                )
                # Limpio su destino de la lista si sigue ahí
                if self.elevator.current_floor in self.elevator.target_floors:
                    self.elevator.target_floors.remove(self.elevator.current_floor)


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
