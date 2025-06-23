#!/usr/bin/env python3
"""
main.py

Simulación dinámica de un ascensor con generación aleatoria de usuarios
y trazabilidad completa del proceso: llamada externa, llegada,
entradas/salidas detectando peso y cierre de puertas.
"""

import random
from simulation.elevator_system import ElevatorSystem
from simulation.elevator        import Elevator
from simulation.controller      import Controller
from simulation.user            import User


def setup_system(min_floor: int, max_floor: int) -> ElevatorSystem:
    """Inicializa y devuelve un ElevatorSystem con todos los FloorPanels."""
    system = ElevatorSystem(min_floor=min_floor, max_floor=max_floor)
    system.populate_panels()
    return system


def setup_elevators(
    system: ElevatorSystem,
    specs: list[dict]
) -> None:
    """Añade instancias de Elevator y Controller al sistema."""
    for spec in specs:
        elev = Elevator(
            system=system,
            id=spec["id"],
            min_floor=spec.get("min_floor", system.min_floor),
            max_floor=spec.get("max_floor", system.max_floor),
            speed_mps=spec.get("speed", 1.0)
        )
        ctrl = Controller(
            id=spec["id"],
            elevator=elev,
            floor_panels=list(system.floor_panels.values()),
            logger=system.logger
        )
        system.add_elevator(elev, ctrl)


def generate_user_events(
    num_users: int,
    min_floor: int,
    max_floor: int,
    total_time: float,
    dt: float
) -> list[dict]:
    """
    Crea eventos de usuarios: tiempo de aparición, id, peso, origen y destino.
    """
    events = []
    for uid in range(1, num_users + 1):
        origin = random.randint(min_floor, max_floor)
        dest_choices = [f for f in range(min_floor, max_floor + 1) if f != origin]
        dest = random.choice(dest_choices)
        max_tick = int(total_time / dt)
        tick = random.randint(0, max_tick)
        event_time = tick * dt
        weight = random.uniform(50.0, 90.0)
        events.append({
            "time": event_time,
            "id": uid,
            "weight": weight,
            "origin": origin,
            "dest": dest,
            "dispatched": False
        })
    return sorted(events, key=lambda e: e["time"])


def update_displays(system: ElevatorSystem) -> None:
    """Sincroniza y muestra todos los Displays, peso y usuarios dentro."""
    for ctrl in system.controllers:
         elev = ctrl.elevator
         disp = elev.display
         # Actualizar display básico
         disp.update_floor(elev.current_floor)
         arrow = {"up": "↑", "down": "↓"}.get(elev.direction, "—")
         disp.update_direction(arrow)
         disp.update_door(elev.door.status)
         # 1) Calcula quién está dentro y su peso
         inside = [(u.id, u.weight_kg) for u in ctrl.users if u.inside_elevator]
         inside_str = ", ".join(f"User{uid}({w:.1f}kg)" for uid, w in inside) or "None"

         # 2) Imprime display + peso + listado de pasajeros
         print(
                f"[Display E{elev.id}] {disp.render()} "
                f"| TotalWeight: {elev.current_weight_kg:.1f}kg "
                f"| Inside: {inside_str}"
            )


def run_simulation(
    system: ElevatorSystem,
    steps: int,
    dt: float,
    events: list[dict]
) -> None:
    """Bucle principal: inyecta usuarios, procesa ticks y muestra logs y estados."""
    total_time = steps * dt
    # Mostrar configuración inicial
    print("====== CONFIGURACIÓN DE SIMULACIÓN ======")
    print(f"Floors: {system.min_floor} to {system.max_floor}")
    print(f"Ticks: {steps}  |  dt: {dt}s  |  Total Time: {total_time}s")
    print(f"Num Users: {len(events)}")
    # Mostrar planta inicial de cada usuario
    print("Usuarios (ID@Origen -> Destino):")
    for evt in events:
        print(f"  User{evt['id']}@{evt['origin']} -> {evt['dest']}")
    print("========================================\n")

    log_index = 0
    for tick in range(1, steps + 1):
        # 1) Avanzar simulación
        system.run_tick(dt)

        # 1.5) Procesar las interacciones usuario ↔ ascensor
        for ctrl in system.controllers:
            ctrl.update_users()

        # 2) Inyectar nuevos usuarios
        for evt in events:
            if not evt["dispatched"] and evt["time"] <= system.time:
                print(
                    f"[t={system.time:.1f}s] Usuario{evt['id']} aparece en piso {evt['origin']} "
                    f"(destino {evt['dest']}, peso {evt['weight']:.1f}kg)"
                )
                user = User(
                    id=evt['id'],
                    weight_kg=evt['weight'],
                    current_floor=evt['origin']
                )
                user.call_elevator(
                    direction="up" if evt['dest'] > evt['origin'] else "down"
                )
                system.add_user(user)
                # calcula la dirección como string
                dir_str = "up" if evt["dest"] > evt["origin"] else "down"
                # marca la llamada externa
                system.dispatch_request(
                    user.current_floor,
                    dir_str
                )
                user.select_floor(evt['dest'])
                evt['dispatched'] = True

        # 3) Mostrar nuevos logs
        new_logs = system.logger.logs[log_index:]
        for entry in new_logs:
            print(entry)
        log_index = len(system.logger.logs)

        # 4) Actualizar peso en cabina
        for ctrl in system.controllers:
            elev = ctrl.elevator
            elev.current_weight_kg = sum(
                u.weight_kg for u in ctrl.users if u.inside_elevator
            )

        # 5) Mostrar estado actual
        print(f"-- Tick {tick}/{steps} (t={system.time:.1f}s) --")
        update_displays(system)
        print("" + "-" * 60)

    print("\nSimulación completada.")


def main() -> None:
    # Parámetros de configuración
    MIN_FLOOR, MAX_FLOOR = 1, 10
    STEPS = 200
    DT = 0.5
    NUM_USERS = 5

    # 1) Inicializar sistema
    system = setup_system(MIN_FLOOR, MAX_FLOOR)

    # 2) Crear ascensores
    specs = [{"id": 1, "min_floor": MIN_FLOOR, "max_floor": MAX_FLOOR, "speed": 1.0}]
    setup_elevators(system, specs)

    # 3) Generar eventos de usuario
    events = generate_user_events(NUM_USERS, MIN_FLOOR, MAX_FLOOR, STEPS * DT, DT)

    # 4) Ejecutar simulación dinámica
    run_simulation(system, STEPS, DT, events)


if __name__ == "__main__":
    main()
