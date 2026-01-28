from odoo import models, fields

class ServicioGuarderia(models.Model):
    _name = 'sge.servicio.guarderia'
    _description = 'Servicio de Guarderia'
    _inherits = {
        'hr.employee': 'empleado_id',
        'calendar.event': 'evento_id',
    }

    empleado_id = fields.Many2one('hr.employee', required=True, ondelete='cascade', auto_join=True, index=True)
    evento_id = fields.Many2one('calendar.event', required=True, ondelete='cascade', auto_join=True, index=True)

    descripcion = fields.Text(string='Descripcion')
    rango_edad = fields.Selection([
        ('0-2', '0-2 años'),
        ('3-5', '3-5 años'),
        ('6-8', '6-8 años'),
        ('9-11', '9-11 años')
    ], string='Rango de edad')
