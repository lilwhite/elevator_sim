# tests/test_motor.py

from simulation.motor import Motor

def test_motor_idle_by_default():
    m = Motor(id=1, max_speed=1.0, acceleration=0.5)
    # Sin velocidad objetivo y sin current_speed, debe estar idle
    assert m.is_idle()

def test_motor_not_idle_when_target_speed_set():
    m = Motor(id=1, max_speed=1.0, acceleration=0.5)
    m.target_speed = 0.8
    assert not m.is_idle()
