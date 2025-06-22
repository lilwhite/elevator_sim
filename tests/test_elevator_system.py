# tests/test_elevator_system.py

import pytest
from simulation import (
    ElevatorSystem,
    Elevator,
    Controller,
    User,
    FloorPanel
)

@pytest.fixture
def simple_system():
    # Sistema con pisos del 1 al 3, un ascensor y su controlador
    system = ElevatorSystem(min_floor=1, max_floor=3)
    system.populate_panels()
    elev = Elevator(id=1, min_floor=1, max_floor=3)
    ctrl = Controller(
        id=1,
        elevator=elev,
        floor_panels=list(system.floor_panels.values()),
        logger=system.logger
    )
    system.add_elevator(elev, ctrl)
    return system

def test_populate_panels_creates_panels(simple_system):
    system = simple_system
    # Debemos tener un panel por cada piso
    assert set(system.floor_panels.keys()) == {1, 2, 3}
    for floor, panel in system.floor_panels.items():
        assert isinstance(panel, FloorPanel)
        assert panel.floor == floor

def test_add_user_appends_to_list(simple_system):
    system = simple_system
    user = User(id=42, weight_kg=65.0, current_floor=2)
    system.add_user(user)
    assert user in system.users

def test_dispatch_request_assigns_to_controller(simple_system):
    system = simple_system
    # Llamada externa desde el piso 3
    system.dispatch_request(floor=3, direction="up")
    # Comprobamos que el controlador recogió la solicitud
    ctrl = system.controllers[0]
    assert 3 in ctrl.pending_requests

def test_run_tick_processes_and_moves(simple_system):
    system = simple_system
    # Llamada y primer tick
    system.dispatch_request(floor=3, direction="up")
    system.run_tick(dt=1.0)
    elev = system.elevators[0]
    # Tras un tick, el ascensor debe haberse movido (current_floor > min_floor)
    assert elev.current_floor != elev.min_floor

def test_get_elevator_status_returns_list_of_dicts(simple_system):
    status = simple_system.get_elevator_status()
    assert isinstance(status, list)
    assert len(status) == 1
    info = status[0]
    # Debe incluir al menos estos campos
    assert info["id"] == 1
    assert isinstance(info["current_floor"], int)
    assert info["direction"] in ("up", "down", "idle")
