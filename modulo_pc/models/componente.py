from odoo import models, fields

class PcComponente(models.Model):
    _name = 'pc.componente'
    _description = 'componente de pc'

    name = fields.Char(string='nombre tecnico', required=True)
    especificaciones = fields.Text(string='especificaciones')
    precio = fields.Monetary(string='precio')
    currency_id = fields.Many2one(
        'res.currency',
        string='moneda',
        default=lambda self: self.env.company.currency_id.id,
    )
