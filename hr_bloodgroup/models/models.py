# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrBloodGroup(models.Model):
    _name = 'hr.blood.group'
    _description = 'HR Blood Group'

    name = fields.Char('Blood Group')
