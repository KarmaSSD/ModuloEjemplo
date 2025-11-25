from odoo import models, fields

class Seguimiento(models.Model):
    _name = "paqueteria_seguimiento"
    _description = "Seguimiento de envio"

    paquete_id = fields.Many2one("paqueteria_paquete", string="Paquete", required=True, ondelete="cascade")

    fecha = fields.Datetime(string="Fecha entrada", default=fields.Datetime.now, required=True)

    estado = fields.Selection([
            ("creado", "Creado"),
            ("en_transito", "En transito"),
            ("en_reparto", "En reparto"),
            ("entregado", "Entregado"),
            ("incidencia", "Incidencia")
        ],
        string="Estado", required=True, default="creado")
        
    notas = fields.Text(string="Notas adicionales")
