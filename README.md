# EventPro – Sistema de Gestión para Eventos y Convenciones
**Espacios Magníficos S.A.** | Marzo 2026

---

## 1. Descripción del Proyecto

EventPro es un sistema de escritorio desarrollado en **Python** con interfaz gráfica **Tkinter**, diseñado para gestionar las operaciones del centro de convenciones Espacios Magníficos S.A. El sistema permite administrar recintos, clientes, eventos y personal de manera integrada, conectándose a una base de datos **MySQL** mediante **Stored Procedures**.

---

## 2. Requisitos Técnicos Cumplidos

| Requisito | Cumplimiento |
|---|---|
| Estructura modular (mín. 4) | 4 módulos: Recintos, Clientes, Eventos, Personal |
| Base de datos | MySQL – base de datos `eventpro` con 4 tablas |
| Integración completa | Python ↔ MySQL via Stored Procedures (20 SP) |
| Interfaz gráfica | Tkinter con formularios, búsqueda y CRUD completo |

---

## 3. Módulos del Sistema

| Módulo | Descripción | Tabla BD |
|---|---|---|
| Recintos | Gestión de espacios físicos del centro | `Recintos` |
| Clientes | Registro de clientes corporativos y particulares | `Clientes` |
| Eventos | Programación y control de eventos | `Eventos` |
| Personal | Administración del personal asignado | `Personal` |

### 3.1 Módulo Recintos
Permite registrar y gestionar los espacios físicos disponibles en el centro de convenciones. Cada recinto se identifica con un código único y almacena información sobre su tipo, ubicación, capacidad y disponibilidad.

### 3.2 Módulo Clientes
Administra el registro de clientes del centro, diferenciando entre clientes corporativos, agencias y particulares. Permite clasificarlos por volumen y registrar su información de contacto completa.

### 3.3 Módulo Eventos
Gestiona la programación de eventos, asociando cada evento a un cliente y permitiendo controlar su estado desde la cotización hasta la finalización.

### 3.4 Módulo Personal
Controla el personal disponible para la atención de eventos, incluyendo su especialidad, disponibilidad y asignación a eventos específicos.

---

## 4. Estructura de la Base de Datos

- **Base de datos:** `eventpro`
- **Motor:** MySQL 8.4
- **Servidor:** `localhost:3306`

### Tabla Recintos
| Campo | Tipo | Descripción |
|---|---|---|
| codigo_recinto | VARCHAR(10) | Clave primaria |
| nombre | VARCHAR(100) | Nombre del recinto |
| tipo | VARCHAR(30) | Salón / Auditorio / Sala de reuniones |
| ubicacion | VARCHAR(100) | Ubicación dentro del complejo |
| capacidad_teatro | INT | Número máximo de personas |
| tarifa | VARCHAR(50) | Tarifa por hora o día |
| disponibilidad | VARCHAR(30) | Disponible / Reservado / En mantenimiento |

### Tabla Clientes
| Campo | Tipo | Descripción |
|---|---|---|
| codigo_cliente | VARCHAR(10) | Clave primaria |
| tipo_cliente | VARCHAR(20) | Corporativo / Agencia / Particular |
| razon_social | VARCHAR(100) | Nombre o razón social |
| documento_fiscal | VARCHAR(20) | NIT / RUT / Cédula |
| telefono | VARCHAR(20) | Número de contacto |
| correo | VARCHAR(80) | Correo electrónico |
| contacto | VARCHAR(80) | Persona de contacto |
| clasificacion | VARCHAR(30) | Nuevo / Frecuente / VIP |

### Tabla Eventos
| Campo | Tipo | Descripción |
|---|---|---|
| num_evento | VARCHAR(15) | Clave primaria |
| titulo | VARCHAR(100) | Título del evento |
| tipo_evento | VARCHAR(30) | Congreso / Boda / Feria / Concierto / Conferencia |
| cliente | VARCHAR(100) | Cliente asociado |
| fecha_inicio | VARCHAR(20) | Fecha y hora de inicio |
| fecha_fin | VARCHAR(20) | Fecha y hora de fin |
| num_asistentes | INT | Número estimado de asistentes |
| estado | VARCHAR(20) | Cotización / Confirmado / En curso / Finalizado |

