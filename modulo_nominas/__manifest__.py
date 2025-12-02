{
    "name": "modulo_nominas",
    "version": "1.0",
    "summary": "gestion de nominas de empleados",
    "category": "Human Resources",
    "depends": ["base", "hr"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/nomina_views.xml",
        "views/nomina_linea_views.xml",
        "views/declaracion_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
