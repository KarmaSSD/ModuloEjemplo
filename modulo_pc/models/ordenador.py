from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class PcOrdenador(models.Model):
    _name = 'pc.ordenador'
    _description = 'ordenador de empresa'

    numero_equipo = fields.Char(string='numero de equipo', required=True)
    user_id = fields.Many2one('res.users', string='usuario')
    components_ids = fields.Many2many('pc.componente', string='componentes')

    ultima_mod = fields.Date(string='ultima modificacion')

    precio_total = fields.Monetary(
        string='precio total',
        compute='_compute_total',
        store=True,
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='moneda',
        default=lambda self: self.env.company.currency_id.id,
    )

    incidencias = fields.Text(string='incidencias')

    os_tag_ids = fields.Many2many(
        'res.partner.category',
        string='sistemas operativos',
        help='tags que indican los sistemas operativos instalados',
    )

    @api.constrains('ultima_mod')
    def _check_fecha_no_futura(self):
        for record in self:
            if record.ultima_mod and record.ultima_mod > date.today():
                raise ValidationError('la fecha no puede ser futura')

    @api.depends('components_ids.precio')
    def _compute_total(self):
        for record in self:
            total = sum(record.components_ids.mapped('precio'))
            record.precio_total = total
