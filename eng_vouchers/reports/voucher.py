# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


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