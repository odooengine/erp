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