### Tabla Personal
| Campo | Tipo | Descripción |
|---|---|---|
| codigo_empleado | VARCHAR(10) | Clave primaria |
| nombres | VARCHAR(60) | Nombres del empleado |
| apellidos | VARCHAR(60) | Apellidos del empleado |
| especialidad | VARCHAR(40) | Coordinador / Técnico / Camarero / Seguridad... |
| tarifa | VARCHAR(50) | Tarifa aplicable |
| evento_asignado | VARCHAR(100) | Evento al que está asignado |
| horario | VARCHAR(40) | Horario de trabajo |
| disponibilidad | VARCHAR(30) | Disponible / Asignado / De vacaciones |

---

## 5. Stored Procedures

El sistema utiliza **20 Stored Procedures** (5 por módulo) para toda la comunicación con la base de datos.

| Stored Procedure | Operación | Descripción |
|---|---|---|
| sp_insertar_recinto | INSERT | Agrega un nuevo recinto |
| sp_actualizar_recinto | UPDATE | Modifica datos de un recinto |
| sp_eliminar_recinto | DELETE | Elimina un recinto por código |
| sp_buscar_recinto | SELECT | Busca por código o nombre |
| sp_listar_recintos | SELECT | Lista todos los recintos |
| sp_insertar_cliente | INSERT | Agrega un nuevo cliente |
| sp_actualizar_cliente | UPDATE | Modifica datos de un cliente |
| sp_eliminar_cliente | DELETE | Elimina un cliente por código |
| sp_buscar_cliente | SELECT | Busca por código o razón social |
| sp_listar_clientes | SELECT | Lista todos los clientes |
| sp_insertar_evento | INSERT | Agrega un nuevo evento |
| sp_actualizar_evento | UPDATE | Modifica datos de un evento |
| sp_eliminar_evento | DELETE | Elimina un evento por número |
| sp_buscar_evento | SELECT | Busca por número o título |
| sp_listar_eventos | SELECT | Lista todos los eventos |
| sp_insertar_personal | INSERT | Agrega un nuevo empleado |
| sp_actualizar_personal | UPDATE | Modifica datos de un empleado |
| sp_eliminar_personal | DELETE | Elimina un empleado por código |
| sp_buscar_personal | SELECT | Busca por código o nombre |
| sp_listar_personal | SELECT | Lista todo el personal |

### Ejemplo de llamada desde Python

```python
def call_sp_fetch(sp_name, params=()):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()
    cur.callproc(sp_name, params)
    rows = []
    for result in cur.stored_results():
        rows = result.fetchall()
    cur.close()
    conn.close()
    return rows

# Uso:
rows = call_sp_fetch('sp_buscar_recinto', ('RC-001',))
```

---

## 6. Requisitos e Instalación

### 6.1 Requisitos del sistema
- Python 3.11 o superior
- WAMP Server (MySQL 8.4)
- PyCharm (recomendado)
- HeidiSQL (administración de BD)

### 6.2 Pasos de instalación

**Paso 1 — Instalar dependencia Python** (en la terminal de PyCharm):
```bash
pip install mysql-connector-python
```

**Paso 2 — Ejecutar Stored Procedures en HeidiSQL:**
1. Abrir HeidiSQL y conectarse a `localhost`
2. Abrir el archivo `stored_procedures.sql`
3. Presionar **F9** para ejecutar

**Paso 3 — Ejecutar la aplicación:**
```bash
python eventpro.py
```

---

## 7. Funcionalidades del Sistema

### 7.1 Operaciones disponibles
- **Guardar** — Inserta un nuevo registro en la base de datos
- **Actualizar** — Modifica un registro existente identificado por su código
- **Eliminar** — Elimina un registro con confirmación previa
- **Limpiar** — Vacía todos los campos del formulario
- **Buscar** — Localiza registros por código o nombre y rellena el formulario

### 7.2 Validaciones implementadas
- Campos obligatorios verificados antes de guardar
- Confirmación antes de eliminar registros
- Manejo de errores de integridad (códigos duplicados)
- Placeholders informativos en todos los campos

---

## 8. Archivos del Proyecto

| Archivo | Descripción |
|---|---|
| `eventpro.py` | Aplicación principal con interfaz Tkinter y lógica CRUD |
| `stored_procedures.sql` | Script SQL con los 20 Stored Procedures |
| `README.md` | Documentación completa del proyecto |

---

*EventPro – Espacios Magníficos S.A. © 2026*
