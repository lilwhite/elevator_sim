# tests/test_elevator_step.py
import pytest
from simulation.elevator import Elevator


def test_step_moves_towards_floor_up_and_opens_door():
    # Ascensor con velocidad 1 floor/s desde piso 1
    e = Elevator(id=1, min_floor=1, max_floor=5, speed_mps=1.0)
    e.call(2)
    # Un tick de 1s debe moverlo al piso 2 y abrir puerta
    e.step(1.0)
    assert e.current_floor == 2
    assert e.position_m == pytest.approx(2.0)
    assert e.door_status == 'opening'
    # La solicitud 2 debe haber sido atendida y eliminada
    assert e.target_floors == []


def test_step_moves_towards_floor_down_and_opens_door():
    # Ascensor inicializado en piso 3 hacia abajo
    e = Elevator(id=1, min_floor=1, max_floor=5, speed_mps=1.0)
    e.current_floor = 3
    e.position_m = 3.0
    e.call(1)
    # Un tick de 2s debe moverlo al piso 1 (2 floors) y abrir puerta
    e.step(2.0)
    assert e.current_floor == 1
    assert e.position_m == pytest.approx(1.0)
    assert e.door_status == 'opening'
    assert e.target_floors == []


def test_step_idle_when_no_requests():
    e = Elevator(id=1, min_floor=1, max_floor=5, speed_mps=1.0)
    # Sin solicitudes, no cambio de estado
    e.step(1.0)
    assert e.current_floor == 1
    assert not e.is_moving
    assert e.door_status == 'closed'


