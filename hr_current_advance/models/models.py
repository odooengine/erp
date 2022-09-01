from odoo import api, fields, models, _
from datetime import timedelta, datetime


class AdvanceCurrent(models.Model):
    _name = "advance.current"
    _description = "Advance Current"
    _rec_name = 'description'

    date_from = fields.Date(string='Date To')
    date_to = fields.Date(string='Date From')
    description = fields.Text(string='Description')
    word_address_id = fields.Many2one('res.partner', string='Work Address')

    employee_lines_id = fields.One2many('employee.lines', 'current_advance_id')



    def get_data_employee(self):
        print("u click")
        for res in self:
            emp = self.env['hr.employee'].search([('address_id', '=', res.word_address_id.id)])
            print(emp)
            for i in res.employee_lines_id:
                i.unlink()
            for record in emp:
                conntr = self.env['hr.contract'].search([('employee_id', '=', record.id)])

                self.write({
                    'employee_lines_id': [(0, 0, {
                        'employee_id': record.name,
                        'wage': conntr.wage,
                    })]

                })

    # wage = fields.Float('Wage' , related="employee_id.wage")
    # amount = fields.Float('Amount')

    # def _compute_wage(self):
    #     for record in self:
    #         rec = self.env['hr.contract'].search([('employee_id', '=', record.employee_id.id)])
    #         for r in rec:
    #             record.wage = r.wage
