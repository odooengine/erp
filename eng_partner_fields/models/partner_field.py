# -*- coding: utf-8 -*-


from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError, MissingError, AccessDenied


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('customer', 'Customer'),
                              ('vendor', 'Vendor'),
                              ('frenchise', 'Frenchise'),
                              ('owned', 'Owned'),
                              ], string='Partner Type')

    @api.onchange('partner_type')
    def onchange_partner_type(self):
        if self.partner_type == 'customer':
            self.customer_rank = 1
            self.supplier_rank = 0
        elif self.partner_type == 'vendor':
            self.supplier_rank = 1
            self.customer_rank = 0
        else:
            self.supplier_rank = 1
            self.customer_rank = 1



