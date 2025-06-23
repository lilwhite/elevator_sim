# tests/test_user.py

import pytest
from simulation.user import User

def test_call_elevator_sets_waiting():
    u = User(id=1, weight_kg=70.0, current_floor=2)
    assert not u.waiting
    u.call_elevator("up")
    assert u.waiting

def test_wait_for_elevator_sets_waiting():
    u = User(id=2, weight_kg=60.0, current_floor=1)
    u.waiting = False
    u.wait_for_elevator()
    assert u.waiting

def test_enter_elevator_only_if_waiting():
    u = User(id=3, weight_kg=80.0, current_floor=1)
    u.inside_elevator = False
    u.waiting = False
    u.enter_elevator()
    assert not u.inside_elevator  # no entra si no estaba esperando

    u.waiting = True
    u.enter_elevator()
    assert u.inside_elevator
    assert not u.waiting

def test_select_floor_only_if_inside():
    u = User(id=4, weight_kg=65.0, current_floor=1)
    u.inside_elevator = False
    u.select_floor(5)
    assert u.destination_floor is None

    u.inside_elevator = True
    u.select_floor(5)
    assert u.destination_floor == 5

def test_exit_elevator_updates_floor_and_state():
    u = User(id=5, weight_kg=75.0, current_floor=2)
    u.inside_elevator = True
    u.destination_floor = 4
    u.exit_elevator()
    assert not u.inside_elevator
    assert u.current_floor == 4
    assert u.destination_floor is None

def test_exit_elevator_no_effect_if_not_inside_or_no_destination():
    u = User(id=6, weight_kg=55.0, current_floor=3)
    # Ni dentro ni destino
    u.inside_elevator = False
    u.destination_floor = None
    u.exit_elevator()
    assert u.current_floor == 3

    # Dentro pero sin destino
    u.inside_elevator = True
    u.destination_floor = None
    u.exit_elevator()
    assert u.current_floor == 3
