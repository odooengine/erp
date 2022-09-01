# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountInh(models.Model):
    _inherit = 'account.account'

    is_carpenter_bill = fields.Boolean()


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    is_carpenter = fields.Boolean()


class CarpenterBill(models.Model):
    _name = 'carpenter.bill'
    _rec_name = 'partner_id'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    vendor_id = fields.Many2one('res.partner')
    move_ids = fields.Many2many('account.move')
    date = fields.Date()
    move_id = fields.Many2one('account.move')
    amount_total = fields.Float(compute='compute_total')
    is_created = fields.Boolean()

    bill_lines = fields.One2many('carpenter.bill.line', 'bill_id')

    def compute_total(self):
        total = 0
        for line in self.bill_lines:
            total = total + (line.quantity * line.price_unit)

        self.amount_total = total


    def action_create_bill(self):
        line_vals = []
        account = self.env['account.account'].search([('is_carpenter_bill', '=', True)], limit=1)
        if not account:
            raise UserError('Expense Account Not Found')
        for line in self.bill_lines:
            line_vals.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'price_unit': line.price_unit,
                'quantity': line.quantity,
                'account_id': account.id
            }))

        bill = {
            'invoice_line_ids': line_vals,
            'partner_id': self.vendor_id.id,
            # 'branch_id': self.branch_id.id,
            'invoice_date': self.date,
            'date': self.date,
            'state': 'draft',
            # 'hide_jv_link': True,
            # 'journal_id': self.lease_journal_id.id,
            'move_type': 'in_invoice'
        }
        record = self.env['account.move'].create(bill)
        record.action_post()
        self.move_id = record.id
        self.is_created = True

    def action_add_lines(self):
        line_vals = []
        for invoice in self.move_ids:

            for line in invoice.invoice_line_ids:
                line_vals.append((0, 0, {
                    'partner_id': invoice.partner_id.id,
                    'product_id': line.product_id.id,
                    'move_id': invoice.id,
                    'uom_id': line.product_uom_id.id,
                    'price_unit': line.price_unit,
                    'quantity': line.quantity,
                    'subtotal': line.quantity * line.price_unit,
                }))
        self.bill_lines = line_vals


class CarpenterBillLine(models.Model):
    _name = 'carpenter.bill.line'

    bill_id = fields.Many2one('carpenter.bill')
    partner_id = fields.Many2one('res.partner')
    move_id = fields.Many2one('account.move')
    product_id = fields.Many2one('product.product')
    uom_id = fields.Many2one('uom.uom')
    quantity = fields.Float()
    price_unit = fields.Float()
    subtotal = fields.Float(compute='compute_subtotal')

    @api.depends('price_unit', 'quantity')
    def compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.price_unit * rec.quantity

