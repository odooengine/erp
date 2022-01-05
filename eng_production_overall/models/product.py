from odoo import models, fields


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    requisition_location_id = fields.Many2one('stock.location')
