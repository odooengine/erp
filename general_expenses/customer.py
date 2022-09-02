# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError
import datetime

class GeneralExpClass(models.Model):
    _name = 'generalexp.class'
    _description = 'General Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sr_no'
    _order = "id desc"

    sr_no = fields.Char(string="Sr. No")
    date = fields.Date(string="Date", required = True ,default=fields.Date.context_today) 
    journal = fields.Many2one('account.journal',string="Journal", track_visibility='onchange')
    partner_id = fields.Many2one('res.partner',string="Partner", track_visibility='onchange')
    partner_id = fields.Char(string="Partner")
    account = fields.Many2one('account.account',string="Account", track_visibility='onchange', related='journal.default_account_id')
    entry = fields.Many2one('account.move',string="Journal Entry",copy= False)
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    # current_users = fields.Many2one('res.users',string="User",default=lambda self: self._uid)
    amount = fields.Float(string="Total Amount",store=True, track_visibility='onchange')
    descrip = fields.Char(string="Description", track_visibility='onchange')
    # descrip = fields.Char(string="Description",required=True, track_visibility='onchange')
    
    

    # @api.model
    # def create(self, vals):
    #     ret = super(GeneralExpClass, self).create(vals)
    #     self.company_id = vals.get('company_id', self.env.company.id)
    #     return ret

    tree_link = fields.One2many('generalexp.tree','link', track_visibility='onchange')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ],default='draft', track_visibility='onchange')
    
    # type = fields.Selection([
    #   ('assets', 'Asset'),
    #   ],string="Expense Type")

    # @api.onchange('date')
    # def get_company(self):
    #     company = self.env['res.users'].search([('id','=',self._uid)])
    #     self.current_users = company.id

    @api.onchange('tree_link')
    def CalculateAmount(self):
        total = 0 
        for x in self.tree_link:
            total = total + x.amount

        self.amount = total



    # @api.onchange('tree_link')
    # def get_descrip(self):
    #     descrip = 0 
    #     for x in self.tree_link:
    #         descrip = x.descrip

    #     self.descrip = descrip


    @api.onchange('tree_link')
    def get_descrip(self):
        descrip = ""
        for x in self.tree_link:
            if x.descrip:
                descrip = descrip + str(x.descrip) + ","
            else:
                descrip = descrip

        self.descrip = descrip  



    @api.onchange('tree_link')
    def get_partner_ext(self):
        partner_id = ""
        for x in self.tree_link:
            if x.partner_id:
                partner_id =  str(x.partner_id.name) + ", " + partner_id
            else:
                partner_id = ""

        self.partner_id = partner_id  

    # @api.onchange('journal')
    # def get_account(self):
    #     if self.journal.default_debit_account_id:
    #         self.account = self.journal.default_debit_account_id.id
    #     else: 
    #         self.account = False


    @api.model
    def create(self, vals):
        vals['sr_no'] = self.env['ir.sequence'].next_by_code('generalexp.class')
        new_record = super(GeneralExpClass, self).create(vals)
        if not new_record.tree_link:
            raise ValidationError(('"You cannot save without selecting Expense Type" '))

        return new_record

 
    def unlink(self): 
        for x in self: 
            if x.state == "validate": 
                raise ValidationError('Cannot Delete Record') 
        for y in x.tree_link:
            y.unlink()
        rec = super(GeneralExpClass,self).unlink()
        return rec
    def is_validate(self):
        self.create_journal_entry(self.journal,self.date,self.descrip,self.company_id.id)
        for lines in self.tree_link:
            create_credit = self.create_entry_lines(self.account.id,0,lines.amount,self.entry.id,lines.descrip,lines.partner_id)
            create_debit = self.create_entry_lines(lines.expense_type.id,lines.amount,0,self.entry.id,lines.descrip,lines.partner_id)

        self.entry.action_post()
        self.state = "validate"

    def set_all_record_company(self):
        rec = self.env['generalexp.class'].search([])
        company = self.env['res.company'].search([('id','=',1)])
        for x in rec:
            x.company_id = company.id

    def is_draft(self):
        self.state = "draft"
        self.entry.button_draft()

        for x in self.entry.line_ids:
            x.unlink()

    def create_journal_entry(self,journal,date,ref,company):
        if not self.entry:
            print ("111111111111111111111")
            print (ref)
            create_journal_entry = self.env['account.move'].create({
                'company_id': company,
                'journal_id': journal.id,
                'date': date,
                'move_type': 'entry',
                'ref':  ref,   
                })
            self.entry = create_journal_entry.id

    def create_entry_lines(self,account,debit,credit,entry_id,label,partner_id):
        self.env['account.move.line'].create({
            'account_id':account,
            'name': label,
            'debit':debit,
            'credit':credit,
            'move_id':entry_id,
            'partner_id':partner_id.id
            })

