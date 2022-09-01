from odoo import api, fields, models, _


class EmployeeLines(models.Model):
    _name = "employee.lines"
    _description = "Employee Lines"
    _order = "wage desc"
    # _rec_name = 'employee_id'

    employee_id = fields.Char(string='Employee')
    wage = fields.Float(string='Salary' )
    amount = fields.Float(string='Current Advance')

    current_advance_id = fields.Many2one('advance.current')

    # def get_lines(self):
    #     self.wage