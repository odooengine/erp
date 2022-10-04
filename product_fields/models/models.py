from odoo import api, models, fields


class StatusProduct(models.Model):
    _inherit = "product.product"

    status = fields.Char(string='Status')
    book_number = fields.Char(string='Book No')

    # @api.model
    # def create(self, vals):
    #     res = super(StatusProduct, self).create(vals)
    #     res.product_tmpl_id.update({
    #         'status': res.status,
    #         'book_number': res.book_number,
    #
    #     })
    #     return res


class StatusProductTemplate(models.Model):
    _inherit = "product.template"

    status = fields.Char(string='Status')
    book_number = fields.Char(string='Book No')

    @api.model
    def create(self, vals):
        res = super(StatusProductTemplate, self).create(vals)
        res.product_variant_ids.update({
            'status': res.status,
            'book_number': res.book_number,
        })
        return res

    def write(self, vals):
        res = super(StatusProductTemplate, self).write(vals)
        if 'status' or 'book_number' in vals:
            self.product_variant_ids.update({
                'status': self.status,
                'book_number': self.book_number,
            })
        return res
