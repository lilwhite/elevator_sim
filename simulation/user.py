class User:
    """
    Modela a un usuario que llama al ascensor y selecciona un destino.
    """

    def __init__(
        self,
        id: int,
        weight_kg: float,
        current_floor: int = 1,
    ):
        # Identificador único del usuario
        self.id: int = id
        # Peso del usuario (kg)
        self.weight_kg: float = weight_kg
        # Piso actual donde se encuentra
        self.current_floor: int = current_floor
        # Piso destino seleccionado (None si no hay)
        self.destination_floor: int = None
        # Estado: dentro del ascensor o esperando
        self.inside_elevator: bool = False
        self.waiting: bool = False

    def call_elevator(self, direction: str) -> None:
        """Llama al ascensor desde su piso ('up' o 'down')."""
        pass

    def enter_elevator(self) -> None:
        """Marca que el usuario ha entrado al ascensor."""
        pass

    def select_floor(self, floor: int) -> None:
        """Selecciona el piso destino dentro del ascensor."""
        pass

    def exit_elevator(self) -> None:
        """Marca que el usuario ha salido del ascensor."""
        pass

    def wait_for_elevator(self) -> None:
        """Establece el estado de espera tras llamar al ascensor."""
        pass

    def cancel_request(self) -> None:
        """Cancela la solicitud de llamada o destino previo."""
        pass
