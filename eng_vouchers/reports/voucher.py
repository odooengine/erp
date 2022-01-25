# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


# class EngAccPayment(models.Model):
#     _inherit="account.payment"
<<<<<<< HEAD
#     
#     
#     available_partner_bank_ids = fields.Many2many(
#         comodel_name='res.partner.bank',
# #         compute='_compute_available_partner_bank_ids',
#     )
#     
=======
    
    
#     available_partner_bank_ids = fields.Many2many(
#         comodel_name='res.partner.bank',
#         compute='_compute_available_partner_bank_ids',
#     )
    
>>>>>>> cbcd2c034b19923eec7ed1138cfee7d7b6cf73c9
    
class AccountEdi(models.Model):
    _inherit = 'account.edi.document'

    def action_export_xml(self):
        pass    
    


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'
    
    
  

    
    
    
    journal_type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'Miscellaneous'),
    ], related='journal_id.type', string='Journal Type')

    def dict_values(self):
        res = dict(self.env['account.journal']._fields['type'].selection).get(self.journal_type)
        return res
