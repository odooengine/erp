# -*- coding: utf-8 -*-
# from odoo import http


# class ReportProductPurchase(http.Controller):
#     @http.route('/report_product_purchase/report_product_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_product_purchase/report_product_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_product_purchase.listing', {
#             'root': '/report_product_purchase/report_product_purchase',
#             'objects': http.request.env['report_product_purchase.report_product_purchase'].search([]),
#         })

#     @http.route('/report_product_purchase/report_product_purchase/objects/<model("report_product_purchase.report_product_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_product_purchase.object', {
#             'object': obj
#         })
