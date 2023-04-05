from odoo import api, models, fields, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError, ValidationError
from itertools import groupby
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase



class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    is_commission = fields.Boolean(string="Is Commission" , default=False)
    commission_total = fields.Float(string="Commission" , compute='_compute_commission')
    tax_amount_commission_total = fields.Float(string="Tax Amount" , compute='_compute_tax_amount_commission')

    # picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', states=Purchase.READONLY_STATES,
    #                                   required=True,
    #                                   domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
    #                                   help="This will determine operation type of incoming shipment")
    def _default_picking_type(self):
        rec = super(PurchaseOrderInherit, self)._default_picking_type()
        print(rec)
        return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)

    @api.model
    def _get_picking_type(self, company_id):
        rec = super(PurchaseOrderInherit, self)._get_picking_type(company_id)
        picking_type = self.env['stock.picking.type'].search(
            [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        print(picking_type)
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return False

    @api.depends('order_line.commission')
    def _compute_commission(self):
        for rec in self:
            if rec.is_commission:
                for line in rec.order_line:
                    if line:
                        if line.commission:
                            rec.commission_total += line.commission
                        else:
                            rec.commission_total = 0.0
                    else:
                        rec.commission_total = 0.0
            else:
                rec.commission_total = 0.0

    @api.depends('order_line.tax_amount_custom')
    def _compute_tax_amount_commission(self):
        for rec in self:
            if rec.is_commission:
                for line in rec.order_line:
                    if line.tax_amount_custom:
                        rec.tax_amount_commission_total += line.tax_amount_custom
                    else:
                        rec.tax_amount_commission_total = 0.0
            else:
                rec.tax_amount_commission_total = 0.0
    @api.onchange('is_commission')
    def _onchange_commission(self):
        for rec in self:
            if rec.is_commission:
                for r in rec.order_line:
                    if r:
                        r.is_commission = True

    def action_create_jv(self):
        lines = []
        debit_sum = 0.0
        credit_sum = 0.0
        ex = self.env['ir.config_parameter'].get_param('po_commission_jv.expense_commission_account_id')
        ta = self.env['ir.config_parameter'].get_param('po_commission_jv.tax_asset_commission_account_id')
        pc = self.env['ir.config_parameter'].get_param('po_commission_jv.payable_commission_account_id')
        tl = self.env['ir.config_parameter'].get_param('po_commission_jv.tax_liability_commission_account_id')
        jrnl = self.env['ir.config_parameter'].get_param('po_commission_jv.commission_journal_id')
        expense = self.env['account.account'].search([('id', '=', int(ex))])
        tax_asset = self.env['account.account'].search([('id', '=', int(ta))])
        payable_commission = self.env['account.account'].search([('id', '=', int(pc))])
        tax_liability = self.env['account.account'].search([('id', '=', int(tl))])
        journal = self.env['account.journal'].search([('id', '=', int(jrnl))])
        print(expense)
        print(tax_asset)
        print(payable_commission)
        print(tax_liability)
        print(journal)
        move = []
        for record in self:
            if record.is_commission:
                bill = self.env['account.move'].search([], limit=1, order='create_date desc')
                print("billllll",bill)
                # print("billllll",record.move_id)
                # move_dict = bill
                move_dict = {
                    'ref': record.name,
                    'move_type': 'entry',
                    'partner_id': self.partner_id.id,
                    'date': self.date_approve,
                    'journal_id': journal.id,
                    'state': 'draft',
                    'analytical_account_id': record.analytical_account_id.id,
                }
                # print(move_dict)
                if record.commission_total > 0:
                    debit_line = (0, 0, {
                        'name': record.name,
                        'debit': record.commission_total,
                        'credit': 0.0,
                        'account_id': expense.id,
                        'analytic_account_id': record.analytical_account_id.id,
                    })
                    lines.append(debit_line)
                    credit_line = (0, 0, {
                        'name': record.name,
                        'debit': 0.0,
                        'credit': record.commission_total,
                        'account_id': payable_commission.id,
                        'analytic_account_id': record.analytical_account_id.id,
                    })
                    lines.append(credit_line)
                    move_dict['line_ids'] = lines
                if record.tax_amount_commission_total > 0:
                    debit_line = (0, 0, {
                        'name': record.name,
                        'debit': record.tax_amount_commission_total,
                        'credit': 0.0,
                        'account_id': tax_asset.id,
                        'analytic_account_id': record.analytical_account_id.id,
                        # 'move_id': bill,

                    })
                    lines.append(debit_line)
                    credit_line = (0, 0, {
                        'name': record.name,
                        'debit': 0.0,
                        'credit': record.tax_amount_commission_total,
                        'account_id': tax_liability.id,
                        'analytic_account_id': record.analytical_account_id.id,
                        # 'move_id': bill,
                    })
                    lines.append(credit_line)
                    move_dict['line_ids'] = lines
                move = self.env['account.move'].create(move_dict)
        return move
                # move.action_post()
                # move.button_review()
                # move.button_approved()


    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrderInherit, self)._prepare_invoice()
        if self.is_commission:
            commission_jv = self.action_create_jv()
            print("commission JV" , commission_jv)
            invoice_vals.update({
                'is_commission': self.is_commission,
                'commision_jv_id': commission_jv.id,
                'po_commission_name': self.name,
                'commission_total': self.commission_total,
                'tax_amount_commission_total': self.tax_amount_commission_total,
            })
        # print(invoice_vals)
        # invoice_vals['is_commission'] = self.is_commission
        # invoice_vals['po_commission_name'] = self.name
        # invoice_vals['commission_total'] = self.commission_total
        # invoice_vals['tax_amount_commission_total'] = self.tax_amount_commission_total

        return invoice_vals



class PurchaseOrderLineInherit(models.Model):
    _inherit = "purchase.order.line"

    commission = fields.Float(string="Commission")
    tax_amount_custom = fields.Float(string="Tax Amount")
    is_commission = fields.Boolean(string="Is Commission")

    # def _prepare_account_move_line(self):
    #     res = super(PurchaseOrderLineInherit, self)._prepare_account_move_line()
    #     print("fffff")
    #     res.update({
    #         'commission': self.commission,
    #         'tax_amount_custom': self.tax_amount_custom,
    #         'is_commission': self.is_commission,
    #     })
    #     print(res)
    #     return res

    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        aml_currency = move and move.currency_id or self.currency_id
        date = move and move.date or fields.Date.today()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': '%s: %s' % (self.order_id.name, self.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'purchase_line_id': self.id,
            'commission': self.commission,
            'tax_amount_custom': self.tax_amount_custom,
            'is_commission': self.is_commission,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res







