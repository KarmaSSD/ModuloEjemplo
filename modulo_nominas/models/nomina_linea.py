from odoo import models, fields

class NominaLinea(models.Model):
    _name = "nomina.linea"
    _description = "linea de bonificacion o deduccion"

    nomina_id = fields.Many2one("nomina.nomina", string="Nomina", required=True, ondelete="cascade",)

    tipo = fields.Selection(
        [
            ("bonus", "Bonificación"),
            ("deduccion", "Deducción"),
        ],
        string="Tipo", required=True,)

    concepto = fields.Char(string="Concepto", required=True)
    importe = fields.Monetary(string="Importe", required=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id,)
