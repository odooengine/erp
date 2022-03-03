# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class PurchaseOrderInh(models.Model):
#     _inherit = 'stock.picking'
#
#     purchase_ids = fields.Many2many('purchase.order')
from odoo.exceptions import UserError


class MrpProductionInh(models.Model):
    _inherit = 'stock.picking'

    ref = fields.Char('Merged From')
    # purchase_ids = fields.Many2many('purchase.order')

    def action_open_wizard(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['stock.picking'].browse(selected_ids)
        # location_list = []
        for rec in selected_records:
            for res in selected_records:
                if rec.location_dest_id.id != res.location_dest_id.id or rec.location_id.id != res.location_id.id:
                    raise UserError('Locations Are Not Same.')
        line_vals = []
        names = []
        for record in selected_records:
            names.append(record.name)
            # if record.state == ''
            for line in record.move_ids_without_package:
                if not any(d['product_id'] == line.product_id.id for d in line_vals):
                    line_data = {
                        # 'picking_id': picking.id,
                        'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_uom': line.product_id.uom_id.id,
                        'location_id': line.location_id.id,
                        'location_dest_id': line.location_dest_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'quantity_done': line.quantity_done,
                    }
                    line_vals.append(line_data)
                else:
                    for rec_l in line_vals:
                        if rec_l['product_id'] == line.product_id.id:
                            rec_l['product_uom_qty'] = rec_l['product_uom_qty'] + line.product_uom_qty
                            rec_l['quantity_done'] = rec_l['quantity_done'] + line.quantity_done
            record.state = 'merged'
        my_string = ','.join(names)
        final_line_vals = []
        for final_line in line_vals:
            final_line_vals.append((0, 0, final_line))
        vals = {
            'company_id': self.env.user.company_id.id,
            # 'request_date': fields.Date.today(),
            'picking_type_id': selected_records[0].picking_type_id.id,
            'location_id': selected_records[0].location_id.id,
            'location_dest_id': selected_records[0].location_dest_id.id,
            'move_ids_without_package': final_line_vals,
            'ref': my_string,
        }
        move = self.env['stock.picking'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': move.id,
            'view_mode': 'form',
            'views': [(False, "form")],
        }
        # return {
        #     'name': 'Transfer',
        #     'res_model': 'stock.picking',
        #     'views': [[False, "form"]],
        #     'type': 'ir.actions.act_window',
        #     'context': {'default_move_ids_without_package': final_line_vals,
        #                 'default_picking_type_id': selected_records[0].picking_type_id.id,
        #                 'default_location_dest_id': selected_records[0].location_dest_id.id,
        #                 'default_location_id': selected_records[0].location_id.id,
        #                 'default_partner_id': selected_records[0].partner_id.id,
        #                 'default_ref': my_string,
        #                 # 'default_request_date': fields.Date.today(),
        #                 'default_company_id': self.env.user.company_id.id}
        # }

    # def action_open_wizard(self):
    #     selected_ids = self.env.context.get('active_ids', [])
    #     selected_records = self.env['stock.picking'].browse(selected_ids)
    #     purchase_list = []
    #     for rec in selected_records:
    #         purchase_list.append(rec.id)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Merge Purchase Order',
    #         'view_id': self.env.ref('merge_purchase_orders.view_merge_purchase_wizard_form', False).id,
    #         'context': {'default_purchase_id': purchase_list},
    #         'target': 'new',
    #         'res_model': 'purchase.merge.wizard',
    #         'view_mode': 'form',
    #     }

