# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
from odoo.exceptions import ValidationError
import datetime
import logging


_logger = logging.getLogger(__name__)


class multi_payments(models.Model):
    _name = 'multi.payments'
    _description = 'Making Multi Payments '
    _rec_name= 's_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(string="name")
    s_no = fields.Char(string="Name")
    date = fields.Date(string="Date",track_visibility='onchange')
    journal_id = fields.Many2one('account.journal',string="Bank / Cash",track_visibility='onchange')
    amount = fields.Float(string="Amount",track_visibility='onchange')

    is_withholding_tax = fields.Boolean(string='WithHolding Tax', default=False , track_visibility='onchange')
    total_tax = fields.Float(string="Tax Amount", track_visibility='onchange')
    tax_account_id = fields.Many2one('account.account', String="Tax Account", track_visibility='onchange')


    # operating_unit_id = fields.Many2one('operating.unit', string="Operating Unit", track_visibility='onchange')
    journal_item = fields.Many2one('account.move',string="Journal Entry",copy= False,track_visibility='onchange')
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company,track_visibility='onchange')
    payment_type =fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money')
        ], string="Payment Type",default='outbound',track_visibility='onchange')
    partner_type =fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ], string="Partner Type",track_visibility='onchange')

    voucher_type_o = fields.Selection([
        ('cpv', 'Cash Payment Voucher'),
        ('bpv', 'Bank Payment Voucher'),
        ],track_visibility='onchange',readonly=True)
    voucher_type_i = fields.Selection([
        ('crv', 'Cash Receipt Voucher'),
        ('brv', 'Bank Receipt Voucher'),
        ],track_visibility='onchange',readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate')
    ], string='Status', default='draft',track_visibility='onchange')


    def button_journal_ext(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'journal Item',
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'domain': [('move_id','=',self.journal_item.id)]
        }

    @api.onchange('journal_id')
    def change_journal(self):
        # if self.journal_id.name == 'Bank':
        if self.journal_id.type == 'bank':
            self.voucher_type_o = 'bpv'
        else:
            self.voucher_type_o = 'cpv'



    def set_multi_payments_links(self):
        records = self.search([('state','=','validate'),('id','>',490)], order='id', limit=100)
        _logger.info ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        _logger.info (len(records))
        for payment in records:
            payment.button_draft()
            payment.button_verified()
            _logger.info ("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            _logger.info (payment.id)

    def button_draft(self):
        self.state = 'draft'
        self.journal_item.button_draft()
        self.journal_item.line_ids.unlink()
        # self.journal_item.unlink()

    def unlink(self): 
        for x in self: 
            if x.state in ["validate"]: 
                raise ValidationError('Cannot Delete Record') 
        rec = super(multi_payments,self).unlink()
        return rec

    @api.onchange('tree_link_id')
    def CalculateAmount(self):
        total = 0 
        for x in self.tree_link_id:
            total = total + x.amount

        self.amount = total

    @api.onchange('tree_link_id')
    def calculate_tax(self):
        total = 0
        for x in self.tree_link_id:
            total = total + x.tax_amount
        self.total_tax = total



    @api.model
    def create(self, vals):
        if vals['payment_type'] == 'outbound':
            vals['s_no'] = self.env['ir.sequence'].next_by_code('outbound.payment.type')
        if vals['payment_type'] == 'inbound':
            vals['s_no'] = self.env['ir.sequence'].next_by_code('receive.payment.type')
        new_record = super(multi_payments, self).create(vals)

        return new_record

    def button_verified(self):
        self.general_entry()
        self.state = 'validate'
        # if not self.journal_item:
        #     self.create_journal_entry(self.journal_id,self.date,self.s_no,self.company_id.id)
        # for lines in self.tree_link_id:
        #     if self.payment_type == 'inbound':
        #         # credit_account = lines.partner_id_tree.property_account_receivable_id.id
        #         credit_account = lines.account_id.id
        #         debit_account = self.journal_id.default_account_id.id
        #         create_debit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,debit_account,lines.amount,0,self.journal_item.id, lines.description)
        #         create_credit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,credit_account,0,lines.amount,self.journal_item.id, lines.description)
        #     if self.payment_type == 'outbound':
        #         credit_account = self.journal_id.default_account_id.id
        #         # debit_account = lines.partner_id_tree.property_account_payable_id.id
        #         debit_account = lines.account_id.id
        #         create_debit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,debit_account,lines.amount,0,self.journal_item.id, lines.description)
        #         create_credit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,credit_account,0,lines.amount,self.journal_item.id, lines.description)

        # self.journal_item.action_post()
        # for line in self.journal_item.line_ids:
        #     line.name = line.name + " " + line.payments_tree_label
        

    # def create_journal_entry(self,journal,date,ref,company):
    #     if not self.journal_item:
    #         create_journal_entry = self.env['account.move'].create({
    #             'company_id': company,
    #             'journal_id': journal.id,
    #             'date': self.date,
    #             'move_type': 'entry',
    #             'ref':  ref,
    #             })
    #         self.journal_item = create_journal_entry.id
    #
    # def create_entry_lines(self,partner,date,label,account,debit,credit,entry_id, description):
    #     self.env['account.move.line'].create({
    #         'account_id':account,
    #         'name': label,
    #         'debit':debit,
    #         'credit':credit,
    #         'move_id':entry_id,
    #         'partner_id':partner,
    #         'payments_tree_label':description,
    #         })

    def general_entry(self):
        if self.payment_type == 'inbound':
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            move_dict = {
                # 'name': self.name,
                'journal_id': self.journal_id.id,
                'analytical_account_id': self.analytical_account_id.id,
                # 'partner_id': self.move_lines.partner_id.id,
                'date': self.date,
                'ref': self.s_no,
                'state': 'draft',
            }

            for oline in self.tree_link_id:
                if self.payment_type == 'inbound':
                    credit_account = oline.account_id.id
                    debit_account = self.journal_id.payment_credit_account_id.id if self.payment_type == 'outbound' else self.journal_id.payment_debit_account_id.id
                if self.payment_type == 'outbound':
                    credit_account = self.journal_id.payment_credit_account_id.id if self.payment_type == 'outbound' else self.journal_id.payment_debit_account_id.id
                    debit_account = oline.account_id.id
                debit_line = (0, 0, {
                    'name': oline.name,
                    'debit': abs(oline.amount),
                    'credit': 0.0,
                    'partner_id': oline.partner_id_tree.id,
                    'analytic_tag_ids': oline.analytic_tag_ids.ids,
                    'analytic_account_id': self.analytical_account_id.id,
                    # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                    'account_id': debit_account,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                credit_line = (0, 0, {
                    'name': oline.name,
                    'debit': 0.0,
                    'partner_id': oline.partner_id_tree.id,
                    'credit': abs(oline.amount),
                    'analytic_tag_ids': oline.analytic_tag_ids.ids,
                    'analytic_account_id': self.analytical_account_id.id,
                    'account_id': credit_account,
                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            self.journal_item = move.id
            print("General entry2 created")
        else:
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            tax_sum = 0.0
            move_dict = {
                # 'name': self.name,
                'journal_id': self.journal_id.id,
                'analytical_account_id': self.analytical_account_id.id,
                # 'partner_id': self.move_lines.partner_id.id,
                'date': self.date,
                'ref': self.s_no,
                'state': 'draft',
            }
            for oline in self.tree_link_id:
                if self.payment_type == 'inbound':
                    credit_account = oline.account_id.id
                    debit_account = self.journal_id.payment_credit_account_id.id if self.payment_type == 'outbound' else self.journal_id.payment_debit_account_id.id
                if self.payment_type == 'outbound':
                    credit_account = self.journal_id.payment_credit_account_id.id if self.payment_type == 'outbound' else self.journal_id.payment_debit_account_id.id
                    debit_account = oline.account_id.id
                debit_line = (0, 0, {
                    'name': oline.name,
                    'debit': abs(oline.amount),
                    'credit': 0.0,
                    'partner_id': oline.partner_id_tree.id,
                    'analytic_tag_ids': oline.analytic_tag_ids.ids,
                    'analytic_account_id': self.analytical_account_id.id,
                    # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                    'account_id': debit_account,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                credit_line = (0, 0, {
                    'name': oline.name,
                    'debit': 0.0,
                    'partner_id': oline.partner_id_tree.id,
                    'credit': abs(oline.amount - oline.tax_amount),
                    'analytic_tag_ids': oline.analytic_tag_ids.ids,
                    'analytic_account_id': self.analytical_account_id.id,
                    'account_id': credit_account,
                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
                tax_line = (0, 0, {
                    'name': oline.name,
                    'debit': 0.0,
                    'partner_id': oline.partner_id_tree.id,
                    'credit': abs(oline.tax_amount),
                    'analytic_tag_ids': oline.analytic_tag_ids.ids,
                    'analytic_account_id': self.analytical_account_id.id,
                    'account_id': self.tax_account_id.id,
                })
                line_ids.append(tax_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            self.journal_item = move.id
            print("General entry2 created")

    # def set_all_record_company_ext(self):
    #     rec = self.env['multi.payments'].search([])
    #     company = self.env['res.company'].search([('id','=',1)])
    #     for x in rec:
    #         x.company_id = company.id



    tree_link_id = fields.One2many('multi.payments.tree', 'tree_link')

    # @api.model
    # def create(self, vals):
    #     if len(payment) > 1:
    #         raise UserError('Cheque No Already Exist')
    #     res = super(multi_payments, self).create(vals)
    #     return res
    #
    # def unique_cheque_no(self):
    #     # for record in self:
    #     #     for record.
    #     # if self.cheque_no:
    #     for rec in self:
    #         payment = self.env['multi.payments'].search([('cheque_no', '=', rec.cheque_no)])
    #         if len(payment) > 1:
    #             raise UserError('Cheque No Already Exist')

class multi_payments_tree(models.Model):
    _name = 'multi.payments.tree'
    _description = 'multi_payments.multi_payments.tree'
    _rec_name= 'name'

    account_id = fields.Many2one('account.account', String="Account")
    name = fields.Char(string="name")
    partner_id_tree = fields.Many2one('res.partner',String="Partner" )
    # operating_unit_id = fields.Many2one('operating.unit', string="Operating Unit")
    description = fields.Char(string="Description")
    cheque_no = fields.Char(string="Cheque No")
    amount = fields.Float(string="Amount")
    tax_amount = fields.Float(string="Tax")
    analytic_tag_ids = fields.Many2many('account.analytic.tag')

    @api.onchange('partner_id_tree')
    def onchange_partner(self):
        if self.tree_link.payment_type == 'outbound':
            self.account_id = self.partner_id_tree.property_account_payable_id.id
        if self.tree_link.payment_type == 'inbound':
            self.account_id = self.partner_id_tree.property_account_receivable_id.id
    # analytic_account_id = fields.Many2one('account.analytic.account', String="Analytic Account")

#    @api.constrains('cheque_no')
#    def unique_cheque_no(self):
#        for rec in self:
#            payment = self.env['multi.payments.tree'].search([('cheque_no', '=', rec.cheque_no)])
#            if len(payment) > 1:
#                raise UserError('Cheque No Already Exist')


    @api.constrains('amount')
    def get_amount_payment(self):
        for rec in self:
            if rec.amount == 0:
                raise ValidationError(('"Amount should be greater than 0" '))

    tree_link = fields.Many2one('multi.payments')


class JouenalEntryLinePayExt(models.Model):
    _inherit = 'account.move.line'

    payments_tree_label = fields.Char("Payments Tree Label")


    def set_jes_payments_links(self):
        # records = self.search([('payments_tree_label','!=',False),('id','>',574)], order='id', limit=100)
        records = self.search([('payments_tree_label','!=',False)])
        _logger.info ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        _logger.info (len(records))
        for line in records:
            _logger.info ("IIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            _logger.info (line.id)
            line.name = line.name +" "+line.payments_tree_label


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    available_partner_bank_ids = fields.Many2many('res.bank', string='Available Partner Bank Ids')
    partner_ids = fields.Many2many('res.partner', compute='_compute_partner')
    account_ids = fields.Many2many('account.account', compute='_compute_partner')
    # analytic_account_id = fields.Many2one('account.analytic.account', String="Analytic Account")
    # operating_unit_id = fields.Many2one('operating.unit', string="Operating Unit", track_visibility='onchange')

    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ('int_trnsfr', 'Internal Transfer'),
    ], default='customer', tracking=True, required=True)

    @api.depends('partner_type')
    def _compute_partner(self):
        partners = self.env['res.partner'].search([])
        accounts = self.env['account.account'].search([])
        if self.partner_type == 'customer':
            partners = self.env['res.partner'].search([('customer_rank', '>', 0)])
        elif self.partner_type == 'supplier':
            partners = self.env['res.partner'].search([('supplier_rank', '>', 0)])
        elif self.partner_type == 'int_trnsfr':
            accounts = self.env['account.account'].search([('user_type_id.name', '=', 'Bank and Cash')])
        # elif self.partner_type == 'othr_pay':
        #     accounts = self.env['account.account'].search([('user_type_id.name', '!=', 'Bank and Cash')])

        self.partner_ids = partners.ids
        self.account_ids = accounts.ids

    @api.onchange('partner_type')
    def onchange_partner_type_inh(self):
        if self.partner_type == 'int_trnsfr':
            self.is_internal_transfer = True
        else:
            self.is_internal_transfer = False


# class AccountMoveInh(models.Model):
#     _inherit = 'account.move'
#
#     operating_unit_id = fields.Many2one('operating.unit', string="Operating Unit", track_visibility='onchange')



