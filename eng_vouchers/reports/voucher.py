# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class EngAccPayment(models.Model):
    _inherit="account.payment"
     
     
    available_partner_bank_ids = fields.Many2many(
        comodel_name='res.partner.bank',
        compute='_compute_available_partner_bank_ids',
    )
     
    
    @api.depends('partner_id', 'company_id', 'payment_type')
    def _compute_available_partner_bank_ids(self):
        for pay in self:
            if pay.payment_type == 'inbound':
                pay.available_partner_bank_ids = pay.journal_id.bank_account_id.id
            else:
                pay.available_partner_bank_ids = pay.partner_id.bank_ids.filtered(lambda x: x.company_id.id in (False, pay.company_id.id)).id
#                         .filtered(lambda x: x.company_id.id in (False, pay.company_id.id))._origin
#                         .filtered(lambda x: x.company_id.id in (False, pay.company_id.id)).id
  
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