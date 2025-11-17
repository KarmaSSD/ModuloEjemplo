{
    'name': 'modulo_pc',
    'version': '1.0',
    'summary': 'gestion de ordenadores y componentes',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
    'security/category.xml',
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/componente_views.xml',
    'views/ordenador_views.xml',
    'views/sistema_operativo_views.xml',
    'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
