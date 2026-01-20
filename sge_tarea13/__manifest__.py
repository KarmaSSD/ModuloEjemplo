{
    'name': 'Tarea 13',
    'version': '1.0',
    'summary': 'Extiendo hr employee para añadir DNI y el numero de la seguridad social',
    'description': """
        Tarea 13:
        - Extend hr.employee to include 'nss' and 'dni'.
        - Validate NSS (12 chars, format).
        - Validate DNI (8 digits + letter, Modulo 23).
    """,
    'author': 'User',
    'category': 'Human Resources',
    'depends': ['hr'],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
