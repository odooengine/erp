# -*- coding: utf-8 -*-
# from odoo import http


# class EmpSalarySlip(http.Controller):
#     @http.route('/emp_salary_slip/emp_salary_slip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_salary_slip/emp_salary_slip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_salary_slip.listing', {
#             'root': '/emp_salary_slip/emp_salary_slip',
#             'objects': http.request.env['emp_salary_slip.emp_salary_slip'].search([]),
#         })

#     @http.route('/emp_salary_slip/emp_salary_slip/objects/<model("emp_salary_slip.emp_salary_slip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_salary_slip.object', {
#             'object': obj
#         })
