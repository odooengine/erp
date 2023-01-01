from odoo import models, fields


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    def get_default_location(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        print(employee)
        return employee.dest_location_id

    requisition_location_id = fields.Many2one('stock.location', default=get_default_location)


