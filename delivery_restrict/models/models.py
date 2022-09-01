from odoo import api, fields, models


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    restricted_locations = fields.Many2many('stock.location', string='Restrict Locations')

