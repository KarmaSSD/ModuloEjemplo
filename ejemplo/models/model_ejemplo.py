from odoo import models, fields

class Ejemplo(models.Model):
    _name = "ejemplo.ejemplo"
    _description = "Modelo de Ejemplo"

    name = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    activo = fields.Boolean(string="Activo", default=True)
