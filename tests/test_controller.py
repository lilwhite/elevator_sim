# tests/test_controller.py
import pytest
from simulation.controller import Controller
from simulation.elevator import Elevator
from simulation.floor_panel import FloorPanel
from simulation.logger import Logger

@pytest.fixture
def setup_controller():
    # Configuración básica: edificio de pisos 1 a 5
    elevator = Elevator(id=1, min_floor=1, max_floor=5)
    panels = [FloorPanel(id=i, floor=i, min_floor=1, max_floor=5) for i in range(1, 6)]
    logger = Logger(timestamp_fn=lambda: 0.0)
    controller = Controller(id=1, elevator=elevator, floor_panels=panels, logger=logger)
    return controller


def test_add_external_request_and_get_active_calls(setup_controller):
    ctrl = setup_controller
    ctrl.add_external_request(3)
    assert ctrl.get_active_calls() == [3]


def test_add_internal_request_and_get_active_calls(setup_controller):
    ctrl = setup_controller
    ctrl.add_internal_request(4)
    assert ctrl.get_active_calls() == [4]


def test_handle_requests_moves_to_elevator_targets(setup_controller):
    ctrl = setup_controller
    ctrl.add_external_request(2)
    ctrl.add_internal_request(5)
    ctrl.handle_requests()
    # Tras manejar, pending_requests debe vaciarse
    assert ctrl.get_active_calls() == []
    # El ascensor debe tener ambas peticiones
    assert 2 in ctrl.elevator.target_floors
    assert 5 in ctrl.elevator.target_floors


def test_run_tick_processes_requests_and_moves_elevator(setup_controller):
    ctrl = setup_controller
    # Llamada externa desde piso 3
    ctrl.add_external_request(3)
    # Ejecutar tick: debe procesar solicitudes y luego mover
    ctrl.run_tick(dt=1.0)
    # La solicitud 3 se habrá enviado al ascensor
    assert 3 in ctrl.elevator.target_floors
    # Después de step de 1s, el ascensor debería moverse hacia 3: current_floor 1->2
    assert ctrl.elevator.current_floor != 1
    # Y la solicitud debería seguir en target_floors hasta llegar completo
    assert 3 in ctrl.elevator.target_floors


def test_log_event_records_to_logger(setup_controller):
    ctrl = setup_controller
    ctrl.log_event("Evento de prueba")
    history = ctrl.logger.show_history()
    assert any("Evento de prueba" in entry for entry in history)


def test_reset_clears_state(setup_controller):
    ctrl = setup_controller
    ctrl.add_external_request(2)
    ctrl.reset()
    assert ctrl.get_active_calls() == []
    assert ctrl.elevator.target_floors == []
