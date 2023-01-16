from odoo import models, fields, api


# class ConfigSettingsInherit(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     pdc_bnk_customer = fields.Many2one('account.account', string='PDC Bank Account For Customer',
#                                        config_parameter='pdc_payments.pdc_bnk_customer')
#     pdc_receivable = fields.Many2one('account.account', string='PDC Receivable',
#                                      config_parameter='pdc_payments.pdc_receivable')
#
#     pdc_bnk_vendor = fields.Many2one('account.account', string='PDC Bank Account For Vendor',
#                                      config_parameter='pdc_payments.pdc_bnk_vendor')
#     pdc_payable = fields.Many2one('account.account', string='PDC Payable',
#                                   config_parameter='pdc_payments.pdc_payable')


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    pdc_bnk_customer = fields.Many2one('account.account', string='PDC Bank Account For Customer')
    pdc_receivable = fields.Many2one('account.account', string='PDC Receivable')
    pdc_bnk_vendor = fields.Many2one('account.account', string='PDC Bank Account For Vendor')
    pdc_payable = fields.Many2one('account.account', string='PDC Payable')
    is_child_company = fields.Boolean()
    # tax_account_id = fields.Many2one('account.account', string='Tax Account')
    parent_partner_id = fields.Many2one('res.partner', string='Parent Partner')
    parent_company_id = fields.Many2one('res.company', string='Parent Company')

    child_lines = fields.One2many('res.company.child', 'company_id')


class ResCompanyLine(models.Model):
    _name = 'res.company.child'

    company_id = fields.Many2one('res.company')
    # parent_company_id = fields.Many2one('res.company')
    partner_id = fields.Many2one('res.partner')
    journal_id = fields.Many2one('account.journal')
    # child_journal_ids = fields.Many2one('account.journal')
    child_journal_id = fields.Many2one('account.journal')
    tax_account_id = fields.Many2one('account.account')




