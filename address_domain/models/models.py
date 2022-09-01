from odoo import api, fields, models


class AddressDomain(models.Model):
    _inherit = "res.partner"

    is_address = fields.Boolean(string='IS Address')

