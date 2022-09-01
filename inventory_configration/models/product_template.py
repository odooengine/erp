from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'product.template'

    category_id = fields.Many2one('smc.product.category', 'Category')
    brand_id = fields.Many2one('smc.product.brands', 'Brands')
    series_id = fields.Many2one('smc.product.series', 'Series')
