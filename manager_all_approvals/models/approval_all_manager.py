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

    # state = fields.Selection([('draft', 'Draft'),
    #                           ('approve', 'Waiting For Approval'),
    #                           ('posted', 'Validated'),
    #                           ('sent', 'Sent'),
    #                           ('reconciled', 'Reconciled'),
    #                           ('cancelled', 'Cancelled'),
    #                           ('reject', 'Reject')
    #                           ], readonly=True, default='draft', copy=False, string="Status")

    def action_post(self):
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
        return rec

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

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
