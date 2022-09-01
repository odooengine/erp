# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class invoice_report_xlsx(models.Model):
#     _name = 'invoice_report_xlsx.invoice_report_xlsx'
#     _description = 'invoice_report_xlsx.invoice_report_xlsx'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
