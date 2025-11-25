from odoo import models, fields

class Camion(models.Model):
    _name = "paqueteria_camion"
    _description = "Camion de la flota"

    matricula = fields.Char(string="Numero de matricula", required=True)

    driver_id = fields.Many2one("hr.employee", string="Conductor actual")

    driver_history_ids = fields.Many2many("hr.employee", "paqueteria_camion_driver_rel", "camion_id",
        "employee_id", string="Antiguos conductores")

    fecha_ultima_itv = fields.Date(string="Fecha ultima ITV")
    notas_mantenimiento = fields.Text(string="Notas de mantenimiento")

    paquete_ids = fields.One2many("paqueteria_paquete", "camion_id", string="Paquetes transportados")
