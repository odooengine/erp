# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    tax_account_id = fields.Many2one('account.account', string='Tax Account')
