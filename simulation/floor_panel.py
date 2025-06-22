class FloorPanel:
    """
    Representa el panel de llamada externa en cada piso con botones de subida y bajada.
    """

    def __init__(
        self,
        id: int,
        floor: int,
        min_floor: int,
        max_floor: int,
    ):
        # Identificador único del panel
        self.id: int = id
        # Piso asociado al panel
        self.floor: int = floor
        # Botones de llamada disponibles
        self.has_up_button: bool = floor < max_floor
        self.has_down_button: bool = floor > min_floor
        # Estado de los botones
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        # Indicadores luminosos
        self.indicator_up: bool = False
        self.indicator_down: bool = False

    def press_up(self) -> None:
        """Marca el botón de subida como presionado y enciende la luz si existe."""
        if self.has_up_button:
            self.up_pressed = True
            self.indicator_up = True

    def press_down(self) -> None:
        """Marca el botón de bajada como presionado y enciende la luz si existe."""
        if self.has_down_button:
            self.down_pressed = True
            self.indicator_down = True

    def reset_up(self) -> None:
        """Resetea el estado del botón e indicador de subida."""
        self.up_pressed = False
        self.indicator_up = False

    def reset_down(self) -> None:
        """Resetea el estado del botón e indicador de bajada."""
        self.down_pressed = False
        self.indicator_down = False

    def is_active(self) -> bool:
        """Devuelve True si alguno de los botones está presionado."""
        return self.up_pressed or self.down_pressed

    def get_requested_directions(self) -> list[str]:
        """Devuelve lista de direcciones solicitadas: ['up'], ['down'], o ambas."""
        directions: list[str] = []
        if self.up_pressed:
            directions.append("up")
        if self.down_pressed:
            directions.append("down")
        return directions
