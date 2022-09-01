from odoo import models, fields, api


class HrContractBonus(models.Model):
    _inherit = 'hr.contract'

    previous_bonus = fields.Float('Previous Bonus')

