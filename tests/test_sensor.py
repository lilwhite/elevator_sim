# tests/test_sensor.py
import pytest
from simulation.sensor import Sensor


def test_read_returns_initial_value_and_updates():
    s = Sensor(id=1, type="weight", unit="kg")
    # Valor inicial None
    assert s.read() is None
    # Modificar valor manualmente
    s.value = 10.5
    assert s.read() == 10.5


def test_update_sets_value_and_timestamp():
    # Timestamp fijo para comprobación
    ts = lambda: 123.456
    s = Sensor(id=2, type="weight", unit="kg", threshold=5.0, timestamp_fn=ts)
    s.update(7.2)
    assert s.value == 7.2
    assert pytest.approx(s.last_updated, rel=1e-6) == 123.456


def test_is_triggered_based_on_threshold():
    s = Sensor(id=3, type="weight", unit="kg", threshold=5.0)
    s.update(4.9)
    assert not s.is_triggered()
    s.update(5.1)
    assert s.is_triggered()


def test_calibrate_adjusts_value():
    s = Sensor(id=4, type="position", unit="m")
    s.value = 10.0
    s.calibrate(-2.5)
    assert pytest.approx(s.value, rel=1e-6) == 7.5


def test_enable_disable_and_reset_behaviour():
    ts = lambda: 50.0
    s = Sensor(id=5, type="presence", unit="bool", timestamp_fn=ts)
    # Desactivar sensor: no debe actualizar
    s.disable()
    s.update(1)
    assert s.value is None
    # Reactivar sensor: sí actualiza
    s.enable()
    s.update(1)
    assert s.value == 1
    # Resetear sensor: vuelve a estado inicial
    s.reset()
    assert s.value is None
    assert pytest.approx(s.last_updated, rel=1e-6) == 0.0
    assert s.active
