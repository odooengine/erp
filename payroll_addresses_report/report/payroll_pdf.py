from odoo import models,api,fields
import string
from datetime import datetime,date, timedelta


class ReportPayrollppdf(models.AbstractModel):
    _name = 'report.payroll_addresses_report.payroll_wizard_report_id_pdf'
    _description = 'Get hash integrity result as PDF.'

    def get_work_addr_emps(self, work_addr):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        payslips = self.env['hr.payslip'].search([('address_id.name', '=', work_addr),('payslip_run_id','=',rec_model.id)])
        slip = []
        for line in payslips:
            slip.append({
                'GROSS': line.net_wage_basic,
                'old_advance': line.balance,
                'cur_advance': line.current_balance,
                'abs_days': line.meal_allowance,
                'days_deduc': line.days_dec,
                'old_deduc': line.conveyance,
                'cur_deduc': line.mobile_allowance,
                'total_deduc': line.total_deductions,
                'net_deduc': line.net_wage_total,
            })

        r1 = sum([x['GROSS'] for x in slip])
        r2 = sum([x['old_advance'] for x in slip])
        r3 = sum([x['cur_advance'] for x in slip])
        r4 = sum([x['abs_days'] for x in slip])
        r5 = sum([x['days_deduc'] for x in slip])
        r6 = sum([x['old_deduc'] for x in slip])
        r7 = sum([x['cur_deduc'] for x in slip])
        r8 = sum([x['total_deduc'] for x in slip])
        r9 = sum([x['net_deduc'] for x in slip])

        record = [slip,r1,r2,r3,r4,r5,r6,r7,r8,r9]
        # print('ggggg',slip)
        return record

    # def get_total(self):
    #     slip = self.get_work_addr_emps()
    #     total = 0
    #     for s in range(len(slip)):
    #         total += slip[s]['GROSS']
    #     return total

    def get_cash(self, w_adr):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        payslips = sum(self.env['hr.payslip'].search(
            [('address_id.name', '=', w_adr), ('payslip_run_id', '=', rec_model.id), ('struct_id.name', '=', 'Cash Employees')]).mapped('net_wage_total'))
        print(payslips)
        print('hello')
        return payslips

    def get_bank(self, w_adr):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        payslips = sum(self.env['hr.payslip'].search(
            [('address_id.name', '=', w_adr), ('payslip_run_id', '=', rec_model.id), ('struct_id.name', '=', 'Bank Employees')]).mapped('net_wage_total'))
        print(payslips)
        print('hello')
        return payslips
    @api.model
    def _get_report_values(self, docids, data=None):
        addreses = data['partner_id']
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        docs = self.env['hr.payslip.run'].browse(docids)
        addreses_list = []
        for rec in rec_model.slip_ids:
            if rec.address_id.id in addreses:
                addreses_list.append(rec.id)
        # print(addreses_list)
        slips = self.env['hr.payslip'].browse(addreses_list)
        work_addr_lst = slips.address_id.mapped('name')
        # print(work_addr_lst)

        return {
            'doc_ids': docids,
            'doc_model': 'report.wizard',
            'data': data,
            'docs': docs,
            'work_addres':work_addr_lst,
            'rec_model': rec_model,
            'get_emps': self.get_work_addr_emps,
            'get_cash': self.get_cash,
            'get_bank': self.get_bank,
           }
     