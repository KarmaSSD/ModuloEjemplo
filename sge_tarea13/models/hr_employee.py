from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    nss = fields.Char(string='Numero de Seguridad Social', help="12 caracteres")
    dni = fields.Char(string='DNI', help="8 digitos + letra")

    @api.constrains('nss')
    def _check_nss(self):
        for record in self:
            if record.nss:
                if len(record.nss) != 12:
                    raise ValidationError(_("El Numero de Seguridad Social debe tener 12 caracteres."))
                if not record.nss.isdigit():
                     raise ValidationError(_("El Numero de Seguridad Social debe contener solo numeros."))

    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            if record.dni:
                dni_str = record.dni.upper().strip()
                if len(dni_str) != 9:
                    raise ValidationError(_("El DNI debe tener 9 caracteres 8 digitos y una letra."))
                
                numbers = dni_str[:-1]
                letter = dni_str[-1]
                
                if not numbers.isdigit() or not letter.isalpha():
                     raise ValidationError(_("El formato del DNI es 8 digitos y una letra."))

                valid_letters = "TRWAGMYFPDXBNJZSQVHLCKE"
                try:
                    calculated_letter = valid_letters[int(numbers) % 23]
                except ValueError:
                    raise ValidationError(_("Error en el calculo de la letra del DNI."))

                if letter != calculated_letter:
                    raise ValidationError(_(f"La letra del DNI es incorrecta. Deberia ser {calculated_letter}."))
