from odoo import models, fields

class SistemaOperativo(models.Model):
    _name = "pc.sistema.operativo"
    _description = "Sistema Operativo"

    name = fields.Char(string="Nombre", required=True)
