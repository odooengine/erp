# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class TempInh(models.Model):
    _inherit = 'product.template'

    show_on_hand_qty_status_button = fields.Float()


class ResUserInh(models.Model):
    _inherit = 'res.users'

    analytical_account_ids = fields.Many2many('account.analytic.account', string="Operating Units")


class StockMoveLineInh(models.Model):
    _inherit = 'stock.move.line'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")


class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")


class MrpWorkOrderInh(models.Model):
    _inherit = 'mrp.workorder'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")


class MultiPaymentInh(models.Model):
    _inherit = 'multi.payments'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    def button_verified(self):
        rec = super().button_verified()
        for line in self.tree_link_id:
            line.analytical_account_id = self.analytical_account_id.id
        return rec

class MultiPaymentTreeInh(models.Model):
    _inherit = 'multi.payments.tree'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")


class MrpProductionInh(models.Model):
    _inherit = 'mrp.production'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    @api.onchange('bom_id')
    def onchange_bom_unit(self):
        self.analytical_account_id = self.bom_id.analytical_account_id

    def action_confirm(self):
        rec = super().action_confirm()
        for line in self.move_raw_ids:
            line.analytical_account_id = self.analytical_account_id.id
        for order in self.workorder_ids:
            order.analytical_account_id = self.analytical_account_id.id
        return rec


class MrpBomInh(models.Model):
    _inherit = 'mrp.bom'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    def action_post(self):
        rec = super(AccountPaymentInh, self).action_post()
        if self.analytical_account_id:
            for line in self.move_id.invoice_line_ids:
                if not line.analytic_account_id:
                    line.analytic_account_id = self.analytical_account_id.id
        return rec


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    def action_post(self):
        rec = super(AccountMoveInh, self).action_post()
        if self.analytical_account_id:
            for line in self.invoice_line_ids:
                if not line.analytic_account_id:
                    line.analytic_account_id = self.analytical_account_id.id
            for res in self.line_ids:
                if not res.analytic_account_id:
                    res.analytic_account_id = self.analytical_account_id.id
        return rec


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    def action_confirm(self):
        rec = super(SaleOrderInh, self).action_confirm()
        if self.analytical_account_id:
            for line in self.order_line:
                if not line.analytical_account_id:
                    line.analytical_account_id = self.analytical_account_id.id
            for picking in self.picking_ids:
                if not picking.analytical_account_id:
                    picking.analytical_account_id = self.analytical_account_id.id
                for rec in picking.move_ids_without_package:
                    rec.analytical_account_id = self.analytical_account_id.id
                for res in picking.move_line_ids_without_package:
                    res.analytical_account_id = self.analytical_account_id.id
        return rec

    def _prepare_invoice(self):
        vals = super(SaleOrderInh, self)._prepare_invoice()
        if self.analytical_account_id:
            vals.update({
                'analytical_account_id': self.analytical_account_id.id,
            })
        return vals


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    def action_assign(self):
        record = super(StockPickingInh, self).action_assign()
        for rec in self.move_line_ids_without_package:
            rec.analytical_account_id = rec.move_id.analytical_account_id.id
        return record

    def button_validate(self):
        rec = super(StockPickingInh, self).button_validate()
        scraps = self.env['stock.scrap'].search([('picking_id', '=', self.id)])
        moves = (self.move_lines + scraps.move_id).stock_valuation_layer_ids
        for res in moves:
            for move in res.account_move_id.line_ids:
                move.analytic_account_id = self.analytical_account_id.id
        for line in self.move_line_ids_without_package:
            line.analytical_account_id = self.analytical_account_id.id
            line.move_id.analytical_account_id = self.analytical_account_id.id
        return rec


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")
    analytical_account_ids = fields.Many2many('account.analytic.account', compute='compute_account')

    @api.depends('analytical_account_id')
    def compute_account(self):
        self.analytical_account_ids = self.env.user.analytical_account_ids.ids

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrderInh, self)._prepare_picking()
        res['analytical_account_id'] = self.analytical_account_id.id
        return res

    def button_confirm(self):
        rec = super(PurchaseOrderInh, self).button_confirm()
        if self.analytical_account_id:
            for line in self.order_line:
                if not line.account_analytic_id:
                    line.account_analytic_id = self.analytical_account_id.id

            for picking in self.picking_ids:
                print(picking)
                for move in picking.move_ids_without_package:
                    move.analytical_account_id = self.analytical_account_id.id
                for move in picking.move_line_ids_without_package:
                    move.analytical_account_id = self.analytical_account_id.id
        # raise UserError('------------')
        return rec

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['analytical_account_id'] = self.analytical_account_id.id
        return invoice_vals


class PurchaseOrderlineInh(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_invoice_line(self, **optional_values):
        res = super(PurchaseOrderlineInh, self)._prepare_invoice_line(**optional_values)
        if self.analytical_account_id:
            res.update({
                'analytic_account_id': self.account_analytic_id,
            })
        return res


class SaleOrderlineInh(models.Model):
    _inherit = 'sale.order.line'

    analytical_account_id = fields.Many2one('account.analytic.account', string="Operating Unit")

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderlineInh, self)._prepare_invoice_line(**optional_values)
        if self.analytical_account_id:
            res.update({
                'analytic_account_id': self.analytical_account_id,
            })
        return res