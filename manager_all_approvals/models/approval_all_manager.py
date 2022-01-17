from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountEdi(models.Model):
    _inherit = 'account.edi.document'

    def action_export_xml(self):
        pass


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_confirm(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_purchase_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_purchase_order'):
            self.approve_by_id = self.env.user.id
        for order in self:
            if order.state not in ['draft', 'sent', 'approve']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_confirm(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_sale_order'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_sale_order'):
            self.approve_by_id = self.env.user.id
        rec = super(SaleOrderInh, self).action_confirm()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })


class MRPProductionInh(models.Model):
    _inherit = 'mrp.production'

    # review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approval'),
        ('confirmed', 'Confirmed'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected')], string='State',
        compute='_compute_state', copy=False, index=True, readonly=True,
        store=True, tracking=True,
        help=" * Draft: The MO is not confirmed yet.\n"
             " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
             " * In Progress: The production has started (on the MO or on the WO).\n"
             " * To Close: The production is done, the MO has to be closed.\n"
             " * Done: The MO is closed, the stock moves are posted. \n"
             " * Cancelled: The MO has been cancelled, can't be confirmed anymore.")

    def _create_notification(self):
        for res in self:
            act_type_xmlid = 'mail.mail_activity_data_todo'
            summary = 'MO Approval'
            note = 'Manufacturing order no:' + res.name + ' is waiting for Approval.'
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
                        'user_id': rec.id,
                    }
                    activities = self.env['mail.activity'].create(create_vals)

    def action_confirm(self):
        self._create_notification()
        self.write({
            'state': 'approve'
        })

    # def button_review(self):
    #     if self.env.user.has_group('manager_all_approvals.group_review_mrp'):
    #         self.review_by_id = self.env.user.id
    #     self.write({
    #         'state': 'approve'
    #     })

    # def action_reject(self):
    #     self.write({
    #         'state': 'rejected'
    #     })

    # def button_approved(self):
    #     if self.env.user.has_group('manager_all_approvals.group_approve_mrp'):
    #         self.approve_by_id = self.env.user.id
    #     rec = super(MRPProductionInh, self).button_mark_done()
    #     return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_mrp'):
            self.approve_by_id = self.env.user.id
        rec = super(MRPProductionInh, self).action_confirm()
        return rec


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('to_review', 'Waiting For Review'),
        ('approve', 'Waiting For Approval'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')

    def action_post(self):
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_invoice_bill'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_invoice_bill'):
            self.approve_by_id = self.env.user.id
        rec = super(AccountMoveInh, self).action_post()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })



