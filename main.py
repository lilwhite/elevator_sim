#!/usr/bin/env python3
"""
main.py

Punto de entrada para la simulación del sistema de ascensores.
Usa los símbolos exportados en simulation/__init__.py para imports más sencillos.
"""

import time
from simulation import ElevatorSystem, Elevator, Controller, User

def main():
    # 1. Crear el sistema para un edificio de 1 a 10
    sim = ElevatorSystem(min_floor=1, max_floor=10)
    sim.populate_panels()

    # 2. Añadir un ascensor con su controlador
    elev = Elevator(id=1, min_floor=sim.min_floor, max_floor=sim.max_floor)
    ctrl = Controller(
        id=1,
        elevator=elev,
        floor_panels=list(sim.floor_panels.values()),
        logger=sim.logger
    )
    sim.add_elevator(elev, ctrl)

    # 3. Crear un usuario de prueba y llamar al ascensor
    user = User(id=1, weight_kg=70.0, current_floor=1)
    sim.add_user(user)
    user.call_elevator("up")

    # 4. Bucle de simulación
    dt = 1.0  # segundos por tick
    max_ticks = 20
    print("Iniciando simulación...")
    for _ in range(max_ticks):
        sim.run_tick(dt)
        status = sim.get_elevator_status()
        print(f"[t={sim.time:.1f}s] Estado ascensores:", status)
        time.sleep(0.5)

    print("Simulación finalizada.")

if __name__ == "__main__":
    main()

