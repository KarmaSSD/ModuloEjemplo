{
    'name': 'Ejemplo',
    'version': '1.0',
    'summary': 'Gestión de Ejemplos',
    'category': 'Gestión/Ejemplos',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/ejemplo_view.xml',
        'views/ejemplo_action.xml',
        'views/ejemplo_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
