# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare

class EngAccPaymentRR(models.TransientModel):
    _inherit="account.payment.register"

    available_partner_bank_ids = fields.Many2many('res.bank',
                                                  )

class EngAccPayment(models.Model):
    _inherit="account.payment"

    available_partner_bank_ids = fields.Many2many('res.bank',
        compute='_compute_available_partner_bank_ids',
    )

    @api.depends('partner_id', 'company_id', 'payment_type')
    def _compute_available_partner_bank_ids(self):
        for pay in self:
            res_partner_bank_id = self.env['res.bank'].search([],limit=1)
            if pay.payment_type == 'inbound':

                pay.available_partner_bank_ids = res_partner_bank_id.ids#pay.journal_id.bank_account_id
            else:
                pay.available_partner_bank_ids = res_partner_bank_id.ids
#                 pay.partner_id.bank_ids\
#                         .filtered(lambda x: x.company_id.id in (False, pay.company_id.id))._origin

    @api.depends('available_partner_bank_ids', 'journal_id')
    def _compute_partner_bank_id(self):
        ''' The default partner_bank_id will be the first available on the partner. '''
        for pay in self:
            res_partner_bank_id = self.env['res.partner.bank'].search([('company_id', '=', self.company_id.id)],limit=1)
#             if pay.partner_bank_id not in pay.available_partner_bank_ids._origin:
            pay.partner_bank_id = res_partner_bank_id.id


    def get_move_lines(self):
        moves = self.env['account.move.line'].search(['|',('move_id.payment_id', '=', self.id),('move_id.ref', '=', self.name)])
        return moves[0], moves[2]





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


class AccPayRegInh(models.TransientModel):
    _inherit = 'account.payment.register'

    cheque_no = fields.Char(string="Cheque No")

    @api.onchange('cheque_no')
    def set_caps(self):
        val = str(self.cheque_no)
        self.cheque_no = val.upper()

    def _create_payments(self):
        res = super(AccPayRegInh, self)._create_payments()
        res.update({'cheque_no': self.cheque_no})
        return res

#     def _post_payments(self, to_process, edit_mode=False):
#         """ Post the newly created payments.
#         :param to_process:  A list of python dictionary, one for each payment to create, containing:
#                             * create_vals:  The values used for the 'create' method.
#                             * to_reconcile: The journal items to perform the reconciliation.
#                             * batch:        A python dict containing everything you want about the source journal items
#                                             to which a payment will be created (see '_get_batches').
#         :param edit_mode:   Is the wizard in edition mode.
#         """
#         payments = self.env['account.payment']
#         for vals in to_process:
#             payments |= vals['payment']
#         payments.action_post()
#         payments.button_review()
#         payments.button_approved()
# #
# #     def _reconcile_payments(self, to_process, edit_mode=False):
# #         """ Reconcile the payments.
# #
# #         :param to_process:  A list of python dictionary, one for each payment to create, containing:
# #                             * create_vals:  The values used for the 'create' method.
# #                             * to_reconcile: The journal items to perform the reconciliation.
# #                             * batch:        A python dict containing everything you want about the source journal items
# #                                             to which a payment will be created (see '_get_batches').
# #         :param edit_mode:   Is the wizard in edition mode.
# #         """
# #         domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False)]
# #         for vals in to_process:
# #             payment_lines = vals['payment'].line_ids.filtered_domain(domain)
# #             lines = vals['to_reconcile']
# #
# #             for account in payment_lines.account_id:
# #                 (payment_lines + lines)\
# #                     .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
# #                     .reconcile()