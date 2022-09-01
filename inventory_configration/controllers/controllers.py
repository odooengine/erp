# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryConfigration(http.Controller):
#     @http.route('/inventory_configration/inventory_configration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_configration/inventory_configration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_configration.listing', {
#             'root': '/inventory_configration/inventory_configration',
#             'objects': http.request.env['inventory_configration.inventory_configration'].search([]),
#         })

#     @http.route('/inventory_configration/inventory_configration/objects/<model("inventory_configration.inventory_configration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_configration.object', {
#             'object': obj
#         })
