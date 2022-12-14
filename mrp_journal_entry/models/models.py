# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api


class MRProductInherit(models.Model):
    _inherit = "mrp.production"

    # action = super(MRProductInherit,self).button_mark_done()

    def button_mark_done(self):
        res = super(MRProductInherit, self).button_mark_done()
        domain = [('id', 'in',
                   (self.move_raw_ids + self.move_finished_ids + self.scrap_ids.move_id).stock_valuation_layer_ids.ids)]
        data = self.env['stock.valuation.layer'].search(domain)
        for r in data:
            lines = []
            account = []
            value = 0
            if r.product_id.type != 'product':
                for p in self.move_raw_ids:
                    if p.product_id.name == r.product_id.name:
                        account = p.location_dest_id.valuation_in_account_id.id
                        value = p.quantity_done
                if value and account:
                    move_dict = {
                        'ref': f'{self.name} - {r.product_id.name}"',
                        'move_type': 'entry',
                        'journal_id': r.product_id.categ_id.property_stock_journal.id,
                        'date': date.today(),
                        'state': 'draft',
                    }
                    debit_line = (0, 0, {
                        'name': f'{self.name} - {r.product_id.name}"',
                        'debit': r.product_id.standard_price * value,
                        'credit': 0.0,
                        'account_id': account,
                        # 'analytic_tag_ids': self.branch_id.analytical_tag_id.ids,
                        # 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
                    })
                    lines.append(debit_line)
                    credit_line = (0, 0, {
                        'name': f'{self.name} - {r.product_id.name}"',
                        'debit': 0.0,
                        # 'partner_id': r.partner_id.id,
                        'credit': r.product_id.standard_price * value,
                        'account_id': r.product_id.property_account_expense_id.id,
                        # 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
                    })
                    lines.append(credit_line)
                    print(debit_line)
                    print(credit_line)
                    move_dict['line_ids'] = lines
                    move = self.env['account.move'].create(move_dict)
                    print(move)
                    move.action_post()
                    move.button_review()
                    move.button_approved()
                    r.entry_move_id = move.id
        return res


class StockValuationInherit(models.Model):
    _inherit = "stock.valuation.layer"

    entry_move_id = fields.Many2one('account.move', string="Journal Entry(Custom)")


class ProductCategory(models.Model):
    _inherit = "product.category"

    is_eng = fields.Boolean(string="Engine")
    is_mk = fields.Boolean(string="MK")
    # user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)


class ProductInherit(models.Model):
    _inherit = "product.product"

    categ_ids = fields.Many2many('product.category', string='Categ', compute='compute_categ_ids')

    @api.depends('categ_id')
    def compute_categ_ids(self):
        if len(self.env.user.company_ids) < 2:
            print("dddddddd")
            if self.env.user.company_ids.id == 1:
                print("sssssss")
                categories = self.env['product.category'].search([('is_eng', '=', True)])
                self.categ_ids = categories.ids
            elif self.env.user.company_ids.id == 2:
                print("cccccccc")
                categories = self.env['product.category'].search([('is_mk', '=', True)])
                self.categ_ids = categories.ids
        elif len(self.env.user.company_ids) > 1:
            print("bbbbbbbb")
            categories = self.env['product.category'].search([])
            self.categ_ids = categories.ids
        print(self.categ_ids)


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    categ_ids = fields.Many2many('product.category', string='Categ', compute='compute_categ_ids')

    @api.depends('categ_id')
    def compute_categ_ids(self):
        if len(self.env.user.company_ids) < 2:
            print("dddddddd")
            if self.env.user.company_ids.id == 1:
                print("sssssss")
                categories = self.env['product.category'].search([('is_eng', '=', True)])
                self.categ_ids = categories.ids
            elif self.env.user.company_ids.id == 2:
                print("cccccccc")
                categories = self.env['product.category'].search([('is_mk', '=', True)])
                self.categ_ids = categories.ids
        elif len(self.env.user.company_ids) > 1:
            print("bbbbbbbb")
            categories = self.env['product.category'].search([])
            self.categ_ids = categories.ids
        print(self.categ_ids)
