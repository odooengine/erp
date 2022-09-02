# -*- coding: utf-8 -*-
import ast

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    total_design = fields.Integer(string='Total Design / Items', compute='compute_total_design')
    total_pair = fields.Integer(string='Total Pairs / Qty', compute='compute_total_pair')

    packing_instruction = fields.Char(string='Packing Instructions')
    special_instruction = fields.Char(string='Special Instructions')

    sock_label = fields.Boolean(string='Sock Label')
    embossing_stamp = fields.Boolean(string='Embossing Stamp')
    sock_stamp = fields.Boolean(string='Sock Stamp')

    # def button_approved(self):
    #     rec = super(PurchaseOrderInherit, self).button_approved()
    #     self.fill_so_date()
    #     return rec
    #
    # def fill_so_date(self):
    #     print('Fill Called')
    #     record = self.env['sale.order'].search([('client_order_ref', '=', self.name)])
    #     record.commitment_date = self.date_planned
    # , ('company_id', '=', 2)

    def compute_total_design(self):
        tot_design = 0
        val = []
        for record in self.order_line:
            val.append({
                'product_id': record.product_id.product_tmpl_id.id,
            })
        list_org_updated = [str(item) for item in val]
        unique_set = set(list_org_updated)
        unique_list = [ast.literal_eval(item) for item in unique_set]
        for rec in unique_list:
            tot_design = tot_design + len(rec)
        self.total_design = tot_design

    def compute_total_pair(self):
        total = 0
        for record in self.order_line:
            total = total + record.product_qty
        self.total_pair = total


