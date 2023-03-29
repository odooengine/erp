from odoo import api, models, fields, _
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError, ValidationError
from itertools import groupby


class AccountInherit(models.Model):
    _inherit = "account.move"

    is_commission = fields.Boolean(string="Is Commission")
    po_commission_name = fields.Char(string="Purchase Order")
    commission_total = fields.Float(string="Commission", compute='_compute_commission')
    tax_amount_commission_total = fields.Float(string="Tax Amount", compute='_compute_tax_amount_commission')

    # def action_post(self):
    #     rec = super(AccountInherit, self).action_post()
    #     commission_jvs = self.env['account.move'].search([('ref', '=', self.po_commission_name)])
    #     print("ddddd",commission_jvs)
    #     if commission_jvs:
    #         commission_jvs.action_post()
    #         commission_jvs.button_review()
    #         print("aaaaaaaaaaaa")
    #         commission_jvs.button_approved()
    #     else:
    #         rec = super(AccountInherit, self).action_post()
    #     return rec

    @api.depends('invoice_line_ids.commission')
    def _compute_commission(self):
        for rec in self:
            if rec.is_commission:
                for line in rec.invoice_line_ids:
                    if line:
                        if line.commission:
                            rec.commission_total += line.commission
                        else:
                            rec.commission_total = 0.0
                    else:
                        rec.commission_total = 0.0
            else:
                rec.commission_total = 0.0
    @api.depends('invoice_line_ids.tax_amount_custom')
    def _compute_tax_amount_commission(self):
        for rec in self:
            if rec.is_commission:
                for line in rec.invoice_line_ids:
                    if line.tax_amount_custom:
                        rec.tax_amount_commission_total += line.tax_amount_custom
                    else:
                        rec.tax_amount_commission_total = 0.0
            else:
                rec.tax_amount_commission_total = 0.0


    def get_commission_jv(self):
        return {
            'name': _('Commission Jvs'),
            'domain': [('ref', '=', self.po_commission_name)],
            'view_type': 'form',
            'res_model': 'account.move.line',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    jv_commission_counter = fields.Integer(string='MO', compute='get_jv_commission_counter')

    def get_jv_commission_counter(self):
        for rec in self:
            count = self.env['account.move.line'].search_count([('ref', '=', rec.po_commission_name)])
            rec.jv_commission_counter = count

class AccountLineInherit(models.Model):
    _inherit = "account.move.line"

    commission = fields.Float(string="Commission")
    tax_amount_custom = fields.Float(string="Tax Amount")
    is_commission = fields.Boolean(string="Is Commission")


class AccountSettingCommission(models.TransientModel):
    _inherit = 'res.config.settings'

    expense_commission_account_id = fields.Many2one('account.account', string='Expense Account',
                                        config_parameter='po_commission_jv.expense_commission_account_id')
    tax_asset_commission_account_id = fields.Many2one('account.account', string='Tax(Asset)',
                                                    config_parameter='po_commission_jv.tax_asset_commission_account_id')
    payable_commission_account_id = fields.Many2one('account.account', string='Payable Account',
                                                    config_parameter='po_commission_jv.payable_commission_account_id')
    tax_liability_commission_account_id = fields.Many2one('account.account', string='Tax(Liability) Account',
                                                    config_parameter='po_commission_jv.tax_liability_commission_account_id')






