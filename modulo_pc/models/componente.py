from odoo import models, fields

class Componente(models.Model):
    _name = "pc.componente"
    _description = "Componente de PC"

    name = fields.Char(string="Nombre tecnico", required=True)
    especificaciones = fields.Text(string="Especificaciones")
    precio = fields.Monetary(string="Precio")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
