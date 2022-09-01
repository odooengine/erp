from odoo import api, models, fields


class InheritedHrEmployee(models.Model):
    _inherit = 'hr.employee'

    blood_group_id = fields.Many2one('hr.blood.group', 'Blood Group')
