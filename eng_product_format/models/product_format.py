# -*- coding: utf-8 -*-

from io import BytesIO
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _
from barcode import EAN13
from barcode.writer import ImageWriter
import base64
import binascii
from odoo.http import request


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


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Product Group')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    dept_id = fields.Many2one('class.department', string='Department')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type_id = fields.Many2one('life.type', string='Life Type')

    accessories = fields.Boolean(string='Accessories')
    fabric = fields.Boolean(string='Fabric')


    # # barco = fields.Binary(string='Bar Image', compute='compute_barcode')
    # barco = fields.Html(string='Bar Image', compute='compute_barcode')
    # # barco = fields.Many2one('ir.attachment', string='Bar Image', compute='compute_barcode')
    #
    # def create_barcode(self):
    #     # , writer = ImageWriter()
    #     if self.barcode:
    #         my_code = EAN13(self.barcode)
    #         img = my_code.make_image()
    #         temp = BytesIO()
    #         img.save(temp, format="PNG")
    #         my_code_br = base64.b64encode(temp.getvalue())
    #         return my_code_br
    #
    # def compute_barcode(self):
    #     # if self.barcode:
    #         # rv = BytesIO().write(rv)
    #         # my_code = EAN13(self.barcode, writer=ImageWriter())
    #         # print(my_code)
    #     system_parameter_url = request.env['ir.config_parameter'].get_param('web.base.url')
    #     system_parameter_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
    #     # self.barco = self.create_qr_code(system_parameter_url)
    #     self.barco = self.create_barcode(system_parameter_url)
    #         # my_code = EAN13(self.barcode)
    #         # my_code.save("new_code1")
    #         # self.barco = my_code
    #         # a = self.env['ir.attachment'].create({
    #         #     'name': 'new_code1',
    #         #     'type': 'binary',
    #         #     'datas': base64.encodebytes(my_code),
    #         #     'res_model': self._name,
    #         #     'res_id': self.id
    #         # })
    #         # self.barco = my_code
    #     # else:
    #     #     self.barco = ''
    #     # self.barco = my_code.save("new_code1")


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
            new_acc_name = ('A' + dept_code + accessory_code + '-' + season_code + crnt_year + '-' + '1000')
            print(new_acc_name)
            vals['name'] = new_acc_name
        elif vals['fabric'] == True:
            new_fab_name = (dept_code + life_code + fabric_code + '-' + season_code + crnt_year + '-' + '1000')
            print(new_fab_name)
            vals['name'] = new_fab_name
        res = super(ProductTemplateInherit, self).create(vals)
        return res

    def write(self, vals):
        res = super(ProductTemplateInherit, self).write(vals)
        if 'calender_season_id' in vals or 'class_fabric_id' in vals or 'life_type_id' in vals or 'accessories_type_id' in vals or 'dept_id' in vals:
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
            if self.accessories == True:
                new_acc_name = ('A' + dept_code + accessory_code + '-' + season_code + crnt_year + '-' + '1000')
                print(new_acc_name)
                vals['name'] = new_acc_name
            elif self.fabric == True:
                new_fab_name = (dept_code + life_code + fabric_code + '-' + season_code + crnt_year + '-' + '1000')
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
    product_group_id = fields.Many2one('product.group', string='Product Group')
    size_range_id = fields.Many2one('size.range', string='Size Range')
    dept_id = fields.Many2one('class.department', string='Department')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('men', 'Men'),
                                       ('women', 'Women'),
                                       ('boys', 'Boys'),
                                       ('girls', 'Girls'),
                                       ], string='Product Gender')

    life_type_id = fields.Many2one('life.type', string='Life Type')

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
