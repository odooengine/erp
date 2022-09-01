from odoo import api, fields, models


class AddressDomain(models.Model):
    _inherit = "res.partner"

    partner_type = fields.Selection(selection=[
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('local_vendor', 'Local Vendor'),
        ('import_vendor', 'Import Vendor'),

    ], string='Partner Type', copy=False, tracking=True,
        )

