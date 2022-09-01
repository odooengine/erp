from odoo import api, fields, models


class PartnerHICReport(models.TransientModel):
    _inherit = 'partner.ledger'

    def partner_hic_report(self):
        print("Click")
        data = {'partner_id': self.partner_id.id,
                'start_date': self.start_date,
                'end_date': self.end_date}
        return self.env.ref('partner_hic_report.partner_ledger_hic_pdf').report_action(self, data)