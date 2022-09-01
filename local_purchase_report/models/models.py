from odoo import models, fields, api


class LocalPurchaseReport(models.TransientModel):
    _name = 'local.purchase'

    product_id = fields.Many2one('product.product')

    def report_action(self):
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('local_purchase_report.test_report_pdf').report_action(self, data=data)
