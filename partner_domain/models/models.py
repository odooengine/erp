# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeInh(models.Model):
    _inherit = 'res.partner'

    is_employee = fields.Boolean()


