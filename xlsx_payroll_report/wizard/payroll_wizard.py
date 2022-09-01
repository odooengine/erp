from odoo import fields, api, models


class PayrollWiz(models.TransientModel):
    _name = 'payroll.payslip.wizard'

    partner_id = fields.Many2one('res.partner', string='Address')
    struct_id = fields.Many2one('hr.payroll.structure', string='Structure')

    def print_report(self):
        data = {'partner_id': self.partner_id.id, 'struct_id': self.struct_id.id}
        return self.env.ref('xlsx_payroll_report.payroll_report_pdf_workcenter_wise').report_action(self, data)


class PayrollRollWizard(models.Model):
    _inherit = "hr.payslip.run"

    def action_open_payroll_wiz(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payroll Report',
            'view_id': self.env.ref('xlsx_payroll_report.payroll_wizard_report', False).id,
            'target': 'new',
            'res_model': 'payroll.payslip.wizard',
            'view_mode': 'form',
        }
