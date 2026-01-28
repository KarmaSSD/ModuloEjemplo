{
    'name': 'Tarea 14 Guarderia',
    'version': '1.0',
    'summary': 'Servicio de guarderia heredando de empleado y evento',
    'description': """
        Tarea 14:
        - Delegacion de herencia de hr.employee y calendar.event.
        - Campos extra: descripcion y rango de edad.
    """,
    'author': 'User',
    'category': 'Services',
    'depends': ['base', 'hr', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/guarderia_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
