from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class Ordenador(models.Model):
    _name = "pc.ordenador"
    _description = "Ordenador de la empresa"

    numero_equipo = fields.Char(string="Numero de equipo", required=True)
    user_id = fields.Many2one("res.users", string="Usuario")
    components_ids = fields.Many2many("pc.componente", string="Componentes")
    ultima_mod = fields.Date(string="Ultima modificacion")
    incidencias = fields.Text(string="Incidencias")

    precio_total = fields.Monetary(string="Precio total", compute="_compute_total", store=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    sistemas_ids = fields.Many2many("pc.sistema.operativo", string="Sistemas Operativos",)



    @api.constrains("ultima_mod")
    def _check_fecha(self):
        for record in self:
            if record.ultima_mod and record.ultima_mod > date.today():
                raise ValidationError("La fecha no puede ser futura")

    @api.depends("components_ids.precio")
    def _compute_total(self):
        for record in self:
            record.precio_total = sum(record.components_ids.mapped("precio"))
