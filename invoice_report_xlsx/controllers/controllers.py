# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceReportXlsx(http.Controller):
#     @http.route('/invoice_report_xlsx/invoice_report_xlsx/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_report_xlsx/invoice_report_xlsx/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_report_xlsx.listing', {
#             'root': '/invoice_report_xlsx/invoice_report_xlsx',
#             'objects': http.request.env['invoice_report_xlsx.invoice_report_xlsx'].search([]),
#         })

#     @http.route('/invoice_report_xlsx/invoice_report_xlsx/objects/<model("invoice_report_xlsx.invoice_report_xlsx"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_report_xlsx.object', {
#             'object': obj
#         })
