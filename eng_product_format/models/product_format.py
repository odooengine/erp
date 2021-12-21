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
    code = fields.Char(string='Code', tracking=True)


class ClassFabric(models.Model):
    _name = 'class.fabric'
    _description = 'Class Fabric'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class LineItem(models.Model):
    _name = 'line.item'
    _description = 'Line item'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'Grade'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class SizeRange(models.Model):
    _name = 'size.range'
    _description = 'Size Range'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)


class Department(models.Model):
    _name = 'class.department'
    _description = 'Department'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class AccessoriesType(models.Model):
    _name = 'accessories.type'
    _description = 'Accessories Type'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class LifeType(models.Model):
    _name = 'life.type'
    _description = 'Life Type'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class ItemSubCategory(models.Model):
    _name = 'item.sub.category'
    _description = 'Item Sub Category'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class ItemCategory(models.Model):
    _name = 'item.category'
    _description = 'Item Category'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class EngineYear(models.Model):
    _name = 'engine.year'
    _description = 'Year'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    name_seq = fields.Char(string='Sequence')

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Grade')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    dept_id = fields.Many2one('class.department', string='Department')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type_id = fields.Many2one('life.type', string='Life Type')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Item Sub Category')
    item_cat_id = fields.Many2one('item.category', string='Item Category')
    engine_year_id = fields.Many2one('engine.year', string='Year')

    accessories = fields.Boolean(string='Accessories')
    fabric = fields.Boolean(string='Fabric')

    @api.onchange('accessories')
    def onchange_accessories(self):
        if self.accessories == True:
            self.fabric = False
        elif self.accessories == False:
            self.fabric = True

    @api.onchange('fabric')
    def onchange_fabric(self):
        if self.fabric == True:
            self.accessories = False
        elif self.fabric == False:
            self.accessories = True

    @api.model
    def create(self, vals):
        sequence = self.env.ref('eng_product_format.product_sequence')
        vals['name'] = sequence.next_by_id()
        vals['name_seq'] = vals['name']

        todays_date = date.today()
        year = str(todays_date.year)
        crnt_year = year[2:]
        dept_record = self.env['class.department'].browse(vals['dept_id'])
        dept_code = str(dept_record.code)
        accessory_record = self.env['accessories.type'].browse(vals['accessories_type_id'])
        accessory_code = str(accessory_record.code)
        season_record = self.env['calender.season'].browse(vals['calender_season_id'])
        season_code = str(season_record.code)
        life_record = self.env['life.type'].browse(vals['life_type_id'])
        life_code = str(life_record.code)
        fabric_record = self.env['class.fabric'].browse(vals['class_fabric_id'])
        fabric_code = str(fabric_record.code)
        if vals['accessories'] == True:
            new_acc_name = ('A' + dept_code + accessory_code + '-' + season_code + crnt_year + '-' + vals['name'])
            print(new_acc_name)
            vals['name'] = new_acc_name
        elif vals['fabric'] == True:
            new_fab_name = (dept_code + life_code + fabric_code + '-' + season_code + crnt_year + '-' + vals['name'])
            print(new_fab_name)
            vals['name'] = new_fab_name
        res = super(ProductTemplateInherit, self).create(vals)
        return res

    def write(self, vals):
        # res = super(ProductTemplateInherit, self).write(vals)
        if 'calender_season_id' in vals or 'class_fabric_id' in vals or 'life_type_id' in vals or 'accessories_type_id' in vals or 'dept_id' in vals or 'accessories' in vals or 'fabric' in vals:
            todays_date = date.today()
            year = str(todays_date.year)
            crnt_year = year[2:]
            if 'dept_id' in vals:
                dept_record = self.env['class.department'].browse(vals['dept_id'])
                dept_code = str(dept_record.code)
            else:
                dept_code = str(self.dept_id.code)
            if 'accessories_type_id' in vals:
                accessory_record = self.env['accessories.type'].browse(vals['accessories_type_id'])
                accessory_code = str(accessory_record.code)
            else:
                accessory_code = str(self.accessories_type_id.code)
            if 'calender_season_id' in vals:
                season_record = self.env['calender.season'].browse(vals['calender_season_id'])
                season_code = str(season_record.code)
            else:
                season_code = str(self.calender_season_id.code)
            if 'life_type_id' in vals:
                life_record = self.env['life.type'].browse(vals['life_type_id'])
                life_code = str(life_record.code)
            else:
                life_code = str(self.life_type_id.code)
            if 'class_fabric_id' in vals:
                fabric_record = self.env['class.fabric'].browse(vals['class_fabric_id'])
                fabric_code = str(fabric_record.code)
            else:
                fabric_code = str(self.class_fabric_id.code)

            if 'accessories' in vals:
                acc_rec = vals['accessories']
            else:
                acc_rec = self.accessories
            if 'fabric' in vals:
                fab_rec = vals['fabric']
            else:
                fab_rec = self.fabric
            # if self.accessories == True:
            if acc_rec:
                new_acc_name = ('A' + dept_code + accessory_code + '-' + season_code + crnt_year + '-' + self.name_seq)
                print(new_acc_name)
                vals['name'] = new_acc_name
            # elif self.fabric == True:
            elif fab_rec:
                new_fab_name = (dept_code + life_code + fabric_code + '-' + season_code + crnt_year + '-' + self.name_seq)
                print(new_fab_name)
                vals['name'] = new_fab_name
        res = super(ProductTemplateInherit, self).write(vals)
        return res


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Grade')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    dept_id = fields.Many2one('class.department', string='Department')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type_id = fields.Many2one('life.type', string='Life Type')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Item Sub Category')
    item_cat_id = fields.Many2one('item.category', string='Item Category')
    engine_year_id = fields.Many2one('engine.year', string='Year')

    accessories = fields.Boolean(string='Accessories')
    fabric = fields.Boolean(string='Fabric')

    @api.onchange('accessories')
    def onchange_accessories(self):
        if self.accessories == True:
            self.fabric = False
        elif self.accessories == False:
            self.fabric = True

    @api.onchange('fabric')
    def onchange_fabric(self):
        if self.fabric == True:
            self.accessories = False
        elif self.fabric == False:
            self.accessories = True
