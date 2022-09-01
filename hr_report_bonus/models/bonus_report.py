from odoo import api, fields, models, _


class BonusReport(models.TransientModel):
    _name = "bonus.report"
    _description = "Bonus Report"

    word_address_id = fields.Many2one('res.partner', string='Work Address')
    previous_bonus_show = fields.Boolean(string="Show Previous Bonus" , default=False)


    def report_pdf_print(self):
        print("click")
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('hr_report_bonus.bonus_report_pdf').report_action(self, data=data)
