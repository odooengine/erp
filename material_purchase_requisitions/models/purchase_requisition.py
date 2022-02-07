# -*- coding: utf-8 -*-
import ast

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import Warning, UserError


class MaterialPurchaseRequisition(models.Model):
    _name = 'material.purchase.requisition'
    _description = 'Purchase Requisition'
    # _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']  # odoo11
    _order = 'id desc'

    # @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel', 'reject'):
                raise Warning(
                    _('You can not delete Purchase Requisition which is not in draft or cancelled or rejected state.'))
        return super(MaterialPurchaseRequisition, self).unlink()

    # name = fields.Char(
    #     string='Number',
    #     index=True,
    #     readonly=1,
    # )

    # user_id = fields.Many2one('res.users',string='User')

    name = fields.Char(required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'New'),
        ('dept_confirm', 'Waiting Department Approval'),
        ('ir_approve', 'Waiting IR Approval'),
        ('approve', 'Approved'),
        ('stock', 'Purchase Order Created'),
        ('receive', 'Received'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected')],
        default='draft',
        track_visibility='onchange',
    )
    request_date = fields.Date(
        string='Requisition Date',
        default=fields.Date.today(),
        required=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        copy=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True,
        copy=True,
    )
    approve_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager',
        readonly=True,
        copy=False,
    )
    reject_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager Reject',
        readonly=True,
    )
    approve_employee_id = fields.Many2one(
        'hr.employee',
        string='Approved by',
        readonly=True,
        copy=False,
    )
    reject_employee_id = fields.Many2one(
        'hr.employee',
        string='Rejected by',
        readonly=True,
        copy=False,
    )

    def _default_get_company(self):
        return self.env.company.id

    company_id = fields.Many2one('res.company', 'Company', default=_default_get_company, required=True)
    # company_id = fields.Many2one(
    #     'res.company',
    #     string='Company',
    #     # default=lambda self: self.env.user.company_id,
    #     required=True,
    #     # copy=True,
    # )
    location_id = fields.Many2one(
        'stock.location',
        string='Source Location',
        copy=True,
    )
    requisition_line_ids = fields.One2many(
        'material.purchase.requisition.line',
        'requisition_id',
        string='Purchase Requisitions Line',
        copy=True,
    )
    date_end = fields.Date(
        string='Requisition Deadline',
        readonly=True,
        help='Last date for the product to be needed',
        copy=True,
    )
    date_done = fields.Date(
        string='Date Done',
        readonly=True,
        help='Date of Completion of Purchase Requisition',
    )
    managerapp_date = fields.Date(
        string='Department Approval Date',
        readonly=True,
        copy=False,
    )
    manareject_date = fields.Date(
        string='Department Manager Reject Date',
        readonly=True,
    )
    userreject_date = fields.Date(
        string='Rejected Date',
        readonly=True,
        copy=False,
    )
    userrapp_date = fields.Date(
        string='Approved Date',
        readonly=True,
        copy=False,
    )
    receive_date = fields.Date(
        string='Received Date',
        readonly=True,
        copy=False,
    )
    reason = fields.Text(
        string='Reason for Requisitions',
        required=False,
        copy=True,
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        copy=True,
    )
    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
        required=False,
        copy=True,
    )
    delivery_picking_id = fields.Many2one(
        'stock.picking',
        string='Internal Picking',
        readonly=True,
        copy=False,
    )
    requisiton_responsible_id = fields.Many2one(
        'hr.employee',
        string='Requisition Responsible',
        copy=True,
    )
    employee_confirm_id = fields.Many2one(
        'hr.employee',
        string='Confirmed by',
        readonly=True,
        copy=False,
    )
    confirm_date = fields.Date(
        string='Confirmed Date',
        readonly=True,
        copy=False,
    )

    purchase_order_ids = fields.One2many(
        'purchase.order',
        'custom_requisition_id',
        string='Purchase Ordes',
    )
    custom_picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Picking Type',
        copy=False,
    )

    vendor_id = fields.Many2one('res.partner')
    mrp_id = fields.Many2one('mrp.production')
    tech_pack = fields.Char('Tech Pack')

    @api.model
    def create(self, vals):
        # name = self.env['ir.sequence'].next_by_code('purchase.requisition.seq')
        # print(name)
        # vals.update({
        #     'name': name
        #     })
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('req.sequence') or _('New')
        # print(self.env['ir.sequence'].next_by_code('req.sequence'))
        res = super(MaterialPurchaseRequisition, self).create(vals)
        # print(res.name)
        return res

    # @api.multi
    def requisition_confirm(self):
        for rec in self:
            manager_mail_template = self.env.ref(
                'material_purchase_requisitions.email_confirm_material_purchase_requistion')
            rec.employee_confirm_id = rec.employee_id.id
            rec.confirm_date = fields.Date.today()
            rec.state = 'dept_confirm'
            if manager_mail_template:
                manager_mail_template.send_mail(self.id)

    # @api.multi
    def requisition_reject(self):
        for rec in self:
            rec.state = 'reject'
            rec.reject_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.userreject_date = fields.Date.today()

    # @api.multi
    def manager_approve(self):
        for rec in self:
            rec.managerapp_date = fields.Date.today()
            rec.approve_manager_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            employee_mail_template = self.env.ref(
                'material_purchase_requisitions.email_purchase_requisition_iruser_custom')
            email_iruser_template = self.env.ref('material_purchase_requisitions.email_purchase_requisition')
            employee_mail_template.sudo().send_mail(self.id)
            email_iruser_template.sudo().send_mail(self.id)
            rec.state = 'ir_approve'

    # @api.multi
    def user_approve(self):
        for rec in self:
            rec.userrapp_date = fields.Date.today()
            rec.approve_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.state = 'approve'

    # @api.multi
    def reset_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def _prepare_pick_vals(self, line=False, stock_id=False):
        pick_vals = {
            'product_id': line.product_id.id,
            'product_uom_qty': line.qty,
            'product_uom': line.uom.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.dest_location_id.id,
            'name': line.product_id.name,
            'picking_type_id': self.custom_picking_type_id.id,
            'picking_id': stock_id.id,
            'custom_requisition_line_id': line.id,
            'company_id': line.requisition_id.company_id.id,
        }
        return pick_vals

    @api.model
    def _prepare_po_line(self, line=False, purchase_order=False):
        po_line_vals = {
            'product_id': line.product_id.id,
            'name': line.product_id.name,
            'product_qty': line.qty,
            'product_uom': line.uom.id,
            'date_planned': fields.Date.today(),
            'price_unit': line.product_id.standard_price,
            'order_id': purchase_order.id,
            'account_analytic_id': self.analytic_account_id.id,
            'custom_requisition_line_id': line.id
        }
        return po_line_vals

    # @api.multi
    def request_stock(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        # internal_obj = self.env['stock.picking.type'].search([('code','=', 'internal')], limit=1)
        # internal_obj = self.env['stock.location'].search([('usage','=', 'internal')], limit=1)
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        #         if not internal_obj:
        #             raise UserError(_('Please Specified Internal Picking Type.'))
        for rec in self:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                    raise Warning(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                    raise Warning(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise Warning(_('Select Destination location under the picking details.'))
                #                 if not rec.employee_id.dest_location_id.id or not rec.employee_id.department_id.dest_location_id.id:
                #                     raise Warning(_('Select Destination location under the picking details.'))

                picking_vals = {
                    'partner_id': rec.employee_id.sudo().address_home_id.id,
                    # 'min_date' : fields.Date.today(),
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                    'picking_type_id': rec.custom_picking_type_id.id,  # internal_obj.id,
                    'note': rec.reason,
                    'custom_requisition_id': rec.id,
                    'origin': rec.name,
                    'company_id': rec.company_id.id,
                    'product_ref_id': rec.mrp_id.product_id.id,
                    'product_tmpl_ref_id': rec.mrp_id.product_id.product_tmpl_id.id,

                }
                print(rec.company_id.name)
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {
                    'delivery_picking_id': stock_id.id,
                }
                rec.write(delivery_vals)
            po_dict = {}
            if rec.vendor_id:
                for line in rec.requisition_line_ids:
                    line.partner_id = [rec.vendor_id.id]
            else:
                for re_line in rec.requisition_line_ids:
                    if re_line.requisition_type == 'purchase':
                        raise UserError('Please Select Vendor.')
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'internal':
                    pick_vals = rec._prepare_pick_vals(line, stock_id)
                    move_id = move_obj.sudo().create(pick_vals)
                if line.requisition_type == 'purchase':  # 10/12/2019
                    if not line.partner_id:
                        raise Warning(
                            _('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                stock_id.action_confirm()
            rec.action_create_po()
            rec.state = 'stock'

    #                     for partner in line.partner_id:
    #                         if partner not in po_dict:
    #                             po_vals = {
    #                                 'partner_id':partner.id,
    #                                 'currency_id':rec.env.user.company_id.currency_id.id,
    #                                 'date_order':fields.Date.today(),
    # #                                'company_id':rec.env.user.company_id.id,
    #                                 'company_id':rec.company_id.id,
    #                                 'custom_requisition_id':rec.id,
    #                                 'origin': rec.name,
    #                             }
    #                             purchase_order = purchase_obj.create(po_vals)
    #                             po_dict.update({partner:purchase_order})
    #                             po_line_vals = rec._prepare_po_line(line, purchase_order)
    # #                            {
    # #                                     'product_id': line.product_id.id,
    # #                                     'name':line.product_id.name,
    # #                                     'product_qty': line.qty,
    # #                                     'product_uom': line.uom.id,
    # #                                     'date_planned': fields.Date.today(),
    # #                                     'price_unit': line.product_id.lst_price,
    # #                                     'order_id': purchase_order.id,
    # #                                     'account_analytic_id': rec.analytic_account_id.id,
    # #                            }
    #                             purchase_line_obj.sudo().create(po_line_vals)
    #                         else:
    #                             purchase_order = po_dict.get(partner)
    #                             po_line_vals = rec._prepare_po_line(line, purchase_order)
    # #                            po_line_vals =  {
    # #                                 'product_id': line.product_id.id,
    # #                                 'name':line.product_id.name,
    # #                                 'product_qty': line.qty,
    # #                                 'product_uom': line.uom.id,
    # #                                 'date_planned': fields.Date.today(),
    # #                                 'price_unit': line.product_id.lst_price,
    # #                                 'order_id': purchase_order.id,
    # #                                 'account_analytic_id': rec.analytic_account_id.id,
    # #                            }
    #                             purchase_line_obj.sudo().create(po_line_vals)
    #                 rec.state = 'stock'

    def action_create_po(self):
        info_dict = {}
        info_list = []
        # for rec in self.requisition_line_ids:
        #     if not rec.product_id.id in info_dict:
        #         val = {'product_id': rec.product_id.id, 'qty' : rec.qty}
        #         info_list.append(val)
        #     else:

        val_list = []

        for rec in self.requisition_line_ids:
            if rec.requisition_type == 'purchase':
                if rec.product_id.product_tmpl_id.id not in val_list:
                    val_list.append(rec.product_id.product_tmpl_id.id)
        # print(val_list)
        for res in val_list:
            val = []
            for record in self.requisition_line_ids:
                # print()
                if record.requisition_type == 'purchase':
                    if record.product_id.product_tmpl_id.id == res:
                        val.append((0, 0, {
                            'product_id': record.product_id.id,
                            # 'product_tmpl_id': record.product_id.product_tmpl_id.id,
                            'name': record.product_id.name,
                            'product_qty': record.qty,
                            'product_uom': record.uom.id,
                            # 'date_planned': datetime.today().date(),
                            'price_unit': record.product_id.standard_price,
                            'partners': record.partner_id.id,
                            # 'account_analytic_id': self.analytic_account_id.id,
                            'custom_requisition_line_id': record.id
                        }))
            print(val)
            # for res in val:
            #     copy_dict = res.copy()
            # val.pop('product_tmpl_id')
            if val:
                partner = ''
                for i in val:
                    partner = i[2]['partners']
                    i[2].pop('partners')
                #     for partner in res['partners']:
                po_vals = {
                    'partner_id': partner,
                    'currency_id': self.env.user.company_id.currency_id.id,
                    'date_order': fields.Date.today(),
                    'company_id': self.company_id.id,
                    'order_line': val,
                    'custom_requisition_id': self.id,
                    'origin': self.name,
                }
                purchase_order = self.env['purchase.order'].create(po_vals)
        #     print(val)
        # print(val)
        # for l in val_list:
        #     qty = 0
        #     partner_list = []
        #     for i in val:
        #         if i['product_tmpl_id'] == l:
        #             qty = qty + i['product_qty']
        #             for k in i['partners']:
        #                 partner_list.append(k)
        #     partner_list = list(dict.fromkeys(partner_list))
        #     for j in val:
        #         if j['product_tmpl_id'] == l:
        #             j['product_qty'] = qty
        #             j['partners'] = partner_list
        # data = {r['product_tmpl_id']: r for r in val}.values()
        # print(data)
        #
        # for res in data:
        #     # print(res['partners'])
        #     copy_dict = res.copy()
        #     copy_dict.pop('product_tmpl_id')
        #     copy_dict.pop('partners')
        #     # print(res)
        #     for partner in res['partners']:
        #         po_vals = {
        #             'partner_id': partner,
        #             'currency_id': self.env.user.company_id.currency_id.id,
        #             'date_order': fields.Date.today(),
        #             'company_id': self.company_id.id,
        #             'order_line': [(0, 0, copy_dict)],
        #             'custom_requisition_id': self.id,
        #             'origin': self.name,
        #         }
        #         purchase_order = self.env['purchase.order'].create(po_vals)

    #         for r in info_list:
    #             for line in self.requisition_line_ids:
    #                 if line.product_id.id == r:
    #                     po_line_vals = {
    #                         'product_id': line.product_id.id,
    #                         'name': line.product_id.name,
    #                         'product_qty': line.qty,
    #                         'product_uom': line.uom.id,
    #                         'date_planned': fields.Date.today(),
    #                         'price_unit': line.product_id.standard_price,
    #                         'order_id': purchase_order.id,
    #                         'account_analytic_id': self.analytic_account_id.id,
    #                         'custom_requisition_line_id': line.id
    #                     }
    #                     purchase_order_line = self.env['purchase.order.line'].create(po_line_vals)
    #                 else:
    #                     po_vals = {
    #                             'partner_id':line.partner_id[0].id,
    #                             'currency_id':self.env.user.company_id.currency_id.id,
    #                             'date_order':fields.Date.today(),
    # #                                'company_id':rec.env.user.company_id.id,
    #                             'company_id':self.company_id.id,
    #                             'custom_requisition_id':self.id,
    #                             'origin': self.name,
    #                     }
    #                     purchase_order = self.env['purchase.order'].create(po_vals)

    # @api.multi
    def action_received(self):
        for rec in self:
            rec.receive_date = fields.Date.today()
            rec.state = 'receive'

    # @api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.onchange('employee_id')
    def set_department(self):
        for rec in self:
            rec.department_id = rec.employee_id.sudo().department_id.id
            rec.dest_location_id = rec.employee_id.sudo().dest_location_id.id or rec.employee_id.sudo().department_id.dest_location_id.id

            # @api.multi

    def show_picking(self):
        for rec in self:
            res = self.env.ref('stock.action_picking_tree_all')
            res = res.read()[0]
            res['domain'] = str([('custom_requisition_id', '=', rec.id)])
        return res

    # @api.multi
    def action_show_po(self):
        for rec in self:
            purchase_action = self.env.ref('purchase.purchase_rfq')
            purchase_action = purchase_action.read()[0]
            purchase_action['domain'] = str([('custom_requisition_id', '=', rec.id)])
        return purchase_action
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
