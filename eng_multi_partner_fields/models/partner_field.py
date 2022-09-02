# -*- coding: utf-8 -*-


from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError, MissingError, AccessDenied


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection([('frenchise', 'Frenchise'),
                                     ('owned', 'Owned'),
                                     ], string='Customer Type')
