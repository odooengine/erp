# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveLineInh(models.Model):
    _inherit = "account.move.line"

    is_check = fields.Boolean(string='Check', default=False)
