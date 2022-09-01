from odoo import models, fields, api


class InventorySeries(models.Model):
    _name = 'smc.product.series'
    _description = 'SMC Product Series'
    _rec_name = 'series'

    series = fields.Char('Series')