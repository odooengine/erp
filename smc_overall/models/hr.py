from datetime import datetime
from pytz import timezone

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrContractInh(models.Model):
    _inherit = 'hr.contract'

    bonus = fields.Float('Bonus')


class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'

    partner_ids = fields.Many2many('res.partner')
    my_activity_date_deadline  = fields.Date()


class HrPayslipInh(models.Model):
    _inherit = 'hr.payslip'

    conveyance = fields.Float('Old Advance')
    mobile_allowance = fields.Float('Current Advance')
    meal_allowance = fields.Float('Absent Days')
    balance = fields.Float('Old Balance')
    current_balance = fields.Float('Current Balance')
    address_id = fields.Many2one('res.partner')
    work_location = fields.Char('Work Location')

    net_wage_total = fields.Float('Net Wage')
    net_wage_basic = fields.Float('Basic Wage')
    total_deductions = fields.Float('Total Deductions')
    days_dec = fields.Float('Days Dec')
    bonus = fields.Float('Bonus')

    def action_add_address(self):
        for rec in self:
            rec.move_id.address_id = rec.address_id.id

    def action_payslip_done(self):
        record = super(HrPayslipInh, self).action_payslip_done()
        for rec in self:
            new_partner = ''
            old_partner = ''
            if rec.employee_id.partner_ids:
                for partner in rec.employee_id.partner_ids:
                    if partner.is_current:
                        new_partner = partner.id
                    if not partner.is_current:
                        old_partner = partner.id
            for line in rec.move_id.line_ids:
                if line.account_id.is_new:
                    line.partner_id = new_partner
                if line.account_id.is_old:
                    line.partner_id = old_partner
        return record

    def compute_sheet(self):
        payslips = self.filtered(lambda slip: slip.state in ['draft', 'verify'])
        # delete old payslip lines
        payslips.line_ids.unlink()
        for payslip in payslips:
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
            payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today(), 'address_id': payslip.employee_id.address_id.id,
                           'work_location': payslip.employee_id.work_location})
            total_ded = 0
            for rec in payslip.line_ids:
                if rec.code == 'NET':
                    payslip.net_wage_total = rec.total
                if rec.category_id.code == 'DED':
                    total_ded = total_ded + rec.total
                if rec.code == 'ADS':
                    payslip.days_dec = rec.total
                if rec.code == 'BO':
                    payslip.bonus = rec.total
            payslip.total_deductions = total_ded
            payslip.net_wage_basic = payslip.contract_id.wage
        return True

    def compute_current_balance(self,):
        for rec in self:
            if rec.employee_id.partner_ids:
                employee = -1
                for p in rec.employee_id.partner_ids:
                    if p.is_current:
                        employee = p
                bal = 0
                if employee != -1:
                    partner_ledger = self.env['account.move.line'].search(
                        [('partner_id', '=', employee.id),
                         ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
                          ('full_reconcile_id', '=', False), '|', '|',
                         ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'), ('account_id.internal_type', '=', 'other')])

                    for par_rec in partner_ledger:
                        if par_rec.account_id.user_type_id.name != 'Current Liabilities':
                            bal = bal + (par_rec.debit - par_rec.credit)
                rec.current_balance = bal
            else:
                rec.current_balance = 0

    def compute_balance(self):
        for rec in self:
            if rec.employee_id.partner_ids:
                employee = -1
                for p in rec.employee_id.partner_ids:
                    if not p.is_current:
                        employee = p
                bal = 0
                if employee != -1:
                    # partner_ledger = self.env['account.move.line'].search(
                    #     [('partner_id', '=', employee.id),
                    #      ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
                    #      ('account_id.reconcile', '=', True), ('full_reconcile_id', '=', False), '|',
                    #      ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable')])
                    partner_ledger = self.env['account.move.line'].search(
                        [('partner_id', '=', employee.id),
                         ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0), '|', '|',
                          ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'), ('full_reconcile_id', '=', False), ('account_id.internal_type', '=', 'other')])
                    for par_rec in partner_ledger:
                        if par_rec.account_id.user_type_id.name != 'Current Liabilities':
                            bal = bal + (par_rec.debit - par_rec.credit)
                rec.balance = bal
            else:
                rec.balance = 0

    # def compute_current_balance(self):
    #     for rec in self:
    #         if rec.employee_id.partner_ids:
    #             employee = -1
    #             for p in rec.employee_id.partner_ids:
    #                 if p.is_current:
    #                     employee = p
    #             bal = 0
    #             if employee != -1:
    #                 partner_ledger = self.env['account.move.line'].search(
    #                     [('partner_id', '=', employee.id),
    #                      ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
    #                       ('full_reconcile_id', '=', False), '|', '|',
    #                      ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'), ('account_id.internal_type', '=', 'other')])
    #
    #                 for par_rec in partner_ledger:
    #                     if par_rec.account_id.user_type_id.name != 'Current Liabilities':
    #                         bal = bal + (par_rec.debit - par_rec.credit)
    #             rec.current_balance = bal
    #         else:
    #             rec.current_balance = 0
    #
    # def compute_balance(self):
    #     for rec in self:
    #         if rec.employee_id.partner_ids:
    #             employee = -1
    #             for p in rec.employee_id.partner_ids:
    #                 if not p.is_current:
    #                     employee = p
    #             bal = 0
    #             if employee != -1:
    #                 # partner_ledger = self.env['account.move.line'].search(
    #                 #     [('partner_id', '=', employee.id),
    #                 #      ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0),
    #                 #      ('account_id.reconcile', '=', True), ('full_reconcile_id', '=', False), '|',
    #                 #      ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable')])
    #                 partner_ledger = self.env['account.move.line'].search(
    #                     [('partner_id', '=', employee.id),
    #                      ('move_id.state', '=', 'posted'), ('full_reconcile_id', '=', False), ('balance', '!=', 0), '|', '|',
    #                       ('account_id.internal_type', '=', 'payable'), ('account_id.internal_type', '=', 'receivable'), ('full_reconcile_id', '=', False), ('account_id.internal_type', '=', 'other')])
    #                 print(partner_ledger)
    #                 for par_rec in partner_ledger:
    #                     print(par_rec.name)
    #                     print()
    #                     if par_rec.account_id.user_type_id.name != 'Current Liabilities':
    #                         bal = bal + (par_rec.debit - par_rec.credit)
    #             rec.balance = bal
    #         else:
    #             rec.balance = 0

    def action_compute_deductions(self):
        for rec in self:
            total = rec.meal_allowance + rec.mobile_allowance + rec.conveyance
            for line in rec.line_ids:
                if line.code == 'NET':
                    line.amount = line.amount - total
                if line.code == 'OAD':
                    line.amount = rec.conveyance
                    line.total = rec.conveyance
                if line.code == 'CAD':
                    line.amount = rec.mobile_allowance
                    line.total = rec.mobile_allowance
                if line.code == 'ADS':
                    line.amount = rec.meal_allowance
                    line.total = rec.meal_allowance
        self.compute_current_balance()
        self.compute_balance()
            # val = {
            #     'Conveyance': rec.conveyance
            # }
            # vals_list = []
            # category = self.env['hr.salary.rule.category'].search([('code', '=', 'DED')])
            # oad = self.env['hr.salary.rule'].search([('code', '=', 'OAD')])
            # vals_list.append([0, 0, {
            #     'name': 'Old Advance',
            #     'code': 'OAD',
            #     'sequence': 101,
            #     'category_id': category.id,
            #     'salary_rule_id': oad.id,
            #     'amount': rec.conveyance,
            #     'total': rec.conveyance,
            #     'quantity': 1,
            # }])
            #
            # cad = self.env['hr.salary.rule'].search([('code', '=', 'CAD')])
            # vals_list.append([0, 0, {
            #     'name': 'Current Advance',
            #     'code': 'CAD',
            #     'category_id': category.id,
            #     'sequence': 101,
            #     'salary_rule_id': cad.id,
            #     'amount': rec.mobile_allowance,
            #     'total': rec.mobile_allowance,
            #     'quantity': 1,
            # }])
            # ads = self.env['hr.salary.rule'].search([('code', '=', 'ADS')])
            # vals_list.append([0, 0, {
            #     'name': 'Absent Days',
            #     'code': 'ADS',
            #     'sequence': 101,
            #     'category_id': category.id,
            #     'salary_rule_id': ads.id,
            #     'amount': rec.meal_allowance,
            #     'total': rec.meal_allowance,
            #     'quantity': 1,
            # }])
            # rec.line_ids = vals_list
            # total = rec.meal_allowance + rec.mobile_allowance + rec.conveyance
            # for line in rec.line_ids:
            #     if line.code == 'NET':
            #         line.amount = line.amount - total


    def action_payslip_wizard(self):
        payslip_list = []
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['hr.payslip'].browse(selected_ids)

        for record in selected_records:
            line = (0, 0, {
                    'slip_id': record.id,
                    'employee_id': record.employee_id.id,
                    'old_advance': record.balance,
                    'current_advance': record.current_balance,
                    'conveyance': record.conveyance,
                    'mobile_allowance': record.mobile_allowance,
                    'meal_allowance': record.meal_allowance,
                })
            payslip_list.append(line)
        return {
                'type': 'ir.actions.act_window',
                'name': 'Payroll Payment',
                'view_id': self.env.ref('smc_overall.view_payroll_wizard_form', False).id,
                'target': 'new',
                'context': {'default_payslip_line': payslip_list},
                'res_model': 'payroll.wizard',
                'view_mode': 'form',
            }


class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'

    wage = fields.Float('Wage', compute='_compute_wage')

    def _compute_wage(self):
        for rec in self:
            contract = self.env['hr.contract'].search([('employee_id', '=', rec.id)], limit=1)
            if contract:
                rec.wage = contract.wage
            else:
                rec.wage = 0