class GeneralExpTree(models.Model):
    _name      = 'generalexp.tree'
    _rec_name  = 'expense_type'
    _order     = "id desc"

    date = fields.Date(string="Date", required = True ,default=fields.Date.context_today) 
    descrip = fields.Char(string="Description", track_visibility='onchange')
    expense_type = fields.Many2one('account.account',string="Expense Account" )
    amount = fields.Float(string="Amount", required='True')
    descrip = fields.Char(string="Description")
    partner_id = fields.Many2one('res.partner',string="Partner", track_visibility='onchange')
    # descrip = fields.Char(string="Description",required=True)
    link = fields.Many2one('generalexp.class', string="General Expense")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ],default='draft', track_visibility='onchange', related='link.state')



    @api.constrains('amount')
    def get_amount(self):
        for rec in self:
            if rec.amount == 0:
                print('xxxxxxxxxxxxxxxxxxx')
                raise ValidationError(('"Amount should be greater than 0" '))   
    # ,invisible=True)
    # asset = fields.Many2one('account.asset.asset',string="Asset")
    # assets = fields.Boolean(string="Assets")
    
    # a_type = fields.Selection([
    #   ('capitalize', 'Capitalize'),
    #   ('expense', 'Expense Out'),
    #   ],string="Aesset Type")

    # @api.onchange('expense_type')
    # def CalculateAssets(self):
    #   if self.expense_type:
    #       if self.expense_type.name == 'Assets':
    #           self.assets = True
    #       if self.expense_type.name != 'Assets':
    #           self.assets = False

class ExpenseTypeClass(models.Model):
    _name = 'expense.type'
    _rec_name = 'name'

    name = fields.Char(string="Name") 
    account = fields.Many2one('account.account',string="Account" ,domain="[('user_type_id','!=','Bank and Cash')]")


class account_move_extend_error(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        # vals['date'] = self.env['ir.sequence'].next_by_code('account.move')
        new_record = super(account_move_extend_error, self).create(vals)
        new_record.set_entry_error()
        return new_record

    
    def write(self, vals):
        super(account_move_extend_error, self).write(vals)
        if 'line_ids' in vals:
            self.set_entry_error()
            return True   

    def set_entry_error(self):
        if self.move_type == 'entry':
            if self.line_ids:
                debit = 0
                credit = 0
                for x in self.line_ids:
                    debit += x.debit
                    credit += x.credit
                if debit != credit:
                    raise ValidationError(('"cannot create Journal Entry with only one debit or credit line" '))
                if len(self.line_ids) < 2:
                    raise ValidationError(('"cannot create record with on line" '))
        

    def _check_balanced(self):
        # print ("sddddddddddddddddddddddddddd")
        ''' Assert the move is fully balanced debit = credit.
        An error is raised if it's not the case.
        '''
        moves = self.filtered(lambda move: move.line_ids)
        if not moves:
            return

        # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
        # are already done. Then, this query MUST NOT depend of computed stored fields (e.g. balance).
        # It happens as the ORM makes the create with the 'no_recompute' statement.
        self.env['account.move.line'].flush(['debit', 'credit', 'move_id'])
        self.env['account.move'].flush(['journal_id'])
        self._cr.execute('''
            SELECT line.move_id, ROUND(SUM(debit - credit), currency.decimal_places)
            FROM account_move_line line
            JOIN account_move move ON move.id = line.move_id
            JOIN account_journal journal ON journal.id = move.journal_id
            JOIN res_company company ON company.id = journal.company_id
            JOIN res_currency currency ON currency.id = company.currency_id
            WHERE line.move_id IN %s
            GROUP BY line.move_id, currency.decimal_places
            HAVING ROUND(SUM(debit - credit), currency.decimal_places) != 0.0;
        ''', [tuple(self.ids)])

        query_res = self._cr.fetchall()
        if query_res:
            ids = [res[0] for res in query_res]
            sums = [res[1] for res in query_res]
            # print ("__________________________________________________")
            # print ("__________________________________________________")
            # print ("__________________________________________________")
            # raise UserError(_("Cannot create unbalanced journal entry. Ids: %s\nDifferences debit - credit: %s") % (ids, sums))
        return True


# class AccountEdi(models.Model):
#     _inherit = 'account.edi.document'
#
#     def action_export_xml(self):
#         pass
#
#
# class Payments(models.Model):
#     _inherit = 'account.payment'
#
#     # balance_aml = fields.Float(string="Balance")
#     balance_aml = fields.Float(string="Balance", compute='compute_total_balance')
#     available_partner_bank_ids = fields.Many2many('res.bank', string='Available Partner Bank Ids')
#
#     def compute_total_balance(self):
#         total = self.env['account.move.line'].search([('partner_id', '=', self.partner_id.id)])
#         print(total)
#         self.balance_aml = 2
