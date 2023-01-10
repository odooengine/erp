# -*- coding: utf-8 -*-

from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class MRPBOMInherit(models.Model):
    _inherit = 'mrp.bom'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Waiting For Approval'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_draft(self):
        self.write({
            'state': 'draft'
        })

    def button_confirm(self):
        self.write({
            'state': 'to_approve'
        })

    def button_approve(self):
        self.product_id.button_bom_cost()
        self.write({
            'state': 'done'
        })

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })


class MRPInherit(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        """ Finds UoM of changed product. """
        if not self.product_id:
            self.bom_id = False
        elif not self.bom_id or self.bom_id.product_tmpl_id != self.product_tmpl_id or (
                self.bom_id.product_id and self.bom_id.product_id != self.product_id):


            bom = self.env['mrp.bom']._bom_find(product=self.product_id, picking_type=self.picking_type_id,
                                                company_id=self.company_id.id, bom_type='normal')
            if bom.state == 'done':
                if bom:
                    self.bom_id = bom.id
                    print(self.bom_id.state)

                    self.product_qty = self.bom_id.product_qty
                    self.product_uom_id = self.bom_id.product_uom_id.id
                else:
                    self.bom_id = False
                    self.product_uom_id = self.product_id.uom_id.id
            else:
                self.bom_id = False
                self.product_uom_id = self.product_id.uom_id.id

    bom_ids = fields.Many2many(
        'mrp.bom',
        string='Boms',
        copy=False,
        compute='compute_bom_ids'
    )

    @api.depends('product_id')
    def compute_bom_ids(self):
        boms = self.env['mrp.bom'].search([('state', '=', 'done')])
        self.bom_ids = boms.ids