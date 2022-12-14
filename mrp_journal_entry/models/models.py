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
        print("data" ,data)
        for r in self.move_raw_ids:
            lines = []
            account = []
            value = 0
            if r.product_id.type != 'product':
                # for p in data:
                #     if p.product_id == r.product_id:
                #         # account = r.location_dest_id.valuation_in_account_id.id
                #         value = p.value
                # # print(account)
                # print(value)
                # if value:
                move_dict = {
                    'ref':  f'{self.name} - {r.product_id.name}"',
                    'move_type': 'entry',
                    'journal_id': r.product_id.categ_id.property_stock_journal.id,
                    'date': date.today(),
                    'state': 'draft',
                }
                debit_line = (0, 0, {
                    'name':  f'{self.name} - {r.product_id.name}"',
                    'debit': r.product_id.standard_price * r.quantity_done,
                    'credit': 0.0,
                    'account_id': r.location_dest_id.valuation_in_account_id.id,
                    # 'analytic_tag_ids': self.branch_id.analytical_tag_id.ids,
                    # 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
                })
                lines.append(debit_line)
                credit_line = (0, 0, {
                    'name': f'{self.name} - {r.product_id.name}"',
                    'debit': 0.0,
                    # 'partner_id': r.partner_id.id,
                    'credit': r.product_id.standard_price * r.quantity_done,
                    'account_id': r.product_id.property_account_expense_id.id,
                    # 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
                })
                lines.append(credit_line)
                # print(debit_line)
                # print(credit_line)
                move_dict['line_ids'] = lines
                print(move_dict)
                move = self.env['account.move'].create(move_dict)
                print(move)
                # self.journal_entry_id = move.id
                move.action_post()
                move.button_review()
                move.button_approved()
        return res
