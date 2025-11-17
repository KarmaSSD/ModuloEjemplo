# modulo_pc

Registro y gestión de ordenadores, sus componentes y el mantenimiento de estos.

---
## Caracteristicas principales

- Registrar componentes con descripcion y precio unitario.

- Gestionar ordenadores con usuarios asignados.

- Calculo automatico del precio total de los ordenadores.

- Restriccion que impide introducir fechas futuras en las incidencias.

- Tags descriptivos para indicar diferencias o filtrar entre los diferentes ordenadores.

- Vistas completas de lista y formulario.

---

## Estructura del módulo

```pgsql
modulo_pc/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── componente.py
│   ├── ordenador.py
│   └── sistema_operativo.py
├── security/
│   ├── category.xml
│   ├── security.xml
│   └── ir.model.access.csv
└── views/
    ├── componente_views.xml
    ├── ordenador_views.xml
    ├── sistema_operativo_views.xml
    └── menus.xml
```
---

## Modelos

### 1. Modelo de componentes (`pc.componente`)

Permite registrar las piezas que componen cada uno de los PCs / ordendadores.

**Campos:**

- `nombre_tecnico`: Nombre del componente
- `especificaciones`: Detalles tecnicos del componente  
- `precio`: Precio unitario del componente  

Cada componente puede estar en muchos ordenadores (Many2many).

---

### 2. Modelo de ordenadores (`pc.ordenador`)

Registra un ordenador y la informacion de este.

**Campos principales:**

- `numero_equipo`: ID del equipo
- `user_id`: Usuario asignado al PC (Many2one)  
- `components_ids`: Componentes que estan instalados (Many2many)  
- `ultima_mod`: Ultima modificación del PC  
- `precio_total`: Precio total que se autocalcula basado en los componentes
- `incidencias`: Incidencias registradas 
- `tags`: Etiquetas descriptivas

## Lógica interna del modelo:

### Restricción de fecha

Comprueba que la ultima modificacion se haya realizado en un punto anterior al actual:

```python
@api.constrains("ultima_mod")
def _check_fecha(self):
    for record in self:
        if record.ultima_mod and record.ultima_mod > fields.Date.today():
            raise ValidationError("La fecha no puede ser futura")
```
### Cálculo automático del precio total

El precio del PC se obtiene sumando el precio unitario de sus componentes:

```python
@api.depends("components_ids.precio")
def _compute_total(self):
    for record in self:
        record.precio_total = sum(c.precio for c in record.components_ids)
```

### 3. Modelo de sistemas operativos (`pc.sistema.operativo`)

Registra diferentes sistemas operativos.

**Campo principal:**

- `name`: Nombre del sistema operativo.

---

## Vistas incluidas

### Componentes

- Vista de lista con nombre, especificaciones y precio final unitario.

- Formulario para edicion y creacion.

### Ordenadores

- Vista de lista con número de equipo, usuario, precio total y numero de sistemas operativos.

- Formulario para edicion y creacion con secciones.

### Sistemas Operativos

- Vista simple de lista y formulario.

Todas estas vistas se integran en un menú principal llamado Gestión de ordenadores.

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

1. Accede al menú Gestión de ordenadores.

2. Registra primero los componentes y sistemas operativos que desees.

3. Crea un nuevo ordenador desde el menú Ordenadores.

4. Asigna un usuario, añade los componentes y asignale un sistema operatiov.

5. Guarda para que se calcule el precio total.

**Puedes usar los tags para filtrar equipos según características.**
