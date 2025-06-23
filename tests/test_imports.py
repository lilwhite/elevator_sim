# tests/test_imports.py

def test_simulation_package_importable():
    import simulation
    from simulation import Elevator, Motor, Door, Controller, ElevatorSystem

    # Opcional: una aserción muy básica para usar los símbolos y que Pylance no los marque como no usados
    assert Elevator is simulation.Elevator
    assert Motor    is simulation.Motor
    assert Door     is simulation.Door
    assert Controller is simulation.Controller
    assert ElevatorSystem is simulation.ElevatorSystem
