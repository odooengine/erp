from odoo import models, fields, api


class InventoryBrands(models.Model):
    _name = 'smc.product.brands'
    _description = 'SMC Product Brand'
    _rec_name = 'brand'

    brand = fields.Char('Brand')
