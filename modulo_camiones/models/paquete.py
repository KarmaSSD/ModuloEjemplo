from odoo import models, fields

class Paquete(models.Model):
    _name = "paqueteria_paquete"
    _description = "Paquete de transporte"

    tracking_code = fields.Char(string="Numero de seguimiento", required=True, index=True)

    remitente_id = fields.Many2one("res.partner", string="Remitente", required=True)

    destinatario_id = fields.Many2one("res.partner", string="Destinatario", required=True)

    country_id = fields.Many2one("res.country", string="Pais entrega")

    state_id = fields.Many2one("res.country.state", string="Region entrega")

    municipio = fields.Char(string="Municipio entrega")

    calle = fields.Char(string="Calle")

    numero = fields.Char(string="Numero")

    datos_adicionales = fields.Text(string="Datos adicionales")

    camion_id = fields.Many2one("paqueteria_camion", string="Camion actual")

    actualizaciones_ids = fields.One2many("paqueteria_seguimiento", "paquete_id", string="Actualizaciones de envio")
