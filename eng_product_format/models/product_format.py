# -*- coding: utf-8 -*-


from xml import etree
from lxml import etree
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import date
from odoo import api, fields, models, _


class AgeGroup(models.Model):
    _name = 'age.group'
    _description = 'Sub Category'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class CalenderSeason(models.Model):
    _name = 'calender.season'
    _description = 'Calender Season'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class ClassFabric(models.Model):
    _name = 'class.fabric'
    _description = 'Class Fabric'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class LineItem(models.Model):
    _name = 'line.item'
    _description = 'Line item'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'Grade'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class SizeRange(models.Model):
    _name = 'size.range'
    _description = 'Size Range'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class Department(models.Model):
    _name = 'class.department'
    _description = 'Department'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)


# class SubDepartment(models.Model):
#     _name = 'sub.department'
#     _description = 'Sub Department'
#     _rec_name = 'name'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#
#     name = fields.Char(string='Name', tracking=True)
#     code = fields.Char(string='Code', tracking=True)


class AccessoriesType(models.Model):
    _name = 'accessories.type'
    _description = 'Accessories Type'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)

    def _default_get_company(self):
        return self.env.company.id

    company_id = fields.Many2one('res.company', 'Company', default=_default_get_company)

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)


class LifeType(models.Model):
    _name = 'life.type'
    _description = 'Life Type'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class ItemSubCategory(models.Model):
    _name = 'item.sub.category'
    _description = 'Sub Class'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class ItemCategory(models.Model):
    _name = 'item.category'
    _description = 'Class'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class EngineYear(models.Model):
    _name = 'engine.year'
    _description = 'Year'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char(string='Code', tracking=True)

    is_mk = fields.Boolean(string='MK', default=False)
    is_eng = fields.Boolean(string='Engine', default=False)


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    is_editable = fields.Boolean(string='Product Creation Fix', default=False)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    my_activity_date_deadline = fields.Date(string='My Activity Date Deadline')

    product_group_type = fields.Selection([('filt_acc', 'Accessories'),
                                           ('filt_fab', 'Fabric'),
                                           ('filt_fin', 'Finish Goods'),
                                           ('filt_sim', 'Simple Product'),
                                           ], string='Product Group Type')

    age_group_id = fields.Many2one('age.group', string='Sub Category')
    calender_season_id = fields.Many2one('calender.season', string='Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Grade')
    size_range_id = fields.Many2one('size.range', string='Width / GSM')
    # dept_id = fields.Many2one('class.department', string='Department')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('male', 'Male'),
                                       ('female', 'Female'),
                                       ('unisex', 'Unisex'),
                                       ], string='Product Gender')

    dept_id = fields.Selection([('boys', 'Boys'),
                                ('girls', 'Girls'),
                                ('men', 'Men'),
                                ('women', 'Women'),
                                ('unisex', 'Unisex'),
                                ], string='Department')

    sub_dept = fields.Selection([('infant', 'Infant'),
                                 ('toddlers', 'Toddlers'),
                                 ('kids', 'Kids'),
                                 ('boys', 'Boys'),
                                 ('girls', 'Girls'),
                                 ('men', 'Men'),
                                 ('women', 'Women'),
                                 ('unisex', 'Unisex'),
                                 ], string='Sub Department')

    life_type_id = fields.Many2one('life.type', string='Life Type')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Sub Class')
    item_cat_id = fields.Many2one('item.category', string='Class')
    engine_year_id = fields.Many2one('engine.year', string='Year')

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    def _default_get_company(self):
        if self.env.company.is_editable:
            return self.env.company.id

    company_id = fields.Many2one('res.company', 'Company', default=_default_get_company)
    is_editable = fields.Boolean(string='Editable', related='company_id.is_editable')

    accessories = fields.Boolean(string='Accessories', default=False)
    fabric = fields.Boolean(string='Fabric', default=False)
    finish = fields.Boolean(string='Finish Goods', default=False)
    simple = fields.Boolean(string='Simple Product', default=True)

    # is_mrp = fields.Boolean(string='MRP', default=False)
    # is_comp = fields.Boolean(string='Compo', default=False)

    is_freeze = fields.Boolean(string='Freeze', default=False)

    pre_seq = fields.Char(string='Pre Sequence')
    pos_seq = fields.Integer(string='Post Sequence', default=1)

    candela_code = fields.Char(string='Candela Code')

    # @api.onchange('accessories', 'fabric', 'finish')
    # def onchange_booleans(self):
    #     for rec in self:
    #         if rec.finish == True:
    #             rec.is_mrp = True
    #         elif not rec.finish == True:
    #             rec.is_mrp = False
    #         if rec.accessories == True or rec.fabric == True:
    #                 rec.is_comp = True
    #         elif not rec.accessories == True or rec.fabric == True:
    #             rec.is_comp = False
    #         rec.product_variant_id.onchange_booleans()

    @api.onchange('accessories')
    def onchange_accessories(self):
        if self.accessories == True:
            self.product_group_type = 'filt_acc'
            self.fabric = False
            self.finish = False
            self.simple = False

    @api.onchange('fabric')
    def onchange_fabric(self):
        if self.fabric == True:
            self.product_group_type = 'filt_fab'
            self.accessories = False
            self.finish = False
            self.simple = False

    @api.onchange('finish')
    def onchange_finish(self):
        if self.finish == True:
            self.product_group_type = 'filt_fin'
            self.accessories = False
            self.fabric = False
            self.simple = False

    @api.onchange('simple')
    def onchange_simple(self):
        if self.simple == True:
            self.product_group_type = 'filt_sim'
            self.accessories = False
            self.fabric = False
            self.finish = False

    def fill_cost(self):
        products = self.env['product.template'].search([])
        for product in products:
            if product.standard_price == 0:
                product.standard_price = 1

        # ('is_eng', '=', True)
        # for rec in self:
        #     if rec.standard_price == 0:
        #         rec.standard_price = 1

    @api.model
    def create(self, vals):
        vals['is_freeze'] = True
        if vals['standard_price'] == 0:
            vals['standard_price'] = 1
        if not vals['simple']:
            accessory_record = self.env['accessories.type'].browse(vals['accessories_type_id'])
            accessory_code = str(accessory_record.code)
            season_record = self.env['calender.season'].browse(vals['calender_season_id'])
            season_code = str(season_record.code)
            life_record = self.env['life.type'].browse(vals['life_type_id'])
            life_code = str(life_record.code)
            fabric_record = self.env['class.fabric'].browse(vals['class_fabric_id'])
            fabric_code = str(fabric_record.code)
            sub_cat_record = self.env['item.sub.category'].browse(vals['item_sub_cat_id'])
            sub_cat_code = str(sub_cat_record.code)
            year_record = self.env['engine.year'].browse(vals['engine_year_id'])
            year_code = str(year_record.code)

            if vals['accessories'] == True:
                if vals['dept_id'] == 'boys':
                    name = ('A' + 'B' + accessory_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'girls':
                    name = ('A' + 'G' + accessory_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'men':
                    name = ('A' + 'M' + accessory_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'women':
                    name = ('A' + 'W' + accessory_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'unisex':
                    name = ('A' + 'U' + accessory_code + '-' + season_code + year_code + '-')
            elif vals['fabric'] == True:
                if vals['dept_id'] == 'boys':
                    name = ('B' + life_code + fabric_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'girls':
                    name = ('G' + life_code + fabric_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'men':
                    name = ('M' + life_code + fabric_code + '-' + season_code + year_code + '-')
                elif vals['dept_id'] == 'women':
                    name = ('W' + life_code + fabric_code + '-' + season_code + year_code + '-')
            elif vals['finish'] == True:
                if vals['dept_id'] == 'men' and vals['sub_dept'] == 'men':
                    name = ('M' + 'M' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '1')
                elif vals['dept_id'] == 'women' and vals['sub_dept'] == 'women':
                    name = ('W' + 'W' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '2')
                elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'infant':
                    name = ('I' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '3')
                elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'toddlers':
                    name = ('T' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '4')
                elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'kids':
                    name = ('K' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '5')
                elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'infant':
                    name = ('I' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '6')
                elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'toddlers':
                    name = ('T' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '7')
                elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'kids':
                    name = ('K' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '8')
                elif vals['dept_id'] == 'unisex' and vals['sub_dept'] == 'unisex':
                    name = ('U' + 'U' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '9')
            vals['pre_seq'] = name

            product_record = self.env['product.template'].search([('pre_seq', '=', vals['pre_seq'])], order='id desc')
            if product_record:
                vals['pos_seq'] = product_record[0].pos_seq + 1
            if vals['pos_seq'] < 10:
                vals['name'] = name + '000' + str(vals['pos_seq'])
            elif 9 < vals['pos_seq'] < 100:
                vals['name'] = name + '00' + str(vals['pos_seq'])
            elif 99 < vals['pos_seq'] < 1000:
                vals['name'] = name + '0' + str(vals['pos_seq'])
            elif 999 < vals['pos_seq'] < 10000:
                vals['name'] = name + str(vals['pos_seq'])
            else:
                vals['name'] = name + str(vals['pos_seq'])
            res = super(ProductTemplateInherit, self).create(vals)
            return res
        else:
            res = super(ProductTemplateInherit, self).create(vals)
            return res

    def create_extra_variant(self):
        if self.finish:
            if self.product_variant_id.product_template_attribute_value_ids:
                create_variant = self.env['product.product'].create({
                    'product_tmpl_id': self.id,
                    'default_code': self.default_code,
                    'sale_ok': False,
                    'purchase_ok': False,
                    'categ_id': self.categ_id.id,
                    'barcode': self.barcode,
                    'type': self.type,
                    'uom_id': self.uom_id.id,
                    'uom_po_id': self.uom_po_id.id,
                    'standard_price': self.standard_price,
                    'lst_price': self.lst_price,
                    'taxes_id': self.taxes_id.ids,
                    'company_id': self.company_id.id,
                    'product_group_type': self.product_group_type,
                    'age_group_id': self.age_group_id.id,
                    'accessories': self.accessories,
                    'fabric': self.fabric,
                    'finish': self.finish,
                    'simple': self.simple,
                    'calender_season_id': self.calender_season_id.id,
                    'class_fabric_id': self.class_fabric_id.id,
                    'line_item_id': self.line_item_id.id,
                    'product_group_id': self.product_group_id.id,
                    'size_range_id': self.size_range_id.id,
                    'accessories_type_id': self.accessories_type_id.id,
                    'product_gender': self.product_gender,
                    'dept_id': self.dept_id,
                    'sub_dept': self.sub_dept,
                    'life_type_id': self.life_type_id.id,
                    'item_sub_cat_id': self.item_sub_cat_id.id,
                    'engine_year_id': self.engine_year_id.id,
                })

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     result = super(ProductTemplateInherit, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
    #     if not self.env.user.has_group('material_purchase_requisitions.group_requisition_user'):
    #         temp = etree.fromstring(result['arch'])
    #         temp.set('edit', '0')
    #         result['arch'] = etree.tostring(temp)
    #     return result

    accessories_type_ids = fields.Many2many('accessories.type', string='Accessories', compute='compute_accessories_type_ids')

    @api.depends('accessories_type_id')
    def compute_accessories_type_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                accessories = self.env['accessories.type'].search([('is_eng', '=', True)])
                self.accessories_type_ids = accessories.ids
            elif self.env.user.company_ids.id == 2:
                accessories = self.env['accessories.type'].search([('is_mk', '=', True)])
                self.accessories_type_ids = accessories.ids
        elif len(self.env.user.company_ids) > 1:
            accessories = self.env['accessories.type'].search([])
            self.accessories_type_ids = accessories.ids

    fabric_ids = fields.Many2many('class.fabric', string='Fabrics',compute='compute_fabric_ids')

    @api.depends('class_fabric_id')
    def compute_fabric_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                fabrics = self.env['class.fabric'].search([('is_eng', '=', True)])
                self.fabric_ids = fabrics.ids
            elif self.env.user.company_ids.id == 2:
                fabrics = self.env['class.fabric'].search([('is_mk', '=', True)])
                self.fabric_ids = fabrics.ids
        elif len(self.env.user.company_ids) > 1:
            fabrics = self.env['class.fabric'].search([])
            self.fabric_ids = fabrics.ids

    life_type_ids = fields.Many2many('life.type', string='Life Types', compute='compute_life_type_ids')

    @api.depends('life_type_id')
    def compute_life_type_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                life_types = self.env['life.type'].search([('is_eng', '=', True)])
                self.life_type_ids = life_types.ids
            elif self.env.user.company_ids.id == 2:
                life_types = self.env['life.type'].search([('is_mk', '=', True)])
                self.life_type_ids = life_types.ids
        elif len(self.env.user.company_ids) > 1:
            life_types = self.env['life.type'].search([])
            self.life_type_ids = life_types.ids

    engine_year_ids = fields.Many2many('engine.year', string='Years', compute='compute_engine_year_ids')

    @api.depends('engine_year_id')
    def compute_engine_year_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                engine_years = self.env['engine.year'].search([('is_eng', '=', True)])
                self.engine_year_ids = engine_years.ids
            elif self.env.user.company_ids.id == 2:
                engine_years = self.env['engine.year'].search([('is_mk', '=', True)])
                self.engine_year_ids = engine_years.ids
        elif len(self.env.user.company_ids) > 1:
            engine_years = self.env['engine.year'].search([])
            self.engine_year_ids = engine_years.ids

    calender_season_ids = fields.Many2many('calender.season', string='Seasons', compute='compute_calender_season_ids')

    @api.depends('calender_season_id')
    def compute_calender_season_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                seasons = self.env['calender.season'].search([('is_eng', '=', True)])
                self.calender_season_ids = seasons.ids
            elif self.env.user.company_ids.id == 2:
                seasons = self.env['calender.season'].search([('is_mk', '=', True)])
                self.calender_season_ids = seasons.ids
        elif len(self.env.user.company_ids) > 1:
            seasons = self.env['calender.season'].search([])
            self.calender_season_ids = seasons.ids

    sub_category_ids = fields.Many2many('item.sub.category', string='Sub Classes', compute='compute_sub_category_ids')

    @api.depends('item_sub_cat_id')
    def compute_sub_category_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                sub_categories = self.env['item.sub.category'].search([('is_eng', '=', True)])
                self.sub_category_ids = sub_categories.ids
            elif self.env.user.company_ids.id == 2:
                sub_categories = self.env['item.sub.category'].search([('is_mk', '=', True)])
                self.sub_category_ids = sub_categories.ids
        elif len(self.env.user.company_ids) > 1:
            sub_categories = self.env['item.sub.category'].search([])
            self.sub_category_ids = sub_categories.ids

    item_category_ids = fields.Many2many('item.category', string='Classes', compute='compute_item_category_ids')

    @api.depends('item_cat_id')
    def compute_item_category_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                item_categories = self.env['item.category'].search([('is_eng', '=', True)])
                self.item_category_ids = item_categories.ids
            elif self.env.user.company_ids.id == 2:
                item_categories = self.env['item.category'].search([('is_mk', '=', True)])
                self.item_category_ids = item_categories.ids
        elif len(self.env.user.company_ids) > 1:
            item_categories = self.env['item.category'].search([])
            self.item_category_ids = item_categories.ids

    age_group_ids = fields.Many2many('age.group', string='Sub Categories', compute='compute_age_group_ids')

    @api.depends('age_group_id')
    def compute_age_group_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                age_groups = self.env['age.group'].search([('is_eng', '=', True)])
                self.age_group_ids = age_groups.ids
            elif self.env.user.company_ids.id == 2:
                age_groups = self.env['age.group'].search([('is_mk', '=', True)])
                self.age_group_ids = age_groups.ids
        elif len(self.env.user.company_ids) > 1:
            age_groups = self.env['age.group'].search([])
            self.age_group_ids = age_groups.ids

    size_range_ids = fields.Many2many('size.range', string='Widthes / GSMes', compute='compute_size_range_ids')

    @api.depends('size_range_id')
    def compute_size_range_ids(self):
        if len(self.env.user.company_ids) < 2:
            if self.env.user.company_ids.id == 1:
                size_ranges = self.env['size.range'].search([('is_eng', '=', True)])
                self.size_range_ids = size_ranges.ids
            elif self.env.user.company_ids.id == 2:
                size_ranges = self.env['size.range'].search([('is_mk', '=', True)])
                self.size_range_ids = size_ranges.ids
        elif len(self.env.user.company_ids) > 1:
            size_ranges = self.env['size.range'].search([])
            self.size_range_ids = size_ranges.ids


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    age_group_id = fields.Many2one('age.group', string='Sub Category', related='product_tmpl_id.age_group_id')
    calender_season_id = fields.Many2one('calender.season', string='Season', related='product_tmpl_id.calender_season_id')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric', related='product_tmpl_id.class_fabric_id')
    line_item_id = fields.Many2one('line.item', string='Line Item', related='product_tmpl_id.line_item_id')
    product_group_id = fields.Many2one('product.group', string='Grade', related='product_tmpl_id.product_group_id')
    size_range_id = fields.Many2one('size.range', string='Width / GSM', related='product_tmpl_id.size_range_id')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type', related='product_tmpl_id.accessories_type_id')
    product_gender = fields.Selection([('male', 'Male'),
                                       ('female', 'Female'),
                                       ('unisex', 'Unisex'),
                                       ], string='Product Gender', related='product_tmpl_id.product_gender')
    dept_id = fields.Selection([('boys', 'Boys'),
                                ('girls', 'Girls'),
                                ('men', 'Men'),
                                ('women', 'Women'),
                                ('unisex', 'Unisex'),
                                ], string='Department', related='product_tmpl_id.dept_id')

    sub_dept = fields.Selection([('infant', 'Infant'),
                                 ('toddlers', 'Toddlers'),
                                 ('kids', 'Kids'),
                                 ('boys', 'Boys'),
                                 ('girls', 'Girls'),
                                 ('men', 'Men'),
                                 ('women', 'Women'),
                                 ('unisex', 'Unisex'),
                                 ], string='Sub Department', related='product_tmpl_id.sub_dept')

    product_group_type = fields.Selection([('filt_acc', 'Accessories'),
                                           ('filt_fab', 'Fabric'),
                                           ('filt_fin', 'Finish Goods'),
                                           ('filt_sim', 'Simple Product'),
                                           ], string='Product Group Type', related='product_tmpl_id.product_group_type')

    life_type_id = fields.Many2one('life.type', string='Life Type', related='product_tmpl_id.life_type_id')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Sub Class', related='product_tmpl_id.item_sub_cat_id')
    item_cat_id = fields.Many2one('item.category', string='Class', related='product_tmpl_id.item_cat_id')
    engine_year_id = fields.Many2one('engine.year', string='Year', related='product_tmpl_id.engine_year_id')

    accessories = fields.Boolean(string='Accessories', related='product_tmpl_id.accessories')
    fabric = fields.Boolean(string='Fabric', related='product_tmpl_id.fabric')
    finish = fields.Boolean(string='Finish Goods', related='product_tmpl_id.finish')
    simple = fields.Boolean(string='Simple Product', related='product_tmpl_id.finish')

    # is_mrp = fields.Boolean(string='MRP', related='product_tmpl_id.is_mrp')
    # is_comp = fields.Boolean(string='Compo', related='product_tmpl_id.is_comp')

    candela_code = fields.Char(string='Candela Code', related='product_tmpl_id.candela_code')

    # def onchange_booleans(self):
    #     for rec in self:
    #         if rec.finish == True:
    #             rec.is_mrp = True
    #         elif not rec.finish == True:
    #             rec.is_mrp = False
    #         if rec.accessories == True or rec.fabric == True:
    #                 rec.is_comp = True
    #         elif not rec.accessories == True or rec.fabric == True:
    #             rec.is_comp = False


class BomLineInherit(models.Model):
    _inherit = 'mrp.bom.line'

    product_qty = fields.Float(
        'Quantity', default=1.0,
        digits=(12, 3),
        # digits='Product Unit of Measure',
        required=True)


class PoLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    product_qty = fields.Float(string='Quantity',
                               digits=(12, 3),
                               # digits='Product Unit of Measure',
                               required=True)


class PickingLineInherit(models.Model):
    _inherit = 'stock.move'

    product_uom_qty = fields.Float(
        'Demand',
        digits=(12, 3),
        # digits='Product Unit of Measure',
        default=0.0, required=True, states={'done': [('readonly', True)]},
        help="This is the quantity of products from an inventory "
             "point of view. For moves in the state 'done', this is the "
             "quantity of products that were actually moved. For other "
             "moves, this is the quantity of product that is planned to "
             "be moved. Lowering this quantity does not generate a "
             "backorder. Changing this quantity on assigned moves affects "
             "the product reservation, and should be done with care.")

