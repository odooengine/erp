# -*- coding: utf-8 -*-


import ast
from odoo import api, models
from datetime import datetime
from pytz import timezone


class SaleReportCustom(models.AbstractModel):
    _name = 'report.general_ledger_report_pdf.report_general_document'

    def get_ledgers(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        ledgers = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                       ('date', '<=', rec_model.date_to), ('move_id.state', '=', 'posted'),
                                                       ('account_id', '=', rec_model.account_id.id),
                                                        ('is_check', '=', False)], order="date asc")
        return ledgers

    def get_opening_bal(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        open_bal = self.env['account.move.line'].search(
            [('account_id', '=', rec_model.account_id.id), ('date', '<', rec_model.date_from),
             ('move_id.state', '=', 'posted'),('is_check', '=', False)])
        bal = 0
        for rec in open_bal:
            bal = bal + rec.balance
        return bal

    def get_closing_bal(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        open_bal = self.env['account.move.line'].search(
            [('account_id', '=', rec_model.account_id.id), ('date', '>=', rec_model.date_from), ('date', '<=', rec_model.date_to),
             ('move_id.state', '=', 'posted'),('is_check', '=', False)])
        bal = 0
        for rec in open_bal:
            bal = bal + rec.balance
        return bal

    def get_print_date(self):
        now_utc_date = datetime.now()
        now_dubai = now_utc_date.astimezone(timezone('Asia/Karachi'))
        return now_dubai.strftime('%d/%m/%Y %H:%M:%S')

    def get_summary_ledgers(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        if rec_model.type == 'summary':
            lines = self.env['account.move.line'].search([('date', '>=', rec_model.date_from),
                                                          ('date', '<=', rec_model.date_to),
                                                          ('move_id.state', '=', 'posted'),
                                                          ('account_id', '=', rec_model.account_id.id),
                                                          ('is_check', '=', False)],
                                                         order="date asc")

            val_list = []
            val = []
            for rec in lines:
                if rec.account_id.id not in val_list:
                    val_list.append({
                        'account_id': rec.account_id.id,
                        'account_name': rec.account_id.name,
                        'debit': rec.debit,
                        'credit': rec.credit,
                        'balance': rec.debit - rec.credit,
                    })

            for record in lines:
                if record.account_id.id not in val:
                    val.append({
                        'account_id': record.account_id.id,
                        'account_name': record.account_id.name,
                        'debit': record.debit,
                        'credit': record.credit,
                        'balance': record.debit - record.credit,
                        # 'name': record.name,
                        # 'date': record.date,
                        # 'move_id': record.move_id.name,
                    })
            new_list = []
            for l in val_list:
                bal = 0
                db = 0
                cr = 0
                if l['account_id'] not in new_list:
                    for i in val:
                        if i['account_id'] == l['account_id']:
                            new_list.append(l['account_id'])
                            bal = bal + i['balance']
                            db = db + i['debit']
                            cr = cr + i['credit']
                    for j in val:
                        if j['account_id'] == l['account_id']:
                            j['balance'] = bal
                            j['debit'] = db
                            j['credit'] = cr

            # list_org_updated = [str(item) for item in val]
            # unique_set = set(list_org_updated)
            # unique_list = [ast.literal_eval(item) for item in unique_set]
            # sorted_list = sorted(unique_list, key=lambda i: i['account_id'])
            # print(sorted_list)
            return val[0]

        # return ledgers

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': self.ids,
            'user': self.env.user.name,
            'doc_model': 'general_ledger_report_pdf.general.ledger.wizard',
            'date_from': rec_model.date_from,
            'date_to': rec_model.date_to,
            'account': rec_model.account_id.name,
            'type': rec_model.type,
            'print_date': self.get_print_date(),
            'ledgers': self.get_ledgers(),
            'summary': self.get_summary_ledgers(),
            'opening': self.get_opening_bal(),
            'closing': self.get_closing_bal() + self.get_opening_bal(),
        }
