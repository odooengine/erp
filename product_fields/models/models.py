from odoo import api, models, fields


class StatusProduct(models.Model):
    _inherit = "product.product"

    status = fields.Char(string='Status')
    book_number = fields.Char(string='Book No')


class StatusProductTemplate(models.Model):
    _inherit = "product.template"

    status = fields.Char(string='Status')
    book_number = fields.Char(string='Book No')

    @api.model
    def create(self, vals):
        res = super(StatusProductTemplate, self).create(vals)
        res.product_variant_ids.update({
            'status': res.status,
            'book_number': res.book_number,
        })
        return res

    def write(self, vals):
        res = super(StatusProductTemplate, self).write(vals)
        if 'status' or 'book_number' in vals:
            self.product_variant_ids.update({
                'status': self.status,
                'book_number': self.book_number,
            })
        return res


class InheritINV(models.Model):
    _inherit = "stock.picking"

    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=True, required=True,
        check_company=True,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations." , tracking=True )
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=True, index=True, required=True,
        check_company=True,
        help="Location where the system will stock the finished products." , tracking=True )


class InheritMRP(models.Model):
    _inherit = "mrp.production"

    @api.model
    def _get_default_location_src_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(
                self.env.context['default_picking_type_id']).default_location_src_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(
                self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    location_src_id = fields.Many2one(
        'stock.location', 'Components Location',
        default=_get_default_location_src_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will look for components." , tracking=True )

    location_dest_id = fields.Many2one(
        'stock.location', 'Finished Products Location',
        default=_get_default_location_dest_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will stock the finished products." , tracking=True )