class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')
    transfer_account_id = fields.Many2one('account.account')
    cheque_no = fields.Char('Cheque No', default='')

    @api.constrains('cheque_no')
    def unique_cheque_no(self):
        if self.cheque_no:
            payment = self.env['account.payment'].search([('cheque_no', '=', self.cheque_no)])
            if len(payment) > 1:
                raise UserError('Cheque No Already Exist')

    @api.onchange('cheque_no')
    def set_caps(self):
        val = str(self.cheque_no)
        self.cheque_no = val.upper()

    # state = fields.Selection([('draft', 'Draft'),
    #                           ('approve', 'Waiting For Approval'),
    #                           ('posted', 'Validated'),
    #                           ('sent', 'Sent'),
    #                           ('reconciled', 'Reconciled'),
    #                           ('cancelled', 'Cancelled'),
    #                           ('reject', 'Reject')
    #                           ], readonly=True, default='draft', copy=False, string="Status")

    @api.model
    def create(self, vals):
        record = super(AccountPaymentInh, self).create(vals)
        if record.is_internal_transfer:
            record.payment_type = 'outbound'
        return record

    # def write(self, vals):
    #     record = super(AccountPaymentInh, self).write(vals)
    #     if self.is_internal_transfer:
    #         self.payment_type = 'outbound'
    #     record = super(AccountPaymentInh, self).write(vals)
    #     return record

    @api.onchange('is_internal_transfer')
    def onchange_internal_transfer(self):
        if self.is_internal_transfer:
            self.payment_type = 'outbound'

    def action_show_move_lines(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Move Line',
            'view_id': self.env.ref('account.view_move_line_tree', False).id,
            'target': 'current',
            'domain': [('payment_id', '=', self.id)],
            'res_model': 'account.move.line',
            'views': [[False, 'tree'], [False, 'form']],
        }

    def action_post(self):
        print(self.cheque_no)
        if self.journal_id.type == 'bank' and not self.cheque_no:
            raise UserError('Please Enter Valid Cheque No.')
        self.write({
            'state': 'to_review'
        })

    def button_review(self):
        if self.env.user.has_group('manager_all_approvals.group_review_payment'):
            self.review_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    def action_reset(self):
        self.write({
            'state': 'draft'
        })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_payment'):
            self.approve_by_id = self.env.user.id
        rec = super(AccountPaymentInh, self).action_post()
        if self.is_internal_transfer:
            self.general_entry()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    def general_entry(self):
        if not self.transfer_account_id:
            raise UserError('Please Add Transfer To Account.')
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        move_dict = {
            'ref': self.name,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_id.id,
            'date': self.date,
            # 'state': 'draft',
        }
        # for oline in self.move_lines:
        debit_line = (0, 0, {
            'name': self.ref,
            'debit': abs(self.amount),
            'credit': 0.0,
            'partner_id': self.partner_id.id,
            # 'analytic_account_id': oline.analytic_account_id.id,
            # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
            # 'account_id': self.destination_account_id.id,
            'account_id': self.transfer_account_id.id,
            'payment_id': self.id,
        })
        line_ids.append(debit_line)
        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
        credit_line = (0, 0, {
            'name': self.ref,
            'date_maturity': self.date,
            'debit': 0.0,
            'partner_id': self.partner_id.id,
            'credit': abs(self.amount),
            # 'account_id': self.transfer_account_id.id,
            'account_id': self.destination_account_id.id,
            'payment_id': self.id,
        })
        line_ids.append(credit_line)
        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
        print(line_ids)
        # self.move_id.button_draft()
        # self.move_id.update({
        #     'line_ids': line_ids
        # })
        move_dict['line_ids'] = line_ids
        # self.move_id.update({
        #         'line_ids': line_ids
        #     })
        # move_dict['move_id'] = self.move_id.id
        rec = self.env['account.move'].create(move_dict)
        for l in rec.line_ids:
            l.payment_id = self.id
        rec.action_post()
        rec.button_review()
        rec.button_approved()
        print("General entry created")

    # def _prepare_move_line_default_vals(self, write_off_line_vals=None):
    #     ''' Prepare the dictionary to create the default account.move.lines for the current payment.
    #     :param write_off_line_vals: Optional dictionary to create a write-off account.move.line easily containing:
    #         * amount:       The amount to be added to the counterpart amount.
    #         * name:         The label to set on the line.
    #         * account_id:   The account on which create the write-off.
    #     :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
    #     '''
    #     print('Helooooooo')
    #     self.ensure_one()
    #     write_off_line_vals = write_off_line_vals or {}
    #
    #     if not self.journal_id.payment_debit_account_id or not self.journal_id.payment_credit_account_id:
    #         raise UserError(_(
    #             "You can't create a new payment without an outstanding payments/receipts account set on the %s journal.",
    #             self.journal_id.display_name))
    #
    #     # Compute amounts.
    #     write_off_amount = write_off_line_vals.get('amount', 0.0)
    #
    #     if self.payment_type == 'inbound':
    #         # Receive money.
    #         counterpart_amount = -self.amount
    #         write_off_amount *= -1
    #     elif self.payment_type == 'outbound':
    #         # Send money.
    #         counterpart_amount = self.amount
    #     else:
    #         counterpart_amount = 0.0
    #         write_off_amount = 0.0
    #
    #     balance = self.currency_id._convert(counterpart_amount, self.company_id.currency_id, self.company_id, self.date)
    #     counterpart_amount_currency = counterpart_amount
    #     write_off_balance = self.currency_id._convert(write_off_amount, self.company_id.currency_id, self.company_id, self.date)
    #     write_off_amount_currency = write_off_amount
    #     currency_id = self.currency_id.id
    #
    #     if self.is_internal_transfer:
    #         if self.payment_type == 'inbound':
    #             liquidity_line_name = _('Transfer to %s', self.journal_id.name)
    #         else: # payment.payment_type == 'outbound':
    #             liquidity_line_name = _('Transfer from %s', self.journal_id.name)
    #     else:
    #         liquidity_line_name = self.payment_reference
    #
    #     # Compute a default label to set on the journal items.
    #
    #     payment_display_name = {
    #         'outbound-customer': _("Customer Reimbursement"),
    #         'inbound-customer': _("Customer Payment"),
    #         'outbound-supplier': _("Vendor Payment"),
    #         'inbound-supplier': _("Vendor Reimbursement"),
    #     }
    #
    #     default_line_name = self.env['account.move.line']._get_default_line_name(
    #         _("Internal Transfer") if self.is_internal_transfer else payment_display_name['%s-%s' % (self.payment_type, self.partner_type)],
    #         self.amount,
    #         self.currency_id,
    #         self.date,
    #         partner=self.partner_id,
    #     )
    #
    #     line_vals_list = [
    #         # Liquidity line.
    #         {
    #             'name': liquidity_line_name or default_line_name,
    #             'date_maturity': self.date,
    #             'amount_currency': -counterpart_amount_currency,
    #             'currency_id': currency_id,
    #             'debit': balance < 0.0 and -balance or 0.0,
    #             'credit': balance > 0.0 and balance or 0.0,
    #             'partner_id': self.partner_id.id,
    #             'account_id': self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id,
    #         },
    #         # Receivable / Payable.
    #         {
    #             'name': self.payment_reference or default_line_name,
    #             'date_maturity': self.date,
    #             'amount_currency': counterpart_amount_currency + write_off_amount_currency if currency_id else 0.0,
    #             'currency_id': currency_id,
    #             'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
    #             'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
    #             'partner_id': self.partner_id.id,
    #             'account_id': self.transfer_account_id.id,
    #         },
    #
    #     ]
    #     if write_off_balance:
    #         # Write-off line.
    #         line_vals_list.append({
    #             'name': write_off_line_vals.get('name') or default_line_name,
    #             'amount_currency': -write_off_amount_currency,
    #             'currency_id': currency_id,
    #             'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
    #             'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
    #             'partner_id': self.partner_id.id,
    #             'account_id': write_off_line_vals.get('account_id'),
    #         })
    #     return line_vals_list

    # def button_approve(self):
    # AccountMove = self.env['account.move'].with_context(default_type='entry')
    # for rec in self:
    #
    #     if rec.state != 'approve':
    #         raise UserError(_("Only a draft payment can be posted."))
    #
    #     if any(inv.state != 'posted' for inv in rec.invoice_ids):
    #         raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
    #
    #     # keep the name in case of a payment reset to draft
    #     if not rec.name:
    #         # Use the right sequence to set the name
    #         if rec.payment_type == 'transfer':
    #             sequence_code = 'account.payment.transfer'
    #         else:
    #             if rec.partner_type == 'customer':
    #                 if rec.payment_type == 'inbound':
    #                     sequence_code = 'account.payment.customer.invoice'
    #                 if rec.payment_type == 'outbound':
    #                     sequence_code = 'account.payment.customer.refund'
    #             if rec.partner_type == 'supplier':
    #                 if rec.payment_type == 'inbound':
    #                     sequence_code = 'account.payment.supplier.refund'
    #                 if rec.payment_type == 'outbound':
    #                     sequence_code = 'account.payment.supplier.invoice'
    #         rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
    #         if not rec.name and rec.payment_type != 'transfer':
    #             raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))
    #
    #     moves = AccountMove.create(rec._prepare_payment_moves())
    #     moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
    #
    #     # Update the state / move before performing any reconciliation.
    #     move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
    #     rec.write({'state': 'posted', 'move_name': move_name})
    #
    #     if rec.payment_type in ('inbound', 'outbound'):
    #         # ==== 'inbound' / 'outbound' ====
    #         if rec.invoice_ids:
    #             (moves[0] + rec.invoice_ids).line_ids \
    #                 .filtered(
    #                 lambda line: not line.reconciled and line.account_id == rec.destination_account_id and not (
    #                             line.account_id == line.payment_id.writeoff_account_id and line.name == line.payment_id.writeoff_label)) \
    #                 .reconcile()
    #     elif rec.payment_type == 'transfer':
    #         # ==== 'transfer' ====
    #         moves.mapped('line_ids') \
    #             .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id) \
    #             .reconcile()
    #
    # return True


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    # review_by_id = fields.Many2one('res.users', string='Reviewed By')
    approve_by_id = fields.Many2one('res.users', string='Approved By')
    received_by_id = fields.Many2one('res.users', string='Received By')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('approve', 'Waiting For Approval'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('rejected', 'Rejected'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    def button_validate(self):
        for record in self.move_ids_without_package:
            print(record.quantity_done)
            print(record.product_uom_qty)
            if record.quantity_done > record.product_uom_qty:
                raise UserError(_('Receiving Quantity Cannot be Exceeded Than Demanded'))
        self.received_by_id = self.env.user.id
        self.write({
            'state': 'approve'
        })

    # def button_review(self):
    #     if self.env.user.has_group('manager_all_approvals.group_review_transfer'):
    #         self.review_by_id = self.env.user.id
    #     self.write({
    #         'state': 'approve'
    #     })

    # def action_reject(self):
    #     self.write({
    #         'state': 'rejected'
    #     })

    def button_approved(self):
        if self.env.user.has_group('manager_all_approvals.group_approve_transfer'):
            self.approve_by_id = self.env.user.id
        rec = super(StockPickingInh, self).button_validate()
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })


class StockImmediateTransferInh(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.immediate_transfer_line_ids:
            if line.to_immediate is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for picking in pickings_to_do:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError \
                            (_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate)
            pickings_to_validate = pickings_to_validate - pickings_not_to_do
            return pickings_to_validate.with_context(skip_immediate=True).button_approved()
        return True


class StockBackorderConfirmationInh(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.backorder_confirmation_line_ids:
            if line.to_backorder is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for pick_id in pickings_not_to_do:
            moves_to_log = {}
            for move in pick_id.move_lines:
                if float_compare(move.product_uom_qty,
                                 move.quantity_done,
                                 precision_rounding=move.product_uom.rounding) > 0:
                    moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
            pick_id._log_less_quantities_than_expected(moves_to_log)

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(
                skip_backorder=True)
            if pickings_not_to_do:
                pickings_to_validate = pickings_to_validate.with_context(
                    picking_ids_not_to_backorder=pickings_not_to_do.ids)

            return pickings_to_validate.button_approved()
        return True

    def process_cancel_backorder(self):
        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            return self.env['stock.picking'] \
                .browse(pickings_to_validate) \
                .with_context(skip_backorder=True, picking_ids_not_to_backorder=self.pick_ids.ids) \
                .button_approved()
        return True
