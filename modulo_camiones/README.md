# modulo_camiones

Registro y gestión de camiones, sus conductores, los paquetes transportados y el seguimiento de los envíos.

---

## Caracteristicas principales

- Registrar paquetes con un remitente, un destinatario y  una dirección de entrega.

- Gestionar camiones con conductor asignado y su historial.

- Registrar actualizaciones de estado para cada paquete (seguimiento del envío).

- Vincular paquetes a camiones para facilitar la gestión logística.

- Vistas completas de lista y formulario para cada modelo.

---

## Estructura del módulo

```pgsql
modulo_camiones/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── paquete.py
│   ├── seguimiento.py
│   └── camion.py
├── security/
│   ├── category.xml
│   ├── security.xml
│   └── ir.model.access.csv
└── views/
    ├── paquete_views.xml
    ├── seguimiento_views.xml
    ├── camion_views.xml
    └── menus.xml
```
---

## Modelos

### 1. Modelo de paquetes (`paqueteria_paquete`)

Permite registrar envíos y toda la información relacionada a ellos.

**Campos:**

- `tracking_code`: Número de seguimiento del paquete.
- `remitente_id`: El emisor del paquete.  
- `destinatario_id`: El receptor del paquete. 
- `country_id`, `state_id`, `municipio`, `calle`, `numero` : Dirección de entrega. 
- `camion_id`: El camion en el que se transporta el paquete.
- `actualizaciones_id`: El seguimiento del paquete. 

### 2. Modelo de seguimiento (`paqueteria_seguimiento`)

Registra el estado del paquete durante su envio.

**Campos principales:**

- `paquete_id`: Paquete al que se realiza el seguimiento.
- `fecha`: Fecha y hora de cada actualizacion. 
- `estado`: El estado del envio (creado, en transito, en reparto, entregado o incidiencia).
- `notas`: Informacion extra.

### 3. Modelo de camiones (`paqueteria_camion`)

Los camiones usados durante los envios.

**Campo principal:**

- `matricula`: La matrícula del camión.
- `driver_id`: El conductor del camión.
- `driver_history_ids`: Los conductores anteriores del camión.
- `fecha_ultima_itv`: Fecha de la ultima revisión del camión.
- `notas_mantenimiento`: Información sobre reparaciones u otros datos del camión.
- `paquete_ids`: Los paquetes transportados por el camión.

---

## Vistas incluidas

### Paquetes

- Vista de lista con la información de los envios.

- Formulario con:
    - Datos del remitente y el destinatario.
    - Dirección de envio.
    - Camión asignado.
    - Lista con las actualizaciones del seguimiento.

### Seguimiento

- Vista de lista con los estados de los envios y sus fechas.

- Formulario para edición o consulta de otros datos.

### Camiones

- Vista de lista con la información de los camiones.

- Formulario con:
    - Datos generales del camion (matricula, ITV, etc...).
    - Conductor actual y el historial de los conductores pasados.
    - Historial de mantenimiento / reparaciones.
    - Paquetes transportados.

---

## Seguridad y permisos

El módulo define:

**- Categoría de seguridad propia:** Gestión PC

**- Dos grupos de usuario:**

    - Usuario del módulo

    - Administrador del módulo

**- Los permisos de acceso para cada modelo dependiendo del rol.**

Los grupos de usuarios se encuentran en security/security.xml y los permisos ensecurity/ir.model.access.csv.

---

## Cómo usar el módulo

1. Accede al menú Gestión de camiones.

2. Registra primero los los camiones y los empleados en caso de que no existen que haran de conductores.

3. Crea un nuevo paquete / paquetes desde la pestaña Paquetes.

4. Asignale un camion al paquete y actualiza la informacion de seguimiento.

5. Una vez registrado todo puedes consultar que todo esta conectado entre si.

