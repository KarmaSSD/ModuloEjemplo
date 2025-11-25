{
    "name": "modulo_camiones",
    "version": "1.0",
    "summary": "Gestion de paquetes y camiones",
    "category": "Operations",
    "depends": ["base", "hr"],
    "data": [
        "security/category.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/paquete_views.xml",
        "views/seguimiento_views.xml",
        "views/camion_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
