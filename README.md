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
│   └── ordenador.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── views/
    ├── componente_views.xml
    ├── ordenador_views.xml
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

---

## Lógica interna del módulo

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

---

## Vistas del modulo:

El modulo contiene vistas completas tanto para ordenadores como para componentes:

### Vistas de componentes

- Lista de componentes

- Formulario completo

### Vistas de ordenadores

- Lista con informacion clave

- Formulario completo con secciones

- Campo tags visible

---

## Seguridad y accesos

**El módulo define:**

- Grupos / tipos de usuarios en security.xml

- Permisos en ir.model.access.csv

---

## Cómo usarlo

1. Entrar al menú Equipos Informáticos.

2. Debes registrar los componentes antes de añadirlos a los PCs.

3. Crear un PC desde el menú Ordenadores.

4. Asignar un usuario, los componentes e incidencias si estas existen al nuevo PC.

5. Guardar los cambios para actualizar el precio total.

6. Posteriormente podemos acceder a los PCs ya creados para modificarlos.
