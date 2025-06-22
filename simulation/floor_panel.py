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
        # Botones de llamada
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
        pass

    def press_down(self) -> None:
        """Marca el botón de bajada como presionado y enciende la luz si existe."""
        pass

    def reset_up(self) -> None:
        """Resetea el estado del botón e indicador de subida."""
        pass

    def reset_down(self) -> None:
        """Resetea el estado del botón e indicador de bajada."""
        pass

    def is_active(self) -> bool:
        """Devuelve True si alguno de los botones está presionado."""
        pass

    def get_requested_directions(self) -> list:
        """Devuelve lista de direcciones solicitadas: ['up'], ['down'], o ambas."""
        pass
