from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Nomina(models.Model):
    _name = "nomina.nomina"
    _description = "nomina de empleado"
    _order = "fecha desc"

    empleado_id = fields.Many2one("hr.employee", string="Empleado", required=True)

    sueldo_base = fields.Monetary(string="Sueldo base", required=True)

    currency_id = fields.Many2one("res.currency", string="Moneda", required=True, 
        default=lambda self: self.env.company.currency_id,)

    linea_ids = fields.One2many("nomina.linea", "nomina_id", string="Bonificaciones y deducciones",)

    irpf = fields.Float(string="IRPF porcentaje", required=True, default=15.0,
        help="porcentaje de irpf entre 0 y 100",)

    irpf_pagado = fields.Monetary(string="IRPF pagado", compute="_compute_totales", store=True,)

    fecha = fields.Date(string="Fecha", required=True, default=fields.Date.context_today,)

    anio_nomina = fields.Integer(string="Año", compute="_compute_anio", store=True)

    pdf_justificante = fields.Binary(string="Justificante transferencia")
    pdf_justificante_filename = fields.Char(string="Nombre fichero")

    estado = fields.Selection(
        [
            ("borrador", "redactada"),
            ("confirmada", "confirmada"),
            ("pagada", "pagada"),
        ],
        string="Estado", default="borrador", required=True,)

    total_bonificaciones = fields.Monetary(string="Total bonificaciones", compute="_compute_totales",
        store=True,)

    total_deducciones = fields.Monetary(string="Total deducciones", compute="_compute_totales", 
        store=True,)

    sueldo_bruto = fields.Monetary(string="Sueldo bruto", compute="_compute_totales", store=True,)

    sueldo_neto = fields.Monetary(string="Sueldo neto", compute="_compute_totales", store=True,)

    declaracion_id = fields.Many2one("nomina.declaracion", string="Declaración anual",
        help="Si pertenece a una declaracion de IRPF.", 
        domain="[('empleado_id', '=', empleado_id), ('anio', '=', anio_nomina)]",)

    @api.depends("sueldo_base", "linea_ids.tipo", "linea_ids.importe", "irpf",)
    def _compute_totales(self):
        for rec in self:
            total_bonus = sum(l.importe for l in rec.linea_ids if l.tipo == "bonus")
            total_dedu = sum(l.importe for l in rec.linea_ids if l.tipo == "deduccion")

            rec.total_bonificaciones = total_bonus
            rec.total_deducciones = total_dedu

            bruto = rec.sueldo_base + total_bonus
            rec.sueldo_bruto = bruto

            rec.irpf_pagado = bruto * rec.irpf / 100.0 if rec.irpf > 0 else 0.0

            rec.sueldo_neto = bruto - total_dedu - rec.irpf_pagado

    @api.constrains("irpf")
    def _check_irpf(self):
        for rec in self:
            if rec.irpf < 0 or rec.irpf > 100:
                raise ValidationError("el porcentaje de irpf debe estar entre 0 y 100")

    @api.constrains("fecha")
    def _check_fecha(self):
        today = fields.Date.today()
        for rec in self:
            if rec.fecha and rec.fecha > today:
                raise ValidationError("la fecha de la nomina no puede ser futura")

    def _ensure_declaracion_capacity(self, declaracion, record=None):
        if not declaracion:
            return
        domain = [("declaracion_id", "=", declaracion.id)]
        if record and record.id:
            domain.append(("id", "!=", record.id))
        count = self.env["nomina.nomina"].search_count(domain)
        if count >= 14:
            raise ValidationError("La declaracion ya tiene 14 nominas asignadas")

    @api.constrains("declaracion_id", "empleado_id", "anio_nomina")
    def _check_declaracion(self):
        for rec in self:
            if not rec.declaracion_id:
                continue
            if rec.declaracion_id.empleado_id != rec.empleado_id:
                raise ValidationError("La nomina solo puede asociarse a la declaracion del mismo empleado")
            if rec.anio_nomina and rec.declaracion_id.anio != rec.anio_nomina:
                raise ValidationError("La nomina solo puede asociarse a una declaracion del mismo año")
            rec._ensure_declaracion_capacity(rec.declaracion_id, record=rec)

    @api.depends("fecha")
    def _compute_anio(self):
        for rec in self:
            rec.anio_nomina = rec.fecha.year if rec.fecha else False

    def _get_declaracion_for_values(self, empleado_id, fecha):
        Declaracion = self.env["nomina.declaracion"]
        if not empleado_id or not fecha:
            return Declaracion.browse()
        if isinstance(fecha, str):
            fecha = fields.Date.to_date(fecha)
        return Declaracion.search(
            [
                ("empleado_id", "=", empleado_id),
                ("anio", "=", fecha.year),
            ],
            limit=1,
        )

    def _auto_assign_declaracion(self):
        for rec in self:
            declaracion = rec._get_declaracion_for_values(rec.empleado_id.id, rec.fecha)
            new_id = declaracion.id if declaracion else False
            if rec.declaracion_id.id != new_id:
                if declaracion:
                    rec._ensure_declaracion_capacity(declaracion, record=rec)
                rec.with_context(skip_auto_declaracion=True).write({"declaracion_id": new_id})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("declaracion_id"):
                declaracion = self._get_declaracion_for_values(
                    vals.get("empleado_id"), vals.get("fecha")
                )
                if declaracion:
                    self._ensure_declaracion_capacity(declaracion)
                    vals["declaracion_id"] = declaracion.id
            else:
                declaracion = self.env["nomina.declaracion"].browse(vals["declaracion_id"])
                self._ensure_declaracion_capacity(declaracion)
        records = super().create(vals_list)
        missing = records.filtered(lambda r: not r.declaracion_id)
        if missing:
            missing._auto_assign_declaracion()
        return records

    def write(self, vals):
        if not self.env.context.get("skip_auto_declaracion") and "declaracion_id" in vals:
            declaracion = self.env["nomina.declaracion"].browse(vals["declaracion_id"])
            for rec in self:
                if declaracion and declaracion != rec.declaracion_id:
                    rec._ensure_declaracion_capacity(declaracion, record=rec)
        res = super().write(vals)
        if not self.env.context.get("skip_auto_declaracion") and (
            "empleado_id" in vals or "fecha" in vals
        ):
            self._auto_assign_declaracion()
        return res

    @api.onchange("empleado_id", "fecha")
    def _onchange_assign_declaracion(self):
        for rec in self:
            declaracion = rec._get_declaracion_for_values(rec.empleado_id.id, rec.fecha)
            rec.declaracion_id = declaracion

    def action_set_borrador(self):
        for rec in self:
            rec.estado = "borrador"

    def action_confirmar(self):
        for rec in self:
            if rec.estado == "pagada":
                continue
            rec.estado = "confirmada"

    def action_marcar_pagada(self):
        for rec in self:
            if rec.estado == "borrador":
                raise ValidationError("Debe confirmar la nomina antes de marcarla como pagada")
            rec.estado = "pagada"
