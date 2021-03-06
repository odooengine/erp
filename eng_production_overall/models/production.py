# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class WorkCenterEmbellishment(models.Model):
    _inherit = 'mrp.workcenter'

    wk_embellish = fields.Boolean(string='Embellishment', default=False)
    src_location_id = fields.Many2one('stock.location', string='Source location')
    dest_location_id = fields.Many2one('stock.location', string='Destination location')
    partner_id = fields.Many2one('res.partner', string='Partner')


class ProducedQtyLine(models.Model):
    _name = 'produced.qty.line'

    mrp_id = fields.Many2one('mrp.production')
    workcenter_id = fields.Many2one('mrp.workcenter')
    name = fields.Char('Operation')
    qty = fields.Float('Produced Quantity')
    start_date = fields.Datetime('Start Date')
    paused_date = fields.Datetime('End Date')


class ReasonLine(models.Model):
    _name = 'reason.line'

    mrp_id = fields.Many2one('mrp.production')
    workcenter_id = fields.Many2one('mrp.workcenter')
    name = fields.Char('Operation')
    qty = fields.Float('Produced Quantity')
    start_date = fields.Datetime('Start Date')
    paused_date = fields.Datetime('End Date')
    reason = fields.Char('Reason')


class MrpOrderInh(models.Model):
    _inherit = 'mrp.workorder'

    start_date_custom = fields.Datetime('Date Start')

    def button_finish(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Done Quantity',
            'view_id': self.env.ref('eng_production_overall.view_done_wizard_form', False).id,
            'target': 'new',
            'res_model': 'done.qty.wizard',
            'view_mode': 'form',
        }

    def button_start(self):
        pre_order = self.env['mrp.workorder'].search([('id', '=', self.id-1), ('production_id', '=', self.production_id.id)])
        if pre_order:
            if pre_order.state != 'done':
                raise UserError('This workorder is waiting for another operation to get done.')
        if self.workcenter_id.wk_embellish:
            self.action_create_internal_transfer(pre_order)
        record = super(MrpOrderInh, self).button_start()
        self.start_date_custom = datetime.today()

    def action_create_internal_transfer(self, pre_order):
        qty = 0
        for line in self.production_id.produced_lines:
            if line.workcenter_id.id == pre_order.workcenter_id.id:
                qty = qty + line.qty
        picking_delivery = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

        vals = {
            'location_id': self.workcenter_id.src_location_id.id,
            'location_dest_id': self.workcenter_id.dest_location_id.id,
            'partner_id': self.workcenter_id.partner_id.id,
            # 'product_sub_id': self.product_subcontract_id.id,
            'picking_type_id': picking_delivery.id,
            'origin': self.production_id.name,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.production_id.bom_id.bom_line_ids:

            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'product_uom': line.product_id.uom_id.id,
                'location_id': self.workcenter_id.src_location_id.id,
                'location_dest_id': self.workcenter_id.dest_location_id.id,
                'product_uom_qty': qty * line.product_qty,
                # 'reserved_availability': qty * line.product_qty,
                # 'quantity_done': qty * line.product_qty,
            }
            stock_move = self.env['stock.move'].create(lines)
            # moves = {
            #     'move_id': stock_move.id,
            #     'product_id': line.product_id.id,
            #     'location_id': self.workcenter_id.src_location_id.id,
            #     'location_dest_id': self.workcenter_id.dest_location_id.id,
            #     'product_uom_id': line.product_id.uom_id.id,
            #     'product_uom_qty': qty * line.product_qty,
            #     # 'qty_done': qty * line.product_qty,
            # }
            # stock_move_line_id = self.env['stock.move.line'].create(moves)
        # picking.action_confirm()
        # picking.action_assign()
        # picking.button_validate()

    def button_pending(self):
        record = super(MrpOrderInh, self).button_pending()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Produced Quantity',
            'view_id': self.env.ref('eng_production_overall.view_produced_wizard_form', False).id,
            'target': 'new',
            'res_model': 'produced.qty.wizard',
            'view_mode': 'form',
        }


class MrpInh(models.Model):
    _inherit = 'mrp.production'

    produced_lines = fields.One2many('produced.qty.line', 'mrp_id')
    reason_lines = fields.One2many('reason.line', 'mrp_id')
    transfer_count = fields.Integer(compute='compute_transfers')

    def compute_transfers(self):
        count = self.env['stock.picking'].search_count([('origin', '=', self.name)])
        print(count)
        self.transfer_count = count

    def action_view_transfers(self):
        return {
            'name': 'Transfers',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)], }

    def _create_notification(self):
        for res in self:
            act_type_xmlid = 'mail.mail_activity_data_todo'
            summary = 'MO Done'
            note = 'Manufacturing order no:' + res.name + ' Created.'
            if act_type_xmlid:
                activity_type = self.sudo().env.ref(act_type_xmlid)
            model_id = self.env['ir.model']._get(res._name).id
            users = self.env['res.users'].search([])
            for rec in users:
                if rec.has_group('mrp.group_mrp_manager'):
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': datetime.today(),
                        'res_model_id': model_id,
                        'res_id': res.id,
                        # 'user_id': self.sale_id.user_id.id,
                        'user_id': rec.id ,
                    }
                    activities = self.env['mail.activity'].create(create_vals)

    def button_mark_done(self):
        # self._create_notification()
        for rec in self.check_ids:
            if rec.quality_state != 'pass':
                raise UserError('Quality Checks Are not Passed.')
        return super(MrpInh, self).button_mark_done()