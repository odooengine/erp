# -*- coding: utf-8 -*-


from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError, MissingError, AccessDenied


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('customer', 'Customer'),
                              ('vendor', 'Vendor'),
                              ], string='Partner Type')

    # customer_type = fields.Selection([('frenchise', 'Frenchise'),
    #                                  ('owned', 'Owned'),
    #                                  ], string='Customer Type')

    supplier_code = fields.Char(string = 'Supplier Code') 
    supplier_ntn = fields.Char(string = 'Supplier NTN#')

    customer_rank = fields.Integer(string = 'Customer Rank')
    supplier_rank = fields.Integer(string = 'Supplier Rank')

    @api.onchange('partner_type')
    def onchange_partner_type(self):
        if self.partner_type == 'customer':
            self.customer_rank = 1
            self.supplier_rank = 0
            self.supplier_code =False
            self.supplier_ntn =False
        elif self.partner_type == 'vendor':
            self.supplier_rank = 1
            self.customer_rank = 0
        else:
            self.supplier_rank = 1
            self.customer_rank = 1
            self.supplier_code =False
            self.supplier_ntn =False

          
    @api.constrains('supplier_code','supplier_ntn')
    def unique_supplier_code_ntn(self):
        for i in self:
            supplier_code_obj = self.env['res.partner'].search([('supplier_code' ,'=',i.supplier_code)])
            supplier_code_obj = supplier_code_obj.filtered(lambda s:s.supplier_code != False)
            
            
            supplier_ntn_obj = self.env['res.partner'].search([('supplier_ntn' ,'=',i.supplier_ntn)])
            supplier_ntn_obj = supplier_ntn_obj.filtered(lambda s:s.supplier_ntn != False)
            
            
            if (supplier_code_obj and len(supplier_code_obj) > 1 )  and  (supplier_ntn_obj and len(supplier_ntn_obj) > 1 ):
                raise ValidationError(_('Supplier Code and NTN# already exist!'))
            elif supplier_code_obj and len(supplier_code_obj) > 1:
                raise ValidationError(_('Supplier Code number already exists!'))
            elif supplier_ntn_obj and len(supplier_ntn_obj) > 1:
                raise ValidationError(_('Supplier NTN# already exists!')) 
#             if self.supplier_ntn:
#                 self.supplier_ntn = self.supplier_ntn.upper()
#                 return 
#             if self.supplier_code:
#                 self.supplier_code = self.supplier_code.upper()
                
     
    @api.model_create_multi
    def create(self, vals_list):
        res= super(PartnerInherit,self).create(vals_list)
        res.supplier_code = res.string_to_upper(res.supplier_code)
        res.supplier_ntn = res.string_to_upper(res.supplier_ntn)
        return res
    
    
    def write(self, vals):
        if vals.get('supplier_ntn') and vals.get('supplier_ntn') != False:
            vals['supplier_ntn'] = vals['supplier_ntn'].upper()
        if vals.get('supplier_code') and  vals.get('supplier_code') != False:
            vals['supplier_code'] = vals['supplier_code'].upper()    
        res= super(PartnerInherit,self).write(vals)
        return res
                   
    def string_to_upper(self, value):
        if value != False:
            return value.upper()
                      
