from odoo import models, fields, api


class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    descriptions = fields.Char(related='bom_line_id.descriptions')

    def _action_confirm(self, merge=False, merge_into=False):
        """ Confirms stock move or put it in waiting if it's linked to another move.
        :param: merge: According to this boolean, a newly confirmed move will be merged
        in another move of the same picking sharing its characteristics.
        """
        move_create_proc = self.env['stock.move']
        move_to_confirm = self.env['stock.move']
        move_waiting = self.env['stock.move']

        to_assign = {}
        for move in self:
            if move.state != 'draft':
                continue
            # if the move is preceeded, then it's waiting (if preceeding move is done, then action_assign has been called already and its state is already available)
            if move.move_orig_ids:
                move_waiting |= move
            else:
                if move.procure_method == 'make_to_order':
                    move_create_proc |= move
                else:
                    move_to_confirm |= move
            if move._should_be_assigned():
                key = (move.group_id.id, move.location_id.id, move.location_dest_id.id)
                if key not in to_assign:
                    to_assign[key] = self.env['stock.move']
                to_assign[key] |= move

        # create procurements for make to order moves
        procurement_requests = []
        for move in move_create_proc:
            values = move._prepare_procurement_values()
            origin = (move.group_id and move.group_id.name or (move.origin or move.picking_id.name or "/"))
            procurement_requests.append(self.env['procurement.group'].Procurement(
                move.product_id, move.product_uom_qty, move.product_uom,
                move.location_id, move.rule_id and move.rule_id.name or "/",
                origin, move.company_id, values))
        self.env['procurement.group'].run(procurement_requests, raise_user_error=not self.env.context.get('from_orderpoint'))
        move_to_confirm.write({'state': 'confirmed'})
        (move_waiting | move_create_proc).write({'state': 'waiting'})
        # assign picking in batch for all confirmed move that share the same details
        for moves in to_assign.values():
            moves._assign_picking()
        self._push_apply()
        self._check_company()
        moves = self
        # if merge:
        #     moves = self._merge_moves(merge_into=merge_into)
        # call `_action_assign` on every confirmed move which location_id bypasses the reservation
        moves.filtered(lambda move: not move.picking_id.immediate_transfer and move._should_bypass_reservation() and move.state == 'confirmed')._action_assign()
        return moves

#     def action_clear_lines_show_details(self):
#         pass


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    product_ref_id = fields.Many2one('product.product')
    product_tmpl_ref_id = fields.Many2one('product.template')
    department_id = fields.Many2one('hr.department')

    def action_send_merge(self):
        for rec in self:
            rec.state = 'merged'

    def action_reset_draft(self):
        self.write({
            'state': 'draft'
        })
#
#     mo_count = fields.Integer(default=0, compute='compute_mo')
#     show_create_mo = fields.Boolean()
#
#     def action_assign(self):
#         rec = super(StockPickingInh, self).action_assign()
#         for line in self.move_ids_without_package:
#             if  line.reserved_availability < line.product_uom_qty:
#                 bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'normal')])
#                 if bom:
#                     self.show_create_mo = True
#
#     def compute_mo(self):
#         count = self.env['mrp.production'].search_count([('origin', '=', self.name)])
#         self.mo_count = count
#
#     def action_view_mo(self):
#         return {
#             'name': 'MO',
#             'type': 'ir.actions.act_window',
#             'view_mode': 'tree,form',
#             'res_model': 'mrp.production',
#             'domain': [('origin', '=', self.name)],
#         }
#
#     def create_mo(self):
#         product_list = []
#         bom = self.env['mrp.bom'].search([])
#         for rec in bom:
#             product_list.append(rec.product_id.id)
#
#         for line in self.move_ids_without_package:
#             line_vals = []
#             if line.product_id.id in product_list and line.reserved_availability < line.product_uom_qty:
#                 bom_id = self.env['mrp.bom'].search([('product_id', '=', line.product_id.id)])
#                 print(bom_id)
#                 for bom_line in bom_id.bom_line_ids:
#                     line_vals.append((0, 0, {
#                         'product_id': bom_line.product_id.id,
#                         'name': bom_line.product_id.name,
#                         'location_id': line.location_id.id,
#                         'location_dest_id': line.location_dest_id.id,
#                         'product_uom_qty':  bom_line.product_qty,
#                         'product_uom': bom_line.product_uom_id.id,
#                     }))
#                     line_vals.append(line_vals)
#                 vals = {
#                     'picking_for_id': self.id,
#                     'product_id': line.product_id.id,
#                     'company_id': self.env.user.company_id.id,
#                     'date_planned_start': fields.Date.today(),
#                     'move_raw_ids': line_vals,
#                     'location_dest_id': self.location_id.id,
#                     'origin': self.name,
#                     'product_qty': line.product_uom_qty - line.reserved_availability,
#                     'product_uom_id': line.product_id.uom_id.id,
#                 }
#                 mrp = self.env['mrp.production'].create(vals)
#                 self.show_create_mo = False
