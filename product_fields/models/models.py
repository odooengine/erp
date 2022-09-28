from odoo import api, models, fields


class StatusProduct(models.Model):
    _inherit = "product.product"

    status = fields.Char(string='Status')
    book_number = fields.Float(string='Book No')


class StatusProductTemplate(models.Model):
    _inherit = "product.template"

    status = fields.Char(string='Status')
    book_number = fields.Float(string='Book No')
