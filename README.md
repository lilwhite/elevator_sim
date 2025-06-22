# 🛗 Simulador de Sistema de Ascensores

Este proyecto modela un sistema realista de ascensores utilizando programación orientada a objetos. Se centra en la modularidad, escalabilidad y capacidad de simulación paso a paso. El sistema está diseñado para soportar múltiples ascensores, usuarios, sensores y controladores, con posibilidad de extensión a simulaciones más complejas o visualización en CLI.

---

[![CI](https://github.com/lilwhite/elevator_sim/actions/workflows/ci-python.yml/badge.svg)](https://github.com/lilwhite/elevator_sim/actions/workflows/ci-python.yml)
[![Lint](https://github.com/lilwhite/elevator_sim/actions/workflows/pylint.yml/badge.svg)](https://github.com/lilwhite/elevator_sim/actions/workflows/pylint.yml)
[![Python Version](https://img.shields.io/badge/python-3.13.5-blue)](https://www.python.org/)

---

# 🗂️ Estructura del proyecto

```
elevator_sim/
├── README.md                # Descripción general del proyecto
├── requirements.txt         # Dependencias
├── main.py                  # Punto de entrada de la simulación
├── simulation/              # Módulo principal del sistema de simulación
│   ├── __init__.py
│   ├── controller.py        # Clase Controller
│   ├── elevator.py          # Clase Elevator (orquesta Motor, Door, etc.)
│   ├── motor.py             # Clase Motor
│   ├── door.py              # Clase Door
│   ├── display.py           # Clase Display
│   ├── sensor.py            # Clase Sensor
│   ├── floor_panel.py       # Clase FloorPanel
│   ├── logger.py            # Clase Logger
│   ├── user.py              # Clase User
│   ├── elevator_system.py   # Clase ElevatorSystem (gestión global del edificio)
│   └── utils.py             # Constantes, validaciones, funciones auxiliares
├── tests/                   # Carpeta para tests con pytest
│   ├── __init__.py
│   ├── test_elevator.py
│   ├── test_controller.py
│   ├── test_user.py
│   └── ... otros tests
└── assets/                  # Recursos no ejecutables
    └── diagrams/            # Diagramas UML, capturas, documentación visual
```


## 🧱 Estructura del sistema

![Diagrama UML](assets/diagrams/uml.jpg)

| Clase           | Descripción breve | Estado |
|------------------|-------------------|--------|
| `Elevator`       | Representa el ascensor: controla su posición, carga, puertas, dirección y solicitudes. | ✅ |
| `Motor`          | Gestiona el movimiento del ascensor (velocidad, dirección, frenado). | ✅ |
| `Door`           | Controla el estado de apertura/cierre de las puertas del ascensor. | ✅ |
| `Display`        | Muestra la información visual del ascensor (piso actual, dirección, errores). | ✅ |
| `Sensor`         | Representa un sensor individual: peso, posición, presencia, etc. | ✅ |
| `User`           | Modela a un usuario que llama al ascensor y selecciona un destino. | ✅ |
| `FloorPanel`     | Panel de llamada externa en cada piso con botones de subida/bajada y luces. | ✅ |
| `Logger`         | Registra eventos y acciones del sistema para trazabilidad y depuración. | ✅ |
| `Controller`     | Orquesta la lógica de movimiento del ascensor y gestiona las solicitudes. | ✅ |
| `ElevatorSystem` | Representa el edificio completo: múltiples ascensores, usuarios, controladores y paneles. | ✅ |

---

## 📌 Características principales

- ✔️ Simulación por pasos (`dt`) del comportamiento del sistema
- ✔️ Gestión de usuarios y flujos realistas (espera, carga, destino)
- ✔️ Lógica de control modular y extensible
- ✔️ Soporte para múltiples ascensores
- ✔️ Registros de eventos con trazabilidad completa
- ✔️ Preparado para pruebas unitarias y futura visualización en CLI

---

## 🚧 Próximas extensiones sugeridas

- Asignación inteligente de ascensores (basado en carga, proximidad, tiempo estimado)
- Simulación basada en eventos programados (horas punta, tráfico)
- Representación visual animada (CLI o interfaz gráfica)




## 🏢 Clase `ElevatorSystem`

### 📦 Atributos

| Nombre             | Tipo                  | Descripción |
|--------------------|-----------------------|-------------|
| `elevators`        | `list[Elevator]`      | Lista de ascensores gestionados por el sistema. |
| `controllers`      | `list[Controller]`    | Lista de controladores (uno por ascensor o compartidos). |
| `floor_panels`     | `dict[int, FloorPanel]` | Paneles de llamada por piso (clave = número de piso). |
| `users`            | `list[User]`          | Lista global de usuarios en el edificio. |
| `logger`           | `Logger`              | Sistema de logging común para todos los componentes. |
| `min_floor`        | `int`                 | Piso mínimo del edificio. |
| `max_floor`        | `int`                 | Piso máximo del edificio. |
| `time`             | `float`               | Tiempo acumulado de simulación global. |

---

### 🛠️ Métodos

| Método                          | Descripción |
|----------------------------------|-------------|
| `add_elevator(elevator: Elevator, controller: Controller)` | Añade un ascensor con su controlador correspondiente. |
| `add_user(user: User)`          | Añade un usuario al sistema. |
| `run_tick(dt: float)`           | Ejecuta un ciclo de simulación para todos los componentes. |
| `dispatch_request(floor: int, direction: str)` | Lógica para asignar el mejor ascensor a una llamada externa. |
| `get_elevator_status() -> list[dict]` | Devuelve información resumida de todos los ascensores (piso, dirección, carga, etc.). |
| `reset()`                       | Reinicia el estado completo del sistema. |
| `populate_panels()`            | Genera los `FloorPanel` automáticamente por piso. |

---

### 🧠 Consideraciones

- Esta clase te permite trabajar en simulaciones de edificios **reales o complejos**, con varios ascensores y flujos de tráfico.
- Si usas un único `Controller`, puede coordinar todos los ascensores como un sistema centralizado.
- Si cada `Elevator` tiene su propio `Controller`, el sistema puede distribuir peticiones como haría un rascacielos real.


## 🎮 Clase `Controller`

### 📦 Atributos

| Nombre           | Tipo             | Descripción |
|------------------|------------------|-------------|
| `id`             | `int`            | Identificador único del controlador. Útil para escalado, trazabilidad y depuración. |
| `elevator`       | `Elevator`       | Instancia del ascensor gestionado. |
| `users`          | `list[User]`     | Lista de usuarios activos en la simulación. |
| `floor_panels`   | `list[FloorPanel]` | Lista de paneles de llamada externa, uno por piso. |
| `logger`         | `Logger`         | Sistema de registro de eventos. |
| `time`           | `float`          | Tiempo acumulado de simulación. |
| `pending_requests` | `list[int]`    | Lista de pisos con llamadas externas pendientes. |

---

### 🛠️ Métodos

| Método                         | Descripción |
|--------------------------------|-------------|
| `run_tick(dt: float)`          | Avanza un ciclo de simulación de `dt` segundos. |
| `handle_requests()`            | Procesa las llamadas externas e internas pendientes. |
| `add_external_request(floor: int)` | Añade una solicitud de llamada desde un panel exterior. |
| `add_internal_request(floor: int)` | Añade una solicitud desde dentro del ascensor. |
| `update_users()`               | Gestiona las acciones de los usuarios (entrar, salir, llamar). |
| `log_event(event: str)`        | Envía un evento al logger. |
| `reset()`                      | Reinicia el controlador a su estado inicial. |
| `get_active_calls() -> list[int]` | Devuelve los pisos que han solicitado el ascensor. |

---

### 🧠 Consideraciones

- Este controlador es **el "cerebro"** del sistema: toma decisiones, interpreta acciones y activa el comportamiento de `Elevator`, `Door`, `Motor`, etc.
- El método `run_tick(dt)` podría ser llamado en un bucle para simular el paso del tiempo (por segundos, por ejemplo).
- `update_users()` puede manejar lógica como: si el ascensor ha llegado, el usuario entra o sale.
- Puede extenderse a múltiples ascensores en versiones futuras añadiendo una lista de instancias `Elevator`.



## 🛗 Clase `Elevator`

### 📦 Atributos

| Nombre              | Tipo                | Descripción                                                                 |
|---------------------|---------------------|-----------------------------------------------------------------------------|
| `id`                | `int`               | Identificador único del ascensor.                                          |
| `min_floor`         | `int`               | Piso mínimo accesible.                                                     |
| `max_floor`         | `int`               | Piso máximo accesible.                                                     |
| `current_floor`     | `int`               | Piso actual donde se encuentra.                                            |
| `target_floors`     | `list[int]`         | Lista de pisos destino pendientes.                                         |
| `direction`         | `str`               | Dirección actual: `"up"`, `"down"` o `"idle"`.                             |
| `is_moving`         | `bool`              | Indica si el ascensor está desplazándose.                                 |
| `door_status`       | `str`               | Estado de la puerta: `"open"`, `"closed"`, `"opening"`, `"closing"`.      |
| `door_timer`        | `float`             | Tiempo restante para mantener la puerta abierta antes de cerrarse.        |
| `speed_mps`         | `float`             | Velocidad del ascensor en metros por segundo.                              |
| `position_m`        | `float`             | Posición vertical continua (en metros).                                    |
| `weight_limit_kg`   | `float`             | Límite máximo de carga permitida.                                          |
| `current_weight_kg` | `float`             | Carga actual detectada en la cabina.                                       |
| `emergency_state`   | `bool`              | Indica si se encuentra en modo de emergencia.                              |
| `motor`             | `Motor`             | Referencia al motor responsable del movimiento.                            |
| `door`              | `Door`              | Instancia del sistema de puertas del ascensor.                             |
| `sensors`           | `list[Sensor]`      | Lista de sensores instalados.                                              |
| `display`           | `Display`           | Pantalla que indica estado, dirección y piso.                              |
| `logger`            | `Logger`            | Sistema de log para registrar eventos.                                     |

---

### 🛠️ Métodos

| Método                       | Descripción |
|-----------------------------|-------------|
| `call(floor: int)`          | Solicitud externa de un usuario desde un piso. |
| `select_floor(floor: int)`  | Solicitud interna desde dentro del ascensor. |
| `step(dt: float)`           | Avanza el estado interno del ascensor según el tiempo. |
| `move_towards_target()`     | Ejecuta movimiento hacia el siguiente piso destino. |
| `open_door()`               | Inicia la secuencia de apertura de puertas. |
| `close_door()`              | Inicia la secuencia de cierre de puertas. |
| `check_overload() -> bool`  | Verifica si se excede el peso máximo permitido. |
| `update_direction()`        | Establece la dirección según los pisos pendientes. |
| `activate_emergency()`      | Detiene el sistema y trata de abrir las puertas. |
| `reset_emergency()`         | Restaura el sistema tras una emergencia. |
| `is_idle() -> bool`         | Devuelve `True` si no hay solicitudes pendientes. |

### 🧠 Consideraciones

- La position_m puede permitir una simulación más fina (movimiento entre pisos).
- El uso de step(dt) permite simular la evolución en tiempo real.
- El logger puede registrar eventos como: llegada a piso, apertura de puertas, peso excedido, emergencia, etc.

## 🧩 Clase `Motor`

### 📦 Atributos

| Nombre            | Tipo       | Descripción |
|-------------------|------------|-------------|
| `id`              | `int`      | Identificador único del motor. |
| `current_speed`   | `float`    | Velocidad actual del motor (en m/s). |
| `target_speed`    | `float`    | Velocidad objetivo que debe alcanzar. |
| `acceleration`    | `float`    | Aceleración del motor (en m/s²). |
| `max_speed`       | `float`    | Velocidad máxima permitida (en m/s). |
| `direction`       | `str`      | Dirección actual del movimiento: `"up"`, `"down"` o `"stopped"`. |
| `position_m`      | `float`    | Posición continua que representa el desplazamiento vertical. |
| `braking`         | `bool`     | Indica si el motor está frenando. |
| `power_on`        | `bool`     | Estado de encendido del motor. |

---

### 🛠️ Métodos

| Método                           | Descripción |
|----------------------------------|-------------|
| `set_target_speed(speed: float)` | Define una nueva velocidad objetivo (ej. para acelerar). |
| `set_direction(dir: str)`        | Establece dirección (`"up"` o `"down"`). |
| `start()`                        | Activa el motor, comenzando movimiento hacia la velocidad objetivo. |
| `stop()`                         | Detiene el motor (desacelera y pone velocidad a 0). |
| `brake()`                        | Aplica frenado de emergencia si hay incidente. |
| `update(dt: float)`              | Actualiza la velocidad y la posición según el paso de tiempo. |
| `is_idle() -> bool`              | Retorna `True` si el motor está parado. |
| `get_position() -> float`        | Devuelve la posición vertical actual. |

### 🧠 Consideraciones

- El método update(dt) permite simular un movimiento físico progresivo (con aceleración y frenado).
- Se puede incluir lógica de "parada suave" si la distancia al destino es corta.
- La integración con Elevator permite saber si ha llegado a un piso entero comparando position_m.



## 🚪 Clase `Door`

### 📦 Atributos

| Nombre            | Tipo       | Descripción |
|-------------------|------------|-------------|
| `id`              | `int`      | Identificador único de la puerta. |
| `status`          | `str`      | Estado actual: `"open"`, `"closed"`, `"opening"`, `"closing"`. |
| `timer`           | `float`    | Tiempo restante (en segundos) para completar la acción actual. |
| `open_duration`   | `float`    | Tiempo total que debe estar abierta la puerta antes de cerrarse automáticamente. |
| `blocked`         | `bool`     | Indica si la puerta está bloqueada (por objeto o sensor de seguridad). |
| `auto_close`      | `bool`     | Indica si debe cerrarse automáticamente tras abrirse. |
| `emergency_locked`| `bool`     | Indica si la puerta ha sido bloqueada manualmente por emergencia. |

---

### 🛠️ Métodos

| Método                     | Descripción |
|----------------------------|-------------|
| `open()`                   | Inicia la apertura de la puerta. Cambia `status` a `"opening"`. |
| `close()`                  | Inicia el cierre de la puerta. Cambia `status` a `"closing"`. |
| `force_open()`             | Abre la puerta ignorando condiciones normales (emergencia). |
| `lock_emergency()`         | Bloquea la puerta por estado de emergencia (no permite cerrar). |
| `unlock_emergency()`       | Desbloquea la puerta tras el estado de emergencia. |
| `set_blocked(value: bool)` | Establece el estado de bloqueo por sensor. |
| `tick(dt: float)`          | Avanza el tiempo de apertura/cierre y cambia el estado cuando termina. |
| `is_open() -> bool`        | Retorna `True` si la puerta está completamente abierta. |
| `is_closed() -> bool`      | Retorna `True` si la puerta está completamente cerrada. |
| `is_moving() -> bool`      | Retorna `True` si la puerta está en movimiento. |

---

### 🧠 Consideraciones

- La función `tick(dt)` permite simular la apertura o cierre gradual de puertas.
- La puerta no debería cerrarse si `blocked` es `True` o si el sensor de presencia detecta movimiento.
- El atributo `emergency_locked` impide cualquier acción hasta que se resuelva la emergencia.

## 🖥️ Clase `Display`

### 📦 Atributos

| Nombre           | Tipo      | Descripción |
|------------------|-----------|-------------|
| `id`             | `int`     | Identificador único del display. |
| `current_floor`  | `int`     | Piso que se está mostrando actualmente. |
| `direction`      | `str`     | Dirección mostrada: `"↑"` (subiendo), `"↓"` (bajando), `"—"` (reposo). |
| `door_status`    | `str`     | Estado mostrado de la puerta: `"open"`, `"closed"`, `"moving"`. |
| `error_message`  | `str`     | Mensaje de error o aviso especial en caso de emergencia o sobrepeso. |
| `mode`           | `str`     | `"internal"` si es de cabina, `"external"` si es de planta. |

---

### 🛠️ Métodos

| Método                           | Descripción |
|----------------------------------|-------------|
| `update_floor(floor: int)`       | Actualiza el piso mostrado. |
| `update_direction(dir: str)`     | Actualiza el símbolo o texto de dirección. |
| `update_door(status: str)`       | Muestra el estado de la puerta. |
| `show_error(msg: str)`           | Muestra un mensaje de error o advertencia. |
| `clear_error()`                  | Limpia el mensaje de error actual. |
| `render() -> str`                | Devuelve una representación visual del display para impresión/logs. |

---

### 🧠 Consideraciones

- La distinción entre `internal` y `external` permite mostrar diferente información (por ejemplo, el externo no necesita `door_status`).
- En una implementación avanzada, `render()` podría devolver un string formateado con íconos o caracteres especiales para representar el estado en consola o interfaz gráfica.
- Puede integrarse con sonidos o luces si se quisiera simular accesibilidad.


## 📡 Clase `Sensor`

### 📦 Atributos

| Nombre         | Tipo       | Descripción |
|----------------|------------|-------------|
| `id`           | `int`      | Identificador único del sensor. |
| `type`         | `str`      | Tipo de sensor: `"weight"`, `"presence"`, `"position"`, `"door"`, `"floor"`, etc. |
| `value`        | `float`/`bool`/`int` | Valor actual registrado por el sensor. El tipo depende del sensor. |
| `unit`         | `str`      | Unidad de medida asociada (por ejemplo, `"kg"`, `"m"`, `"bool"`). |
| `threshold`    | `float`    | Umbral crítico para activar una alerta o condición (por ejemplo, peso máximo). |
| `active`       | `bool`     | Indica si el sensor está habilitado y funcionando. |
| `last_updated` | `float`    | Timestamp o contador de tiempo desde la última actualización. |

---

### 🛠️ Métodos

| Método                          | Descripción |
|---------------------------------|-------------|
| `read() -> float|bool|int`      | Devuelve el valor actual del sensor. |
| `update(value: any)`            | Actualiza el valor del sensor manual o automáticamente. |
| `is_triggered() -> bool`        | Retorna `True` si el valor supera el umbral (`threshold`), si aplica. |
| `calibrate(offset: float)`      | Ajusta el valor base del sensor (por ejemplo, para peso o posición). |
| `enable()`                      | Activa el sensor. |
| `disable()`                     | Desactiva temporalmente el sensor. |
| `reset()`                       | Reinicia el valor del sensor a su estado por defecto. |

---

### 🧠 Consideraciones

- Esta clase puede actuar como base para sensores más específicos (`WeightSensor`, `ProximitySensor`, etc.) mediante herencia.
- El método `is_triggered()` es útil para sensores con lógica de alerta (ej. sobrepeso, intrusión, bloqueo de puerta).
- Puede integrarse con el logger para registrar cambios críticos o anomalías.


## 🧾 Clase `Logger`

### 📦 Atributos

| Nombre        | Tipo          | Descripción |
|----------------|---------------|-------------|
| `logs`         | `list[str]`   | Lista de entradas de log en formato de texto plano. |
| `enabled`      | `bool`        | Indica si el logger está activo o silenciado. |
| `log_level`    | `str`         | Nivel de detalle del log: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`. |
| `timestamp_fn` | `Callable`    | Función para obtener el tiempo actual (útil para simular o testear). |

---

### 🛠️ Métodos

| Método                               | Descripción |
|--------------------------------------|-------------|
| `log(message: str, level: str = "INFO")` | Agrega una nueva entrada al log si el nivel cumple con el `log_level`. |
| `show_history(n: int = None) -> list[str]` | Devuelve la lista de los últimos `n` eventos registrados. Si `n` es `None`, devuelve todos. |
| `clear()`                            | Limpia todos los registros del log. |
| `enable()`                           | Activa el sistema de log. |
| `disable()`                          | Desactiva el sistema de log temporalmente. |
| `set_level(level: str)`              | Cambia el nivel mínimo de severidad que se registrará. |
| `export(path: str)`                  | Exporta los logs a un archivo de texto en disco. (Opcional en simulación) |

---

### 🧠 Consideraciones

- Ideal para registrar eventos del ascensor: llamadas, llegadas, errores, aperturas de puerta, sobrepeso, etc.
- El atributo `timestamp_fn` permite simular un reloj en sistemas sin acceso a `datetime.now()` (útil en entornos de prueba).
- Podría extenderse para soportar múltiples formatos de salida: consola, archivo, base de datos, etc.


## 🙋 Clase `User`

### 📦 Atributos

| Nombre               | Tipo        | Descripción |
|----------------------|-------------|-------------|
| `id`                 | `int`       | Identificador único del usuario. |
| `current_floor`      | `int`       | Piso donde se encuentra actualmente. |
| `destination_floor`  | `int`       | Piso al que desea ir. |
| `inside_elevator`    | `bool`      | Indica si el usuario está dentro del ascensor. |
| `waiting`            | `bool`      | Indica si el usuario está esperando al ascensor. |
| `weight_kg`          | `float`     | Peso del usuario, usado para el cálculo de carga. |

---

### 🛠️ Métodos

| Método                            | Descripción |
|-----------------------------------|-------------|
| `call_elevator(direction: str)`   | Llama al ascensor desde su piso (`"up"` o `"down"`). |
| `enter_elevator()`                | Marca que el usuario ha entrado al ascensor. |
| `select_floor(floor: int)`        | Pulsa el botón del piso destino dentro del ascensor. |
| `exit_elevator()`                 | Marca que el usuario ha salido del ascensor. |
| `wait_for_elevator()`             | Cambia el estado a `waiting = True`. |

---

### 🧠 Consideraciones

- Puedes añadir `trip_started_at` y `trip_ended_at` más adelante si quieres medir tiempos de viaje.
- Esta versión es suficiente para representar el flujo clásico: llama, entra, selecciona piso, sale.
- Puede integrarse fácilmente con una lógica de simulación de comportamiento por turnos o por eventos.


## 🔲 Clase `FloorPanel`

### 📦 Atributos

| Nombre             | Tipo     | Descripción |
|--------------------|----------|-------------|
| `id`               | `int`    | Identificador único del panel. |
| `floor`            | `int`    | Piso al que está asociado el panel. |
| `up_pressed`       | `bool`   | Indica si el botón de subida ha sido presionado. |
| `down_pressed`     | `bool`   | Indica si el botón de bajada ha sido presionado. |
| `indicator_up`     | `bool`   | Luz indicadora encendida para "subida". |
| `indicator_down`   | `bool`   | Luz indicadora encendida para "bajada". |
| `has_up_button`    | `bool`   | Indica si el panel tiene botón de subida. Desactivado en el último piso. |
| `has_down_button`  | `bool`   | Indica si el panel tiene botón de bajada. Desactivado en el primer piso. |

---

### 🛠️ Métodos

| Método                              | Descripción |
|-------------------------------------|-------------|
| `press_up()`                        | Marca el botón de subida como presionado y enciende la luz, solo si `has_up_button` es `True`. |
| `press_down()`                      | Marca el botón de bajada como presionado y enciende la luz, solo si `has_down_button` es `True`. |
| `reset_up()`                        | Apaga la luz de subida y resetea el estado. |
| `reset_down()`                      | Apaga la luz de bajada y resetea el estado. |
| `is_active() -> bool`               | Devuelve `True` si alguno de los botones está presionado. |
| `get_requested_directions() -> list[str]` | Devuelve una lista con los botones activos (`["up"]`, `["down"]`, o ambos). |

---

### 🧠 Consideraciones

- El constructor debe recibir `min_floor` y `max_floor` para determinar automáticamente si el panel debe tener botón de subida o bajada.
- Por ejemplo:
  - Si `floor == min_floor` → `has_down_button = False`
  - Si `floor == max_floor` → `has_up_button = False`
- Este diseño protege contra errores de uso y permite mayor realismo en la simulación.


