# -*- coding: utf-8 -*-
from datetime import datetime
from pytz import timezone

from odoo import models, fields, api


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    received_from = fields.Char('Received From')
    journals_ids = fields.Many2many('account.journal', compute='compute_journals')
    # available_partner_bank_ids = fields.Many2many('res.bank')

    @api.depends('journal_id')
    def compute_journals(self):
        journals = self.env['account.journal'].search([])
        journal_list = []
        for rec in journals:
            if rec.branch_id.id == self.env.user.branch_id.id:
                journal_list.append(rec.id)
        self.journals_ids = journal_list

    def get_print_date(self):
        now_utc_date = datetime.now()
        now_dubai = now_utc_date.astimezone(timezone('Asia/Karachi'))
        return now_dubai.strftime('%d/%m/%Y %H:%M:%S')


class AccountMoveLineInh(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one('res.branch', related='account_id.branch_id')
    return_qty = fields.Float('Return Qty')

    def compute_branch(self):
        for rec in self:
            rec.branch_id = rec.account_id.branch_id.id


class AccountAccountInh(models.Model):
    _inherit = 'account.account'

    branch_id = fields.Many2one('res.branch')
    is_new = fields.Boolean()
    is_old = fields.Boolean()


class AccountJournalInh(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one('res.branch')
    total_bal = fields.Float(compute='compute_bal')

    def compute_bal(self):
        for rec in self:
            lines = self.env['account.move.line'].search(
                [('account_id', '=', rec.default_account_id.id), ('move_id.state', '=', 'posted')]).mapped('balance')
            rec.total_bal = sum(lines)

    @api.onchange('default_account_id')
    def onchange_default_account_id(self):
        self.branch_id = self.default_account_id.branch_id.id


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    customer_balance = fields.Float('Balance', compute='compute_customer_balance')
    address_id = fields.Many2one('res.partner')

    def compute_customer_balance(self):
        for rec in self:
            invoices = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
            rec.customer_balance = invoices.total_due
            for k in self.invoice_line_ids:
                saleorder = self.env['sale.order'].search([("name", '=', self.invoice_origin)])
                for l in saleorder.picking_ids:
                    if l.picking_type_id.code == 'incoming':
                        for line in l.move_line_ids_without_package:
                            if k.product_id.id == line.product_id.id:
                                k.return_qty = line.qty_done

    def get_print_date(self):
        now_utc_date = datetime.now()
        now_dubai = now_utc_date.astimezone(timezone('Asia/Karachi'))
        return now_dubai.strftime('%d/%m/%Y %H:%M:%S')


class StockLandedInh(models.Model):
    _inherit = 'stock.landed.cost'

    vendor_bill_ids = fields.Many2many('account.move')
    description = fields.Char()

    def action_show_line(self):
        vals_list = []
        for rec in self.vendor_bill_ids:
            for line in rec.invoice_line_ids:
                vals_list.append([0, 0, {
                    'account_id': line.account_id.id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'price_unit': line.price_unit,
                    'split_method': 'equal',
                }])
        self.cost_lines = vals_list
