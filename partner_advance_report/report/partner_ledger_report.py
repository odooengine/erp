# -*- coding: utf-8 -*-


from odoo import models
from datetime import datetime
from pytz import timezone


class CustomReport(models.AbstractModel):
    _name = "report.partner_advance_report.advance_ledger_pdf_report"

    def get_partner_old(self, data):
        employee = self.env['hr.employee'].search([('address_home_id', '=', data)])

        # rec.employee_id.partner_ids:
        # employee = -1
        for p in employee.partner_ids:
            if not p.is_current:
                employee = p
        # bal = 0
        p_list = []
        # if employee != -1:
        partner_ledger = self.env['account.move.line'].search(
            [('partner_id', '=', employee.id),
             ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
             ('full_reconcile_id', '=', False), '|', '|',
             ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'),
             ('account_id.internal_type', '=', 'other')])

        for par_rec in partner_ledger:
            if par_rec.account_id.user_type_id.name != 'Current Liabilities':
                p_list.append(par_rec.id)
        #             bal = bal + (par_rec.debit - par_rec.credit)
        # rec.current_balance = bal
        # partner_ledger = self.env['account.move.line'].search(
        #     [('partner_id', 'in', employee.partner_ids.ids),
        #      ('move_id.state', '=', 'posted'), ('balance', '!=', 0),
        #      ('account_id.name', '=', 'Old Advance')]).sorted(key=lambda r: r.date)
        partner_ledger = self.env['account.move.line'].browse(p_list).sorted(key=lambda r: r.date)
        return partner_ledger

    def get_partner_current(self, data):
        employee = self.env['hr.employee'].search([('address_home_id', '=', data)])

        # rec.employee_id.partner_ids:
        # employee = -1
        for p in employee.partner_ids:
            if p.is_current:
                employee = p
        # bal = 0
        p_list = []
        # if employee != -1:
        partner_ledger = self.env['account.move.line'].search(
            [('partner_id', '=', employee.id),
             ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
             ('full_reconcile_id', '=', False), '|', '|',
             ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'),
             ('account_id.internal_type', '=', 'other')])

        for par_rec in partner_ledger:
            if par_rec.account_id.user_type_id.name != 'Current Liabilities':
                p_list.append(par_rec.id)
        #             bal = bal + (par_rec.debit - par_rec.credit)
        # rec.current_balance = bal
        # partner_ledger = self.env['account.move.line'].search(
        #     [('partner_id', 'in', employee.partner_ids.ids),
        #      ('move_id.state', '=', 'posted'), ('balance', '!=', 0),
        #      ('account_id.name', '=', 'Old Advance')]).sorted(key=lambda r: r.date)
        partner_ledger = self.env['account.move.line'].browse(p_list).sorted(key=lambda r: r.date)
        return partner_ledger

    # def get_partner_current(self, data):
        # employee = self.env['hr.employee'].search([('address_home_id', '=', data)])
        # partner_ledger = self.env['account.move.line'].search(
        #     [('partner_id', 'in', employee.partner_ids.ids),
        #      ('move_id.state', '=', 'posted'), ('balance', '!=', 0), ('account_id.name', '=', 'Current Advance')]).sorted(key=lambda r: r.date)
        # return partner_ledger

    # def get_opening_bal(self, data):
    #     open_bal = self.env['account.move.line'].search(
    #         [('partner_id', '=', data['partner_id']), ('date', '<', data['start_date']),
    #          ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
    #          ('account_id.reconcile', '=', True), ('full_reconcile_id', '=', False), '|',
    #          ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable')])
    #     bal = 0
    #     for rec in open_bal:
    #         bal = bal + rec.balance
    #     return bal
    #
    # def get_foreign_opening_bal(self, data):
    #     open_bal = self.env['account.move.line'].search(
    #         [('partner_id', '=', data['partner_id']), ('date', '<', data['start_date']),
    #          ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
    #          ('account_id.reconcile', '=', True), ('full_reconcile_id', '=', False), '|',
    #          ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable')])
    #     bal = 0
    #     for rec in open_bal:
    #         bal = bal + rec.amount_currency
    #     return bal
    #
    # def get_closing_bal(self, data):
    #     open_bal = self.env['account.move.line'].search(
    #         [('partner_id', '=', data['partner_id']), ('date', '>=', data['start_date']), ('date', '<=', data['end_date']),
    #          ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
    #          ('account_id.reconcile', '=', True), ('full_reconcile_id', '=', False), '|',
    #          ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable')])
    #     bal = 0
    #     for rec in open_bal:
    #         bal = bal + rec.balance
    #     return bal

    def get_print_date(self):
        now_utc_date = datetime.now()
        now_dubai = now_utc_date.astimezone(timezone('Asia/Karachi'))
        return now_dubai.strftime('%d/%m/%Y %H:%M:%S')

    def _get_report_values(self, docids, data=None):
        old = self.get_partner_old(docids)
        current = self.get_partner_current(docids)
        partner = self.env['res.partner'].browse([docids[0]])
        return {
            'doc_ids': self.ids,
            'doc_model': 'partner.ledger',
            'print_date': self.get_print_date(),
            'login_user': self.env.user.name,
            'old': old,
            'current': current,
            'partner': partner,
        }
