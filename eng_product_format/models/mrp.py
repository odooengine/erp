# -*- coding: utf-8 -*-


from xml import etree
from lxml import etree
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _


class MRPInherit(models.Model):
    _inherit = 'mrp.production'

    categ_id = fields.Many2one('product.category', string='Product Category', store=True)
    calender_season_id = fields.Many2one('calender.season', string='Season', store=True)
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric', store=True)
    life_type_id = fields.Many2one('life.type', string='Life Type', store=True)
    item_cat_id = fields.Many2one('item.category', string='Class', store=True)
    engine_year_id = fields.Many2one('engine.year', string='Year', store=True)
    dept_id = fields.Selection([('boys', 'Boys'),
                                ('girls', 'Girls'),
                                ('men', 'Men'),
                                ('women', 'Women'),
                                ('unisex', 'Unisex'),
                                ], string='Department', store=True)
    sub_dept = fields.Selection([('infant', 'Infant'),
                                 ('toddlers', 'Toddlers'),
                                 ('kids', 'Kids'),
                                 ('boys', 'Boys'),
                                 ('girls', 'Girls'),
                                 ('men', 'Men'),
                                 ('women', 'Women'),
                                 ('unisex', 'Unisex'),
                                 ], string='Sub Department', store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.categ_id = self.product_id.categ_id.id
        self.engine_year_id = self.product_id.engine_year_id.id
        self.calender_season_id = self.product_id.calender_season_id.id
        self.class_fabric_id = self.product_id.class_fabric_id.id
        self.item_cat_id = self.product_id.item_cat_id.id
        self.dept_id = self.product_id.dept_id
        self.sub_dept = self.product_id.sub_dept
        self.life_type_id = self.product_id.life_type_id.id