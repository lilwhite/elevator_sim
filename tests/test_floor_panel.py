# tests/test_floor_panel.py

from simulation.floor_panel import FloorPanel


def test_press_up_enables_up():
    panel = FloorPanel(id=1, floor=1, min_floor=1, max_floor=3)
    panel.press_up()
    assert panel.up_pressed
    assert panel.indicator_up


def test_press_down_enables_down():
    panel = FloorPanel(id=2, floor=3, min_floor=1, max_floor=3)
    panel.press_down()
    assert panel.down_pressed
    assert panel.indicator_down


def test_press_up_when_not_available_does_nothing():
    # Último piso no tiene botón de subida
    panel = FloorPanel(id=3, floor=3, min_floor=1, max_floor=3)
    panel.press_up()
    assert not panel.up_pressed
    assert not panel.indicator_up


def test_press_down_when_not_available_does_nothing():
    # Primer piso no tiene botón de bajada
    panel = FloorPanel(id=4, floor=1, min_floor=1, max_floor=3)
    panel.press_down()
    assert not panel.down_pressed
    assert not panel.indicator_down


def test_reset_up_and_reset_down():
    panel = FloorPanel(id=5, floor=2, min_floor=1, max_floor=3)
    panel.press_up()
    panel.press_down()
    panel.reset_up()
    assert not panel.up_pressed
    assert not panel.indicator_up
    panel.reset_down()
    assert not panel.down_pressed
    assert not panel.indicator_down


def test_is_active_and_get_requested_directions():
    panel = FloorPanel(id=6, floor=2, min_floor=1, max_floor=3)
    # Inicialmente inactivo
    assert not panel.is_active()
    assert panel.get_requested_directions() == []
    # Con un solo botón presionado
    panel.press_up()
    assert panel.is_active()
    assert panel.get_requested_directions() == ["up"]
    # Con ambos botones presionados
    panel.press_down()
    assert panel.is_active()
    assert set(panel.get_requested_directions()) == {"up", "down"}
