from odoo import api, fields, models


class PayrollReport(models.Model):
    _inherit = "hr.payslip.run"


    def action_payroll_report(self):
        print("u click")
        rec = self.env.ref('payroll_addresses_report.report_wizard_action').read()[0]
        return rec