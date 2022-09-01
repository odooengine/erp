# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class StockValuationSalesprice(models.Model):
    _inherit = 'stock.quant'

    valuation_salesprice = fields.Float(string="Valuation w.r.t unitprice", compute='get_salesprice_valuation')

    def get_salesprice_valuation(self):
        try:
            for quant in self:
                quant.valuation_salesprice = quant.product_id.free_sold_qty * quant.product_id.lst_price
        except Exception as e:
            raise ValidationError(_(e.args))

    def write(self, vals):
        for rec in self:
            record = super(StockValuationSalesprice, self).write(vals)
            records = self.env['stock.move.line'].search([('picking_id.state', '=', 'in_transit'), ('picking_id.location_id', '=', rec.location_id.id), ('product_id', '=', rec.product_id.id)])
            qty = sum(records.mapped('product_uom_qty'))
            print(records)
            print(rec._context)
            print(qty)
            print(rec.inventory_quantity)
            if 'active_model' in rec._context:
                if rec._context['active_model'] == 'product.product' or rec._context['active_model'] == 'product.template':
                    if rec.inventory_quantity < qty:
                        raise UserError(str(qty) + ' Quantity is already in transit.')
            return record


class StockScrapInh(models.Model):
    _inherit = 'stock.scrap'

    def check_intransit(self, available):
        for rec in self:
            records = self.env['stock.move.line'].search([('picking_id.state', '=', 'in_transit'), ('picking_id.location_id', '=', rec.location_id.id), ('product_id', '=', rec.product_id.id)])
            qty = sum(records.mapped('product_uom_qty'))
            print(qty)
            print(rec.scrap_qty)
            print(available)
            if available - rec.scrap_qty < qty:
                raise UserError(str(qty) + ' Quantity is already in transit.')

    def action_validate(self):
        product = self.env['stock.quant'].search([('product_id', '=', self.product_id.id), ('location_id', '=', self.location_id.id)], limit=1)
        self.check_intransit(product.available_quantity)
        if self.scrap_qty > product.available_quantity:
            raise UserError('Available Quantity is less than Scrap Quantity.')
        else:
            return super(StockScrapInh, self).action_validate()


class ResBranchInh(models.Model):
    _inherit = 'res.branch'

    branch_code = fields.Char('Branch Code')
    # active = fields.Boolean(default=True)


# class ResUsersInh(models.Model):
#     _inherit = 'res.users'

#     agent_code = fields.Char('Agent Code')


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char('Customer Code', copy=False, index=True)
    test = fields.Boolean("Test Field")
    no_cnic = fields.Char('CNIC')
    ntn = fields.Char('NTN')
    fax = fields.Char('Fax')
    beneficiary_name = fields.Char('Beneficiary Name')
    bank_name = fields.Char('Bank Name')
    address = fields.Char('Address')
    iban_no = fields.Char('IBAN NO.')
    swift_code = fields.Char('Swift Code')
    ac_no = fields.Char('Account No.')
    short_code = fields.Char('Amount')
    purpose = fields.Char('Purpose')
    is_supplier = fields.Boolean(default=False, compute='compute_is_supplier')
    # is_current = fields.Boolean('Current Account')
    currency_id = fields.Many2one('res.currency')
    property_account_receivable_id = fields.Many2one('account.account', company_dependent=True,
                                                     string="Account Receivable",
                                                     domain="[('internal_type', 'in', ['receivable','other']), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                                                     help="This account will be used instead of the default one as the receivable account for the current partner",
                                                     required=True)
    # is_employee = fields.Boolean()

    def compute_is_supplier(self):
        for rec in self:
            # rec.partner_balance = rec.credit - rec.debit
            if rec.supplier_rank > 0:
                rec.is_supplier = True
            else:
                rec.is_supplier = False

    # partner_balance = fields.Float('Balance')

    @api.model
    def create(self, vals):
        # if vals.get('customer_code', _('New')) == _('New'):
        vals['customer_code'] = self.env['ir.sequence'].next_by_code('res.partner.sequence') or _('New')
        branch = self.env['res.branch'].browse([vals.get('branch_id')])
        vals['customer_code'] = str(1) + '-' + str(self.env.user.agent_code) + '-' + str(branch.branch_code) + vals['customer_code']
        result = super(ResPartnerInh, self).create(vals)
        return result


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    user_id = fields.Many2one('res.users', related='sale_id.user_id')
    manager_id = fields.Many2one('res.users', related='sale_id.manager_id')
    ref = fields.Char('Reference')

    def action_cancel(self):
        for record in self:
            if record.state in ['assigned', 'in_transit', 'done']:
                raise UserError(_('You Cannot cancel the DO in this State'))
            else:
                result = super(StockPickingInh, self).action_cancel()
                return result

    def do_unreserve(self):
        result = super(StockPickingInh, self).do_unreserve()
        if self.picking_type_id.code == 'outgoing':
            act_type_xmlid = 'mail.mail_activity_data_todo'
            summary = 'My Notification'
            note = 'Delivery Order No ' + str(self.name) + ' is Unreserved.'
            if act_type_xmlid:
                activity_type = self.sudo().env.ref(act_type_xmlid)
            model_id = self.env['ir.model']._get(self._name).id
            create_vals = {
                'activity_type_id': activity_type.id,
                'summary': summary or activity_type.summary,
                'automated': True,
                'note': note,
                'date_deadline': datetime.today(),
                'res_model_id': model_id,
                'res_id': self.id,
                'user_id': self.create_user.id,
            }
            activities = self.env['mail.activity'].create(create_vals)
        return result


class StockWarehouseInh(models.Model):
    _inherit = 'stock.warehouse'

    is_active = fields.Boolean('Active')


class StockLocationInh(models.Model):
    _inherit = 'stock.location'

    is_active = fields.Boolean('Active')


class StockMoveLineInh(models.Model):
    _inherit = 'stock.move.line'

    is_from_active = fields.Boolean('From Active')
    is_to_active = fields.Boolean('To Active', compute='compute_to_from_active')

    def compute_to_from_active(self):
        for rec in self:
            if rec.location_dest_id.is_active:
                rec.is_to_active = True
            else:
                rec.is_to_active = False



