# -*- coding: utf-8 -*-


from xml import etree
from lxml import etree
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


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    is_editable = fields.Boolean(string='Editable', default=False)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    product_group_type = fields.Selection([('filt_acc', 'Accessories'),
                                           ('filt_fab', 'Fabric'),
                                           ('filt_fin', 'Finish Goods'),
                                           ], string='Product Group Type')

    acc_seq = fields.Char(string='Acc Sequence')
    fab_seq = fields.Char(string='Fab Sequence')

    fin_men_seq = fields.Char(string='Fin Men Sequence')
    fin_women_seq = fields.Char(string='Fin Women Sequence')

    fin_boy_infan_seq = fields.Char(string='Fin Boy Infan Sequence')
    fin_boy_tod_seq = fields.Char(string='Fin Boy Tod Sequence')
    fin_boy_kid_seq = fields.Char(string='Fin Boy Kid Sequence')

    fin_girl_infan_seq = fields.Char(string='Fin Girl Infan Sequence')
    fin_girl_tod_seq = fields.Char(string='Fin Girl Tod Sequence')
    fin_girl_kid_seq = fields.Char(string='Fin Girl Kid Sequence')

    age_group_id = fields.Many2one('age.group', string='Age Group')
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
                                 ], string='Department')

    sub_dept = fields.Selection([('infant', 'Infant'),
                                 ('toddlers', 'Toddlers'),
                                 ('kids', 'Kids'),
                                 ('men', 'Men'),
                                 ('women', 'Women'),
                                 ], string='Sub Department')

    life_type_id = fields.Many2one('life.type', string='Life Type')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Item Sub Category')
    item_cat_id = fields.Many2one('item.category', string='Item Category')
    engine_year_id = fields.Many2one('engine.year', string='Year')
    # sub_dept_id = fields.Many2one('sub.department', string='Sub Department')

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    # company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)

    def _default_get_company(self):
        return self.env.company.id

    company_id = fields.Many2one('res.company', 'Company', default=_default_get_company)
    is_editable = fields.Boolean(string='Editable', related='company_id.is_editable')

    accessories = fields.Boolean(string='Accessories', default=False)
    fabric = fields.Boolean(string='Fabric', default=False)
    finish = fields.Boolean(string='Finish Goods', default=False)

    is_freeze = fields.Boolean(string='Freeze', default=False)

    # @api.constrains('seller_ids')
    # def _check_o2m_field(self):
    #     if len(self.seller_ids) > 0:
    #         raise ValidationError(_('Warning! You cannot add lines.'))

    @api.onchange('accessories')
    def onchange_accessories(self):
        if self.accessories == True:
            self.product_group_type = 'filt_acc'
            self.fabric = False
            self.finish = False

    @api.onchange('fabric')
    def onchange_fabric(self):
        if self.fabric == True:
            self.product_group_type = 'filt_fab'
            self.accessories = False
            self.finish = False

    @api.onchange('finish')
    def onchange_finish(self):
        if self.finish == True:
            self.product_group_type = 'filt_fin'
            self.accessories = False
            self.fabric = False

    @api.model
    def create(self, vals):
        vals['is_freeze'] = True
        if vals['accessories']:
            access_sequence = self.env.ref('eng_product_format.acc_sequence')
            vals['acc_seq'] = access_sequence.next_by_id()
        elif vals['fabric']:
            fabri_sequence = self.env.ref('eng_product_format.fab_sequence')
            vals['fab_seq'] = fabri_sequence.next_by_id()
        elif vals['finish']:
            if vals['dept_id'] == 'men':
                fini_man_sequence = self.env.ref('eng_product_format.fin_man_sequence')
                vals['fin_men_seq'] = fini_man_sequence.next_by_id()
            elif vals['dept_id'] == 'women':
                fini_wom_sequence = self.env.ref('eng_product_format.fin_woman_sequence')
                vals['fin_women_seq'] = fini_wom_sequence.next_by_id()
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'infant':
                fin_boy_inf_sequence = self.env.ref('eng_product_format.fin_boy_infan_sequence')
                vals['fin_boy_infan_seq'] = fin_boy_inf_sequence.next_by_id()
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'toddlers':
                fin_boy_tod_sequence = self.env.ref('eng_product_format.fin_boy_tod_sequence')
                vals['fin_boy_tod_seq'] = fin_boy_tod_sequence.next_by_id()
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'kids':
                fin_boy_kid_sequence = self.env.ref('eng_product_format.fin_boy_kid_sequence')
                vals['fin_boy_tod_seq'] = fin_boy_kid_sequence.next_by_id()
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'infant':
                fin_gir_inf_sequence = self.env.ref('eng_product_format.fin_gir_infan_sequence')
                vals['fin_girl_infan_seq'] = fin_gir_inf_sequence.next_by_id()
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'toddlers':
                fin_gir_tod_sequence = self.env.ref('eng_product_format.fin_gir_tod_sequence')
                vals['fin_girl_tod_seq'] = fin_gir_tod_sequence.next_by_id()
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'kids':
                fin_gir_kid_sequence = self.env.ref('eng_product_format.fin_gir_kid_sequence')
                vals['fin_girl_kid_seq'] = fin_gir_kid_sequence.next_by_id()

        # dept_record = self.env['class.department'].browse(vals['dept_id'])
        # dept_code = str(dept_record.code)
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
        # sub_dept_record = self.env['sub.department'].browse(vals['sub_dept_id'])
        # sub_dept_code = str(sub_dept_record.code)
        year_record = self.env['engine.year'].browse(vals['engine_year_id'])
        year_code = str(year_record.code)
        if vals['accessories'] == True:
            if vals['dept_id'] == 'boys':
                new_acc_name = ('A' + 'B' + accessory_code + '-' + season_code + year_code + '-' + vals['acc_seq'])
                vals['name'] = new_acc_name
            elif vals['dept_id'] == 'girls':
                new_acc_name = ('A' + 'G' + accessory_code + '-' + season_code + year_code + '-' + vals['acc_seq'])
                vals['name'] = new_acc_name
            elif vals['dept_id'] == 'men':
                new_acc_name = ('A' + 'M' + accessory_code + '-' + season_code + year_code + '-' + vals['acc_seq'])
                vals['name'] = new_acc_name
            elif vals['dept_id'] == 'women':
                new_acc_name = ('A' + 'W' + accessory_code + '-' + season_code + year_code + '-' + vals['acc_seq'])
                vals['name'] = new_acc_name
        elif vals['fabric'] == True:
            if vals['dept_id'] == 'boys':
                new_fab_name = ('B' + life_code + fabric_code + '-' + season_code + year_code + '-' + vals['fab_seq'])
                vals['name'] = new_fab_name
            elif vals['dept_id'] == 'girls':
                new_fab_name = ('G' + life_code + fabric_code + '-' + season_code + year_code + '-' + vals['fab_seq'])
                vals['name'] = new_fab_name
            elif vals['dept_id'] == 'men':
                new_fab_name = ('M' + life_code + fabric_code + '-' + season_code + year_code + '-' + vals['fab_seq'])
                vals['name'] = new_fab_name
            elif vals['dept_id'] == 'women':
                new_fab_name = ('W' + life_code + fabric_code + '-' + season_code + year_code + '-' + vals['fab_seq'])
                vals['name'] = new_fab_name
        elif vals['finish'] == True:
            if vals['dept_id'] == 'men' and vals['sub_dept'] == 'men':
                new_fin_man_name = ('M' + 'M' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '1' + vals['fin_men_seq'])
                vals['name'] = new_fin_man_name
            elif vals['dept_id'] == 'women' and vals['sub_dept'] == 'women':
                new_fin_man_name = ('W' + 'W' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '2' + vals['fin_women_seq'])
                vals['name'] = new_fin_man_name
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'infant':
                new_fin_boy_inf_name = ('I' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '3' + vals['fin_boy_infan_seq'])
                vals['name'] = new_fin_boy_inf_name
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'toddlers':
                new_fin_boy_tod_name = ('T' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '4' + vals['fin_boy_tod_seq'])
                vals['name'] = new_fin_boy_tod_name
            elif vals['dept_id'] == 'boys' and vals['sub_dept'] == 'kids':
                new_fin_boy_kid_name = ('K' + 'B' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '5' + vals['fin_boy_kid_seq'])
                vals['name'] = new_fin_boy_kid_name
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'infant':
                new_fin_gir_inf_name = ('I' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '6' + vals['fin_girl_infan_seq'])
                vals['name'] = new_fin_gir_inf_name
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'toddlers':
                new_fin_gir_tod_name = ('T' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '7' + vals['fin_girl_tod_seq'])
                vals['name'] = new_fin_gir_tod_name
            elif vals['dept_id'] == 'girls' and vals['sub_dept'] == 'kids':
                new_fin_gir_kid_name = ('K' + 'G' + fabric_code + sub_cat_code + '-' + life_code + year_code + season_code + '-' + '8' + vals['fin_girl_kid_seq'])
                vals['name'] = new_fin_gir_kid_name
        res = super(ProductTemplateInherit, self).create(vals)
        res.product_variant_id.product_group_type = res.product_group_type
        res.product_variant_id.age_group_id = res.age_group_id
        res.product_variant_id.accessories = res.accessories
        res.product_variant_id.fabric = res.fabric
        res.product_variant_id.finish = res.finish
        res.product_variant_id.calender_season_id = res.calender_season_id
        res.product_variant_id.class_fabric_id = res.class_fabric_id
        res.product_variant_id.line_item_id = res.line_item_id
        res.product_variant_id.product_group_id = res.product_group_id
        res.product_variant_id.size_range_id = res.size_range_id
        res.product_variant_id.accessories_type_id = res.accessories_type_id
        res.product_variant_id.product_gender = res.product_gender
        res.product_variant_id.dept_id = res.dept_id
        res.product_variant_id.sub_dept = res.sub_dept
        res.product_variant_id.life_type_id = res.life_type_id
        res.product_variant_id.item_sub_cat_id = res.item_sub_cat_id
        res.product_variant_id.item_cat_id = res.item_cat_id
        res.product_variant_id.engine_year_id = res.engine_year_id
        return res

    # def write(self, vals):
    #     # res = super(ProductTemplateInherit, self).write(vals)
    #     if 'calender_season_id' in vals or 'class_fabric_id' in vals or 'life_type_id' in vals or 'accessories_type_id' in vals or 'dept_id' in vals or 'accessories' in vals or 'fabric' in vals:
    #         todays_date = date.today()
    #         year = str(todays_date.year)
    #         crnt_year = year[2:]
    #         if 'dept_id' in vals:
    #             dept_record = self.env['class.department'].browse(vals['dept_id'])
    #             dept_code = str(dept_record.code)
    #         else:
    #             dept_code = str(self.dept_id.code)
    #         if 'accessories_type_id' in vals:
    #             accessory_record = self.env['accessories.type'].browse(vals['accessories_type_id'])
    #             accessory_code = str(accessory_record.code)
    #         else:
    #             accessory_code = str(self.accessories_type_id.code)
    #         if 'calender_season_id' in vals:
    #             season_record = self.env['calender.season'].browse(vals['calender_season_id'])
    #             season_code = str(season_record.code)
    #         else:
    #             season_code = str(self.calender_season_id.code)
    #         if 'life_type_id' in vals:
    #             life_record = self.env['life.type'].browse(vals['life_type_id'])
    #             life_code = str(life_record.code)
    #         else:
    #             life_code = str(self.life_type_id.code)
    #         if 'class_fabric_id' in vals:
    #             fabric_record = self.env['class.fabric'].browse(vals['class_fabric_id'])
    #             fabric_code = str(fabric_record.code)
    #         else:
    #             fabric_code = str(self.class_fabric_id.code)
    #
    #         if 'accessories' in vals:
    #             acc_rec = vals['accessories']
    #         else:
    #             acc_rec = self.accessories
    #         if 'fabric' in vals:
    #             fab_rec = vals['fabric']
    #         else:
    #             fab_rec = self.fabric
    #         # if self.accessories == True:
    #         if acc_rec:
    #             new_acc_name = ('A' + dept_code + accessory_code + '-' + season_code + crnt_year + '-' + self.name_seq)
    #             print(new_acc_name)
    #             vals['name'] = new_acc_name
    #         # elif self.fabric == True:
    #         elif fab_rec:
    #             new_fab_name = (dept_code + life_code + fabric_code + '-' + season_code + crnt_year + '-' + self.name_seq)
    #             print(new_fab_name)
    #             vals['name'] = new_fab_name
    #     res = super(ProductTemplateInherit, self).write(vals)
    #     return res

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     result = super(ProductTemplateInherit, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
    #     if not self.env.user.has_group('material_purchase_requisitions.group_requisition_user'):
    #         temp = etree.fromstring(result['arch'])
    #         temp.set('edit', '0')
    #         result['arch'] = etree.tostring(temp)
    #     return result


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    age_group_id = fields.Many2one('age.group', string='Age Group')
    calender_season_id = fields.Many2one('calender.season', string='Season')
    class_fabric_id = fields.Many2one('class.fabric', string='Fabric')
    line_item_id = fields.Many2one('line.item', string='Line Item')
    product_group_id = fields.Many2one('product.group', string='Grade')
    size_range_id = fields.Many2one('size.range', string='Width / GSM')
    accessories_type_id = fields.Many2one('accessories.type', string='Accessories Type')
    product_gender = fields.Selection([('male', 'Male'),
                                       ('female', 'Female'),
                                       ('unisex', 'Unisex'),
                                       ], string='Product Gender')
    dept_id = fields.Selection([('boys', 'Boys'),
                                ('girls', 'Girls'),
                                ('men', 'Men'),
                                ('women', 'Women'),
                                ], string='Department')

    sub_dept = fields.Selection([('infant', 'Infant'),
                                 ('toddlers', 'Toddlers'),
                                 ('kids', 'Kids'),
                                 ('men', 'Men'),
                                 ('women', 'Women'),
                                 ], string='Sub Department')

    product_group_type = fields.Selection([('filt_acc', 'Accessories'),
                                           ('filt_fab', 'Fabric'),
                                           ('filt_fin', 'Finish Goods'),
                                           ], string='Product Group Type')

    life_type_id = fields.Many2one('life.type', string='Life Type')
    item_sub_cat_id = fields.Many2one('item.sub.category', string='Item Sub Category')
    item_cat_id = fields.Many2one('item.category', string='Item Category')
    engine_year_id = fields.Many2one('engine.year', string='Year')

    accessories = fields.Boolean(string='Accessories')
    fabric = fields.Boolean(string='Fabric')
    finish = fields.Boolean(string='Finish Goods')

