# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class MrpBomLineInh(models.Model):
    _inherit = 'mrp.bom.line'

    class_fabric_id = fields.Many2one('class.fabric', related='product_id.class_fabric_id')
    accessories_type_id = fields.Many2one('accessories.type', related='product_id.accessories_type_id')
    descriptions = fields.Char()
    components_ids = fields.Many2many('product.product')

    @api.onchange('product_id')
    def _onchange_product(self):
        for rec in self:
            rec.descriptions = rec.product_id.name

    @api.depends('product_id')
    def compute_components(self):
        products = self.env['product.product'].search([('is_comp', '=', True)])
        self.components_ids = products.ids

    # components_ids = fields.Many2many('product.product', compute='compute_components')

    # @api.depends('product_id')
    # def compute_components(self):
    #     products = self.env['product.product'].search([])
    #     products_list = []
    #     for product in products:
    #         for route in product.route_ids:
    #             if route.name == 'Components':
    #                 products_list.append(product.id)
    #     self.components_ids = products_list


class MrpBomInh(models.Model):
    _inherit = 'mrp.bom'

    product_tmpl_ids = fields.Many2many('product.template')

    @api.depends('product_tmpl_id')
    def compute_products(self):
        products = self.env['product.template'].search([('is_mrp', '=', True)])
        self.product_tmpl_ids = products.ids

# class MrpBomInh(models.Model):
#     _inherit = 'mrp.bom'
#
#     product_tmpl_ids = fields.Many2many('product.template', compute='compute_products')
#
#     @api.depends('product_tmpl_id')
#     def compute_products(self):
#         products = self.env['product.template'].search([])
#         products_list = []
#         for product in products:
#             for route in product.route_ids:
#                 if route.name == 'Manufacture':
#                     products_list.append(product.id)
#         self.product_tmpl_ids = products_list

        # products = self.env['product.product'].search([('product_tmpl_id', '=', self.product_tmpl_id.id)])
        # empty_id = ''
        # for rec in products:
        #     if not rec.product_template_attribute_value_ids:
        #         empty_id = rec.id
        # self.product_id = empty_id


class WorkCenterEmbellishment(models.Model):
    _inherit = 'mrp.workcenter'

    wk_embellish = fields.Boolean(string='Embellishment', default=False, copy=False)
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
    reasons = fields.Char(ondelete='cascade')
    # reason = fields.Selection([
    #     ('wrong', 'Wrong Cutting'),
    #     ('burn', 'Burn'),
    #     ('hole', 'Hole'),
    #     ('shortage', 'Shortage of material during welding'),
    #     ('excess', 'Excess of material during welding'),
    # ], string='Reason', default='', ondelete='cascade')


class MrpOrderInh(models.Model):
    _inherit = 'mrp.workorder'

    start_date_custom = fields.Datetime('Date Start')
    work_order_no = fields.Char('Work Order No')

    life_type = fields.Char()
    depart = fields.Char('Department')
    fabric = fields.Char()
    qty_producing_1 = fields.Float(compute='_compute_qty_producing')
    qty_producing_2 = fields.Float('Qty Producing')

    def _compute_qty_producing(self):
        for rec in self:
            rec.qty_producing_1 = rec.qty_production
            rec.qty_producing_2 = rec.qty_production

    def button_finish(self):
        # if self._context['active_model'] != 'stock.picking':
        #     transfers = self.env['stock.picking'].search([('origin', '=', self.production_id.name)])
        #     if any(line.state != 'done' for line in transfers):
        #         print(self._context)
        #         raise UserError('Please Confirm all Transfers')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Done Quantity',
            'view_id': self.env.ref('eng_production_overall.view_done_wizard_form', False).id,
            'target': 'new',
            'res_model': 'done.qty.wizard',
            'view_mode': 'form',
        }

    def button_start(self):
        flag = False
        reqs = self.env['material.purchase.requisition'].search([('mrp_id', '=', self.production_id.id)])
        print(reqs)
        for req in reqs:
            if req.state != 'receive':
                flag = True
            if flag:
                raise UserError(_('Receive the Requisition'))
            else:
                for rec in self:
                    pre_order = self.env['mrp.workorder'].search([('id', '=', rec.id-1), ('production_id', '=', rec.production_id.id)])
                    # if pre_order:
                    #     if pre_order.state != 'done':
                    #         raise UserError('This workorder is waiting for another operation to get done.')
                    if rec.workcenter_id.wk_embellish:
                        if not rec.production_id.is_transfer_created:
                            rec.action_create_internal_transfer(pre_order)
                            rec.action_create_internal_transfer_second(pre_order)
                    record = super(MrpOrderInh, rec).button_start()
                    rec.start_date_custom = datetime.today()


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

    def action_create_internal_transfer_second(self, pre_order):
        qty = 0
        for line in self.production_id.produced_lines:
            if line.workcenter_id.id == pre_order.workcenter_id.id:
                qty = qty + line.qty
        picking_delivery = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

        vals = {
            'location_id': self.workcenter_id.dest_location_id.id,
            'location_dest_id': self.workcenter_id.src_location_id.id,
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
                'location_id': self.workcenter_id.dest_location_id.id,
                'location_dest_id': self.workcenter_id.src_location_id.id,
                'product_uom_qty': qty * line.product_qty,
                # 'reserved_availability': qty * line.product_qty,
                # 'quantity_done': qty * line.product_qty,
            }
            stock_move = self.env['stock.move'].create(lines)
        self.production_id.is_transfer_created = True
        picking.action_confirm()
        if picking.state == 'assigned':
            picking.do_unreserve()

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


