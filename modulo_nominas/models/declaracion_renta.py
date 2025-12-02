from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DeclaracionRenta(models.Model):
    _name = "nomina.declaracion"
    _description = "Declaracion anual de IRPF"
    _order = "anio desc"

    anio = fields.Integer(string="Año", required=True)
    empleado_id = fields.Many2one("hr.employee", string="Empleado", required=True)

    nomina_ids = fields.One2many("nomina.nomina", "declaracion_id", string="Nominas del año")

    sueldo_bruto_total = fields.Monetary(string="Sueldo bruto total", compute="_compute_totales", 
        store=True)

    impuestos_totales = fields.Monetary(string="Total IRPF pagado", compute="_compute_totales", 
        store=True)

    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    fecha_inicio = fields.Date(compute="_compute_fechas", store=True)
    fecha_fin = fields.Date(compute="_compute_fechas", store=True)

    @api.depends("nomina_ids.sueldo_bruto", "nomina_ids.irpf_pagado")
    def _compute_totales(self):
        for rec in self:
            rec.sueldo_bruto_total = sum(n.sueldo_bruto for n in rec.nomina_ids)
            rec.impuestos_totales = sum(n.irpf_pagado for n in rec.nomina_ids)

    @api.depends("anio")
    def _compute_fechas(self):
        for rec in self:
            if rec.anio:
                rec.fecha_inicio = date(rec.anio, 1, 1)
                rec.fecha_fin = date(rec.anio, 12, 31)
            else:
                rec.fecha_inicio = False
                rec.fecha_fin = False

    @api.constrains("nomina_ids", "empleado_id", "anio")
    def _check_limite_nominas(self):
        for rec in self:
            if len(rec.nomina_ids) > 14:
                raise ValidationError("Una declaracion anual no puede tener más de 14 nominas")

            years = {n.fecha.year for n in rec.nomina_ids}
            if len(years) > 1:
                raise ValidationError("Todas las nominas deben pertenecer al mismo año natural")

            if years and years != {rec.anio}:
                raise ValidationError("El año de la declaracion debe coincidir con las nominas seleccionadas")

            empleados = {n.empleado_id.id for n in rec.nomina_ids if n.empleado_id}
            if empleados and empleados != {rec.empleado_id.id}:
                raise ValidationError("Todas las nominas deben ser del mismo empleado que la declaracion")
