# tests/test_door.py
import pytest
from simulation.door import Door


def test_open_sets_status_and_timer():
    d = Door(id=1, open_duration=3.0)
    d.open()
    assert d.status == "opening"
    assert pytest.approx(d.timer, rel=1e-3) == 3.0


def test_tick_completes_open():
    d = Door(id=1, open_duration=2.0)
    d.open()
    d.tick(2.5)
    assert d.status == "open"
    assert pytest.approx(d.timer, rel=1e-3) == 0.0
    assert d.is_open()
    assert not d.is_moving()


def test_close_sets_status_and_timer():
    d = Door(id=1, open_duration=4.0)
    # Primero abrimos para poder cerrar
    d.open()
    d.tick(4.0)
    assert d.status == "open"
    d.close()
    assert d.status == "closing"
    assert pytest.approx(d.timer, rel=1e-3) == 4.0


def test_tick_completes_close():
    d = Door(id=1, open_duration=1.5)
    d.open(); d.tick(1.5)
    d.close()
    d.tick(2.0)
    assert d.status == "closed"
    assert d.is_closed()
    assert not d.is_moving()


def test_blocked_prevents_close():
    d = Door(id=1, open_duration=2.0)
    d.open(); d.tick(2.0)
    d.set_blocked(True)
    d.close()
    # No debería iniciar cierre si está bloqueada
    assert not d.is_moving()
    assert d.status == "open"


def test_force_open_ignores_block_and_emergency():
    d = Door(id=1, open_duration=5.0)
    d.set_blocked(True)
    d.lock_emergency()
    d.force_open()
    assert d.status == "open"
    assert d.timer == 0.0
    assert d.is_open()
