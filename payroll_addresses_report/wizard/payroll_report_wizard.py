from odoo import fields, api, models


class ReportWizard(models.TransientModel):
    _name = 'report.wizard'

    partner_id = fields.Many2many('res.partner', string='Address')

    def print_report(self):
        # print("u click")
        data = {'partner_id': self.partner_id.ids}
        # print(data)
        return self.env.ref('payroll_addresses_report.payroll_wizard_report_pdf').report_action(self, data)

        # data = {
        #     'form': self.read()[0],
        # }
        # return self.env.ref('payroll_addresses_report.payroll_wizard_report_pdf').report_action(self, data=data)


