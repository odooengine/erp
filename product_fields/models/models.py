from odoo import api, models, fields


class StatusProduct(models.Model):
    _inherit = "product.product"

    status = fields.Char(string='Status')
    book_number = fields.Float(string='Book No')

    @api.model
    def create(self, vals):
        res = super(StatusProduct, self).create(vals)
        res.product_tmpl_id.update({
            'status': res.status,
            'book_number': res.book_number,

        })
        return res


class StatusProductTemplate(models.Model):
    _inherit = "product.template"

    status = fields.Char(string='Status')
    book_number = fields.Float(string='Book No')
