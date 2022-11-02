from odoo import models, fields


class MrpProductionInherited(models.Model):
    _inherit = 'mrp.production'

    origin = fields.Char('Source', required=True)
