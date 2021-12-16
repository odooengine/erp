# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _


class AgeGroup(models.Model):
    _name = 'age.group'
    _description = 'Age Group'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class CalenderSeason(models.Model):
    _name = 'calender.season'
    _description = 'Calender Season'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class ClassFabric(models.Model):
    _name = 'class.fabric'
    _description = 'Class Fabric'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class LineItem(models.Model):
    _name = 'line.item'
    _description = 'Line item'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'Product Group'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class SizeRange(models.Model):
    _name = 'size.range'
    _description = 'Size Range'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Calender Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Class Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Product Group')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type = fields.Selection([('outlet', 'Outlet'),
                                  ('regular', 'Regular'),
                                  ], string='Life Type')


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Calender Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Class Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Product Group')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type = fields.Selection([('outlet', 'Outlet'),
                                  ('regular', 'Regular'),
                                  ], string='Life Type')
