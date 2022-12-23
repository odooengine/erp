from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PDCPaymentWizard(models.TransientModel):
    _name = 'pdc.payment.wizard'
    _description = 'PDC Payment'

    partner_id = fields.Many2one('res.partner', string='Partner',)
    payment_amount = fields.Float(string='Payment Amount')
    cheque_ref = fields.Char(string='Commercial Name')
    memo = fields.Char(string='Memo')
    destination_account_id = fields.Many2one('account.account', string='Bank')
    journal_id = fields.Many2one('account.journal', string='Journal')
    currency_id = fields.Many2one('res.currency', string='Currency')
    pdc_type = fields.Selection([('sent', 'Sent'),
                                 ('received', 'Received'),
                                 ], string='PDC Type',)

    date_payment = fields.Date(string='Payment Date')
    cheque_no = fields.Char()
    move_id = fields.Many2one('account.move', string='Invoice/Bill Ref')

    @api.onchange('journal_id')
    def _onchange_journal(self):
        for rec in self:
            if rec.journal_id:
                rec.destination_account_id = rec.journal_id.default_account_id.id

    def create_pdc_payments(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        for record in self:
            if rec.move_type == 'out_invoice':
                vals = {
                    'partner_id': record.partner_id.id,
                    'journal_id': record.journal_id.id,
                    'move_id': rec.id,
                    'date_payment': record.date_payment,
                    'destination_account_id': record.destination_account_id.id,
                    'currency_id': record.currency_id.id,
                    'payment_amount': record.payment_amount,
                    'cheque_no': record.cheque_no,
                    'pdc_type': 'received'
                }
                record = self.env['pdc.payment'].create(vals)
            elif rec.move_type == 'in_invoice':
                vals = {
                    'partner_id': record.partner_id.id,
                    'journal_id': record.journal_id.id,
                    'move_id': rec.id,
                    'date_payment': record.date_payment,
                    'destination_account_id': record.destination_account_id.id,
                    'currency_id': record.currency_id.id,
                    'payment_amount': record.payment_amount,
                    'cheque_no': record.cheque_no,
                    'pdc_type': 'sent'
                }
                record = self.env['pdc.payment'].create(vals)

        rec.is_pdc_created = True