# class StockInventoryLineInh(models.Model):
#     _inherit = 'stock.inventory.line'
#
#     ref = fields.Char('Origin')

class PolineDescript(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        prod_des = ''
        if self.name != False:
            prod_des = self.name
        res = super(PolineDescript, self)._onchange_quantity()
        self.name = prod_des
        return res


class StockInventoryInh(models.Model):
    _inherit = 'stock.inventory'

    ref = fields.Char('Origin')


class RequisitionInh(models.Model):
    _inherit = 'material.purchase.requisition'

    ref = fields.Char('Origin')


class MrpInh(models.Model):
    _inherit = 'mrp.production'

    produced_lines = fields.One2many('produced.qty.line', 'mrp_id')
    reason_lines = fields.One2many('reason.line', 'mrp_id')
    transfer_count = fields.Integer(compute='compute_transfers')
    is_req_created = fields.Boolean(copy=False)
    req_count = fields.Integer(string="Requisitions", compute='compute_req_count')
    # adjust_count = fields.Integer(string="Adjustment", compute='compute_adjust_count')
    work_order_no = fields.Char('Work Order No')

    # product_ids = fields.Many2many('product.product', compute='compute_products')
    is_transfer_created = fields.Boolean(copy=False)
    product_templ = fields.Char()
    life_type = fields.Char()
    depart = fields.Char('Department')
    fabric = fields.Char()
    # is_adj_created = fields.Boolean()

    # def compute_adjust_count(self):
    #     for rec in self:
    #         count = self.env['stock.inventory'].search_count([('ref', '=', rec.name)])
    #         rec.adjust_count = count

    # @api.depends('product_id')
    # def compute_products(self):
    #     products = self.env['product.product'].search([('is_mrp', '=', True)])
    #     self.product_ids = products.ids

    # @api.depends('product_id')
    # def compute_products(self):
    #     products = self.env['product.product'].search([])
    #     products_list = []
    #     for product in products:
    #         for route in product.route_ids:
    #             if route.name == 'Manufacture':
    #                 products_list.append(product.id)
    #     self.product_ids = products_list

    @api.onchange('product_id')
    def onchange_product_id_inh(self):
        for rec in self:
            rec.product_templ = rec.product_tmpl_id.name
            rec.life_type = rec.product_id.life_type_id.name
            rec.depart = rec.product_id.dept_id
            rec.fabric = rec.product_id.class_fabric_id.name
            for line in self.workorder_ids:
                line.life_type = rec.product_id.life_type_id.name
                line.depart = rec.product_id.dept_id
                line.fabric = rec.product_id.class_fabric_id.name

    def compute_req_count(self):
        for rec in self:
            count = self.env['material.purchase.requisition'].search_count([('ref', '=', rec.name)])
            rec.req_count = count

    # def action_show_adjustment(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Variants Adjustments',
    #         'view_id': self.env.ref('stock.view_inventory_tree', False).id,
    #         'target': 'current',
    #         'domain': [('ref', '=', self.name)],
    #         'res_model': 'stock.inventory',
    #         'views': [[False, 'tree'], [False, 'form']],
    #     }

    def action_show_requisitions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requisitions',
            'view_id': self.env.ref('material_purchase_requisitions.material_purchase_requisition_tree_view', False).id,
            'target': 'current',
            'domain': [('ref', '=', self.name)],
            'res_model': 'material.purchase.requisition',
            'views': [[False, 'tree'], [False, 'form']],
        }

    def compute_transfers(self):
        count = self.env['stock.picking'].search_count([('origin', '=', self.name)])
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
        # if 'active_model' not in self._context:
        for rec in self.check_ids:
            if rec.quality_state != 'pass':
                raise UserError('Quality Checks Are not Passed.')
            # adjustment = self.env['stock.inventory'].search([('ref', '=', self.name)], limit=1)
            # if adjustment:
            #     if adjustment.state == 'done':
            #         return super(MrpInh, self).button_mark_done()
            #     else:
            #         raise ValidationError('Please Add Adjustment of All Variants.')
            # else:
            #     raise ValidationError('Please Add Adjustment of All Variants.')
        # else:
        # self.action_general_entry()
        return super(MrpInh, self).button_mark_done()

    # def create_adjustment(self):
    #     if not self.is_adj_created:
    #         variants = self.env['product.product'].search([('product_tmpl_id', '=', self.product_tmpl_id.id)])
    #         create_vals = {
    #             'name': 'Manufacturing Adjustment',
    #             'location_ids': [self.location_dest_id.id],
    #             'product_ids': variants.ids,
    #             'company_id': self.env.company.id,
    #             'ref': self.name,
    #             'date': datetime.today(),
    #         }
    #         adju = self.env['stock.inventory'].create(create_vals)
    #         self.is_adj_created = True

    def action_create_requisition(self):
        product_list = []
        bom = self.env['mrp.bom'].search([])
        for rec in bom:
            product_list.append(rec.product_tmpl_id.id)
        line_vals = []
        line_vals_new = []
        line_vals_three = []
        src_location_one = ''
        src_location_two = ''
        src_location_three = ''
        for line in self.move_raw_ids:
            if line.product_id.product_tmpl_id.id not in product_list and line.reserved_availability < line.product_uom_qty:
                if not line.product_id.requisition_location_id:
                    line_vals.append((0, 0, {
                        'requisition_type': 'internal',
                        'product_id': line.product_id.id,
                        'description': line.product_id.name,
                        'qty':  line.product_uom_qty - line.reserved_availability,
                        'uom': line.product_id.uom_id.id,
                    }))
                    line_vals.append(line_vals)
                    src_location_one = line.product_id.property_stock_production.id
                else:
                    if not src_location_two:
                        src_location_two = line.product_id.requisition_location_id.id
                    else:
                        if not src_location_three and line.product_id.requisition_location_id.id != src_location_two:
                            src_location_three = line.product_id.requisition_location_id.id
                    if src_location_two == line.product_id.requisition_location_id.id:
                        line_vals_new.append((0, 0, {
                            'requisition_type': 'internal',
                            'product_id': line.product_id.id,
                            'description': line.descriptions,
                            'qty': line.product_uom_qty - line.reserved_availability,
                            'uom': line.product_id.uom_id.id,
                        }))
                        line_vals_new.append(line_vals_new)
                        src_location_two = line.product_id.requisition_location_id.id
                    if src_location_three == line.product_id.requisition_location_id.id:
                        line_vals_three.append((0, 0, {
                            'requisition_type': 'internal',
                            'product_id': line.product_id.id,
                            'description': line.descriptions,
                            'qty': line.product_uom_qty - line.reserved_availability,
                            'uom': line.product_id.uom_id.id,
                        }))
                        line_vals_three.append(line_vals_three)
                        src_location_three = line.product_id.requisition_location_id.id
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.user_id.id)])

        if line_vals:
            vals = {
                'company_id': self.company_id.id,
                'department_id': employee.department_id.id,
                'request_date': fields.Date.today(),
                'requisition_line_ids': line_vals,
                'dest_location_id': self.location_src_id.id,
                # 'location_id': src_location_one,
                'ref': self.name,
                'mrp_id': self.id,
                }
            req_one = self.env['material.purchase.requisition'].with_context(default_company_id=self.env.user.company_id.id).create(vals)
            req_one.requisition_confirm()
            req_one.manager_approve()
            req_one.user_approve()
            self.is_req_created = True
        if line_vals_new:
            picking_type = self.env['stock.picking.type'].search([('default_location_src_id', '=', src_location_two), ('code', '=', 'internal')], limit=1)
            vals_two = {
                'company_id': self.company_id.id,
                'department_id': employee.department_id.id,
                'request_date': fields.Date.today(),
                'requisition_line_ids': line_vals_new,
                'dest_location_id': self.location_src_id.id,
                'location_id': src_location_two,
                'ref': self.name,
                'custom_picking_type_id': picking_type.id,
                'mrp_id': self.id,
            }
            req_two = self.env['material.purchase.requisition'].with_context(default_company_id=self.env.user.company_id.id).create(vals_two)
            req_two.requisition_confirm()
            req_two.manager_approve()
            req_two.user_approve()
            self.is_req_created = True
        if line_vals_three:
            picking_type_three = self.env['stock.picking.type'].search(
                [('default_location_src_id', '=', src_location_three), ('code', '=', 'internal')], limit=1)
            vals_three = {
                'company_id': self.company_id.id,
                'department_id': employee.department_id.id,
                'request_date': fields.Date.today(),
                'requisition_line_ids': line_vals_three,
                'dest_location_id': self.location_src_id.id,
                'location_id': src_location_three,
                'ref': self.name,
                'custom_picking_type_id': picking_type_three.id,
                'mrp_id': self.id,
            }
            req_three = self.env['material.purchase.requisition'].with_context(default_company_id=self.env.user.company_id.id).create(vals_three)
            req_three.requisition_confirm()
            req_three.manager_approve()
            req_three.user_approve()
            self.is_req_created = True

    # Manufacturing Order Journal Entry

    # def create_journal_entry(self):
    #     lines = []
    #     amt = 0
    #     for j in self.maintenance_lines_id:
    #         if j.type == 'product':
    #             amt += j.total
    #             move_dict = {
    #                 'ref': self.maintenance_ref,
    #                 # 'branch_id': self.branch_id.id,
    #                 'move_type': 'entry',
    #                 'journal_id': int(
    #                     self.env['ir.config_parameter'].get_param('vehicle_maintenance.journal_expense_id')),
    #                 'date': self.vehicle_in,
    #                 'state': 'draft',
    #             }
    #             debit_line = (0, 0, {
    #                 'name': 'Non Pool Vehicle For Maintenance',
    #                 'debit': j.total,
    #                 'credit': 0.0,
    #                 'partner_id': self.vehicle_id.vendor_id.id,
    #                 'account_id': self.vehicle_id.vendor_id.property_account_payable_id.id,
    #                 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
    #             })
    #             lines.append(debit_line)
    #             credit_line = (0, 0, {
    #                 'name': 'Non Pool Vehicle For Maintenance',
    #                 'debit': 0.0,
    #                 # 'partner_id': r.partner_id.id,
    #                 'credit': j.total,
    #                 'account_id': int(
    #                     self.env['ir.config_parameter'].get_param('vehicle_maintenance.account_non_pool_expense_id')),
    #                 'analytic_account_id': self.vehicle_id.analytical_account_id.id,
    #             })
    #             lines.append(credit_line)
    #             move_dict['line_ids'] = lines
    #     move = self.env['account.move'].create(move_dict)
    #     print("non pooolllllllllllll", move)
    #     self.journal_entry_id = move.id
    #     move.action_post()

    def action_general_entry(self):
        for rec in self:
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            total = 0
            move_dict = {
                'ref': rec.name,
                'journal_id': 11,
                'mo_id': self.id,
                'currency_id': 165,
                'date': datetime.today(),
                'move_type': 'entry',
                'state': 'draft',
            }
            d_acc = self.env['account.account'].search([('name', '=', 'Finished Goods')])
            c_acc = self.env['account.account'].search([('name', '=', 'Work In Process')])
            for line in rec.move_raw_ids:
                total = total + (line.product_id.standard_price * line.quantity_done)
                cr_acc = line.location_dest_id.valuation_out_account_id
            debit_line = (0, 0, {
                'name': rec.product_id.categ_id.property_stock_valuation_account_id.name,
                'debit': abs(total),
                'credit': 0.0,
                # 'partner_id': partner.id,
                'currency_id': 165,
                # 'account_id': d_acc.id,
                'account_id': rec.product_id.categ_id.property_stock_valuation_account_id.id,
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': cr_acc.name,
                'debit': 0.0,
                'credit': abs(total),
                # 'partner_id': partner.id,
                'currency_id': 165,
                'account_id': cr_acc.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
        if line_ids:
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            line_ids = []
            move.button_approved()
            print("General entry created")

    # move_count = fields.Integer(compute='get_move_count')

    # def get_move_count(self):
    #     for rec in self:
    #         count = self.env['account.move'].search_count([('mo_id', '=', self.id)])
    #         rec.move_count = count

    # def action_move_view(self):
    #     return {
    #         'name': ('Journal Vouchers'),
    #         'domain': [('mo_id', '=', self.id)],
    #         'view_type': 'form',
    #         'res_model': 'account.move',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'type': 'ir.actions.act_window',
    #     }

    def server_action_general_entry(self):
        for rec in self:
            if rec.state == 'done':
                entry = self.env['account.move'].search([('mo_id', '=', rec.id)])
                if not entry:
                    line_ids = []
                    debit_sum = 0.0
                    credit_sum = 0.0
                    total = 0
                    move_dict = {
                        'ref': rec.name,
                        'journal_id': 11,
                        'mo_id': rec.id,
                        'currency_id': 165,
                        'date': datetime.today(),
                        'move_type': 'entry',
                        'state': 'draft',
                    }
                    d_acc = self.env['account.account'].search([('name', '=', 'Finished Goods')])
                    c_acc = self.env['account.account'].search([('name', '=', 'Work In Process')])
                    for line in rec.move_raw_ids:
                        total = total + (line.product_id.standard_price * line.quantity_done)
                    debit_line = (0, 0, {
                        'name': 'Finished Goods',
                        'debit': abs(total),
                        'credit': 0.0,
                        # 'partner_id': partner.id,
                        'currency_id': 165,
                        'account_id': d_acc.id,
                    })
                    line_ids.append(debit_line)
                    debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                    credit_line = (0, 0, {
                        'name': 'Work InProcess',
                        'debit': 0.0,
                        'credit': abs(total),
                        # 'partner_id': partner.id,
                        'currency_id': 165,
                        'account_id': c_acc.id,
                    })
                    line_ids.append(credit_line)
                    credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
                    if line_ids:
                        move_dict['line_ids'] = line_ids
                        move = self.env['account.move'].create(move_dict)
                        line_ids = []
                        move.button_approved()
                        print("General entry created")


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    mo_id = fields.Many2one('mrp.production', string='MO REF')

    def action_unpost_entries(self):
        for record in self:
            # if record.state == 'posted':
            record.button_draft()
            record.button_cancel()


# class StockPickingInh(models.Model):
#     _inherit = 'stock.picking'
#
#     def button_validate(self):
#         # res = super(StockPickingInh, self).button_validate()
#         self.action_general_entry()
#         # return res
#
#     def action_general_entry(self):
#         for rec in self:
#             line_ids = []
#             debit_sum = 0.0
#             credit_sum = 0.0
#             total = 0
#             move_dict = {
#                 'ref': rec.name,
#                 'journal_id': 11,
#                 'currency_id': 165,
#                 'date': datetime.today(),
#                 'move_type': 'entry',
#                 'state': 'draft',
#             }
#             # d_acc = self.env['account.account'].search([('name', '=', 'Finished Goods')])
#             # c_acc = self.env['account.account'].search([('name', '=', 'Work In Process')])
#             for line in rec.move_ids_without_package:
#                 total = total + (line.product_id.standard_price * line.quantity_done)
#                 db_acc = line.product_id.categ_id.property_stock_account_output_categ_id
#                 cr_acc = line.product_id.categ_id.property_stock_valuation_account_id
#             debit_line = (0, 0, {
#                 'name': db_acc.name,
#                 'debit': abs(total),
#                 'credit': 0.0,
#                 # 'partner_id': partner.id,
#                 'currency_id': 165,
#                 # 'account_id': d_acc.id,
#                 'account_id': db_acc.id,
#             })
#             line_ids.append(debit_line)
#             debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
#             credit_line = (0, 0, {
#                 'name': cr_acc.name,
#                 'debit': 0.0,
#                 'credit': abs(total),
#                 # 'partner_id': partner.id,
#                 'currency_id': 165,
#                 'account_id': cr_acc.id,
#             })
#             line_ids.append(credit_line)
#             credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
#         if line_ids:
#             move_dict['line_ids'] = line_ids
#             move = self.env['account.move'].create(move_dict)
#             line_ids = []
#             move.button_approved()
#             print("General entry created")


