class Display:
    """
    Muestra información visual del estado del ascensor.
    """

    def __init__(
        self,
        id: int,
    ):
        # Identificador único del display
        self.id: int = id
        # Piso mostrado actualmente
        self.current_floor: int = 0
        # Dirección mostrada: "↑", "↓" o "—"
        self.direction: str = "—"
        # Estado de la puerta mostrado: "open", "closed", "moving"
        self.door_status: str = "closed"
        # Mensaje de error o advertencia
        self.error_message: str = ""
        # Modo: "internal" o "external"
        self.mode: str = "internal"

    def update_floor(self, floor: int) -> None:
        """Actualiza el piso mostrado."""
        pass

    def update_direction(self, dir: str) -> None:
        """Actualiza el símbolo o texto de dirección."""
        pass

    def update_door(self, status: str) -> None:
        """Actualiza el estado de la puerta en pantalla."""
        pass

    def show_error(self, msg: str) -> None:
        """Muestra un mensaje de error o advertencia."""
        pass

    def clear_error(self) -> None:
        """Limpia el mensaje de error actual."""
        pass

    def render(self) -> str:
        """Devuelve una representación visual del display para impresión o logs."""
        pass
