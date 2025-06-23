# simulation/user.py

from typing import Optional
import logging

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

    def call_elevator(self, direction: str):
        """
        Llamada al botón de planta (externa).
        """
        logging.info(f"User {self.id} called elevator at floor {self.current_floor} going {direction}")

    def enter_elevator(self) -> None:
        """
        El usuario entra al ascensor.
        """
        if self.waiting:
            self.inside_elevator = True
            self.waiting = False

    def select_floor(self, floor: int):
        """
        Se invoca cuando el usuario YA está dentro del ascensor.
        Guarda su destino interno.
        """
        self.destination_floor = floor
        logging.info(f"User {self.id} selected internal floor {floor}")

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
