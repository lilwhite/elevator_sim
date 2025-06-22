from typing import Any, Callable

class Sensor:
    """
    Representa un sensor genérico (peso, presencia, posición, etc.).
    """

    def __init__(
        self,
        id: int,
        type: str,
        unit: str = "", 
        threshold: float = 0.0,
        timestamp_fn: Callable[[], float] = None,
    ):
        # Identificador único del sensor
        self.id: int = id
        # Tipo: "weight", "presence", "position", "door", "floor", etc.
        self.type: str = type
        # Valor actual del sensor
        self.value: Any = None
        # Unidad de medida ("kg", "m", "bool", etc.)
        self.unit: str = unit
        # Umbral crítico para alerta
        self.threshold: float = threshold
        # Activo/deshabilitado
        self.active: bool = True
        # Última actualización de valor (timestamp)
        self.last_updated: float = 0.0
        # Función para obtener tiempo actual (útil para pruebas)
        self.timestamp_fn: Callable[[], float] = timestamp_fn or (lambda: 0.0)

    def read(self) -> Any:
        """Devuelve el valor actual del sensor."""
        return self.value

    def update(self, value: Any) -> None:
        """Actualiza el valor del sensor y el timestamp si está activo."""
        if not self.active:
            return
        self.value = value
        self.last_updated = self.timestamp_fn()

    def is_triggered(self) -> bool:
        """Retorna True si `value` supera `threshold` (si aplica)."""
        if self.value is None:
            return False
        try:
            return float(self.value) > self.threshold
        except (TypeError, ValueError):
            return False

    def calibrate(self, offset: float) -> None:
        """Ajusta el valor base del sensor añadiendo un offset."""
        if self.value is not None:
            try:
                self.value = self.value + offset
            except TypeError:
                pass

    def enable(self) -> None:
        """Habilita el sensor."""
        self.active = True

    def disable(self) -> None:
        """Deshabilita el sensor."""
        self.active = False

    def reset(self) -> None:
        """Reinicia el sensor a estado por defecto."""
        self.value = None
        self.last_updated = 0.0
        self.active = True
