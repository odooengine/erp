# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InventoryCategories(models.Model):
    _name = 'smc.product.category'
    _description = 'SMC Product Category'
    _rec_name = 'category'

    category = fields.Char('Category')
