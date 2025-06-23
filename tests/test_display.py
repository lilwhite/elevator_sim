# tests/test_display.py
from simulation.display import Display


def test_update_floor_direction_and_door():
    d = Display(id=1)
    d.update_floor(3)
    assert d.current_floor == 3
    d.update_direction("up")
    assert d.direction == "up"
    d.update_door("open")
    assert d.door_status == "open"


def test_show_and_clear_error():
    d = Display(id=1)
    d.show_error("Test error")
    assert d.error_message == "Test error"
    d.clear_error()
    assert d.error_message == ""


def test_render_contains_correct_info():
    d = Display(id=1)
    d.update_floor(2)
    d.update_direction("down")
    d.update_door("closing")
    d.show_error("Err msg")
    output = d.render()
    # Verificar que el render incluye todos los campos relevantes
    assert "Floor: 2" in output
    assert "Direction: down" in output
    assert "Door: closing" in output
    assert "Error: Err msg" in output
