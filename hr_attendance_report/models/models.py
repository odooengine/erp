from odoo import models, fields, api


class PublicHolidays(models.Model):
    _name = 'public.holidays'

    name = fields.Char()
    date_from = fields.Date()
    date_to = fields.Date()


class UserdataInh(models.Model):
    _inherit = 'user.attendance'

    address_id = fields.Many2one('res.partner')
    department_id = fields.Many2one('hr.department')


class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'

    late_in = fields.Integer()
    late_out = fields.Integer()
    st = fields.Integer()
    ot = fields.Integer()
    my_activity_date_deadline = fields.Date()

#     bonus = fields.Float('Bonus', compute="_compute_bonus")
#
#     def _compute_bonus(self):
#         for record in self:
#             rec = self.env['hr.contract'].search([('employee_id', '=', record.employee_id.id)])
#             for r in rec:
#                 record.bonus = r.bonus
