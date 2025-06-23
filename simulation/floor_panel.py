from typing import List
from .user import User

class FloorPanel:
    """
    Panel externo de cada piso:  
    - mantiene cola de usuarios que han llamdo desde aquí  
    - enciende/apaga indicadores según dirección  
    """
    def __init__(
        self,
        id: int,
        floor: int,
        min_floor: int,
        max_floor: int,
    ):
        self.id = id
        self.floor = floor
        self.has_up_button = floor < max_floor
        self.has_down_button = floor > min_floor
        self.up_pressed = False
        self.down_pressed = False
        self.indicator_up = False
        self.indicator_down = False
        # Cola interna de usuarios que esperan en este piso
        self._waiting: List[User] = []

    def press_up(self) -> None:
        if self.has_up_button:
            self.up_pressed = True
            self.indicator_up = True

    def press_down(self) -> None:
        if self.has_down_button:
            self.down_pressed = True
            self.indicator_down = True

    def reset_up(self) -> None:
        self.up_pressed = False
        self.indicator_up = False

    def reset_down(self) -> None:
        self.down_pressed = False
        self.indicator_down = False

    def is_active(self) -> bool:
        return self.up_pressed or self.down_pressed

    def get_requested_directions(self) -> List[str]:
        dirs = []
        if self.up_pressed: dirs.append("up")
        if self.down_pressed: dirs.append("down")
        return dirs

    def call(self, user: User) -> None:
        """Añade usuario a la cola y enciende el indicador correcto."""
        self._waiting.append(user)
        if user.call_direction == "up":
            self.press_up()
        else:
            self.press_down()

    def get_waiting_users(self, current_floor: int, direction: str) -> List[User]:
        """
        Devuelve sólo los usuarios en cola cuya dirección coincide
        con la del ascensor, y los elimina de la cola interna.
        Mantiene el indicador de la otra dirección si procede.
        """
        matches: List[User] = []
        rest: List[User] = []

        for u in self._waiting:
            if u.call_direction == direction:
                matches.append(u)
            else:
                rest.append(u)

        # La cola interna se convierte en los que no coincidían
        self._waiting = rest

        # Si ya no quedan “up” pendientes, apaga el indicador correspondiente
        if direction == "up" and not any(u.call_direction == "up" for u in self._waiting):
            self.reset_up()
        # Igual para “down”
        if direction == "down" and not any(u.call_direction == "down" for u in self._waiting):
            self.reset_down()

        return matches

    def clear_call(self, floor: int, user_id: str) -> None:
        """Elimina de la cola a un usuario específico (por cancelación, p.ej.)."""
        self._waiting = [u for u in self._waiting if u.id != user_id]
        # (podrías tocar también reset_* si queda vacío para esa dirección)
