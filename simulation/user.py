# simulation/user.py

from typing import Optional

class User:
    def __init__(
        self,
        id: int,
        weight_kg: float,
        current_floor: int
    ):
        self.id: int = id
        self.current_floor: int = current_floor
        self.destination_floor: Optional[int] = None
        self.inside_elevator: bool = False
        self.waiting: bool = False
        self.weight_kg: float = weight_kg

    def call_elevator(self, direction: str) -> None:
        """
        Marca al usuario como en espera y (opcional) almacena la dirección deseada.
        """
        self.waiting = True
        # Si necesitas almacenar direction para lógica futura, podrías hacerlo:
        # self.call_direction = direction

    def enter_elevator(self) -> None:
        """
        El usuario entra al ascensor.
        """
        if self.waiting:
            self.inside_elevator = True
            self.waiting = False

    def select_floor(self, floor: int) -> None:
        """
        Selecciona el piso destino dentro del ascensor.
        """
        if self.inside_elevator:
            self.destination_floor = floor

    def exit_elevator(self) -> None:
        """
        El usuario sale del ascensor al llegar al destino.
        """
        if self.inside_elevator and self.destination_floor is not None:
            self.inside_elevator = False
            self.current_floor = self.destination_floor
            self.destination_floor = None

    def wait_for_elevator(self) -> None:
        """
        Pon al usuario en estado de espera.
        """
        self.waiting = True
