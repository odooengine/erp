# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class emp_salary_slip(models.Model):
#     _name = 'emp_salary_slip.emp_salary_slip'
#     _description = 'emp_salary_slip.emp_salary_slip'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
