from odoo import fields, models, _, api
from odoo.exceptions import UserError


class HRShift(models.Model):
    _name = 'hr.shift'

    name = fields.Char('Name')
    check_in = fields.Float('Check In')
    check_out = fields.Float('Check Out')


class InheritEmployee(models.Model):
    _inherit = "hr.employee"

    shift_id = fields.Many2one('hr.shift', string='Shifts')
