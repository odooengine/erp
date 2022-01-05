# -*- coding: utf-8 -*-


from os.path import dirname, abspath
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import csv
from datetime import datetime
from datetime import date
import xlrd


class EngineProductXLSX(models.Model):
    _inherit = 'product.template'

    def create_products(self):
        # loc = ("/home/musadiqfiazch/odoo-14.0/engine_03_01_2022/eng_product_upload/static/engine_products.xlsx")
        loc = abspath(dirname(dirname(dirname(__file__)))) + '/eng_product_upload/static/engine_products.xlsx'
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        i = 0
        for line in range(sheet.nrows):
            i = i + 1
            if i != 1:
                category_records = self.env['product.category'].search([('name', '=', sheet.row_values(line)[9])], limit=1)
                uom_records = self.env['uom.uom'].search([('name', '=', sheet.row_values(line)[7])], limit=1)
                uom_po_records = self.env['uom.uom'].search([('name', '=', sheet.row_values(line)[8])], limit=1)
                vals = {
                    'categ_id': category_records.id,
                    'uom_id': uom_records.id,
                    'uom_po_id': uom_po_records.id,
                    'company_id': 1,
                    'name': sheet.row_values(line)[1],
                    'barcode': sheet.row_values(line)[0],
                    'sale_ok': sheet.row_values(line)[3],
                    'purchase_ok': sheet.row_values(line)[4],
                    'type': sheet.row_values(line)[5],
                    'list_price': sheet.row_values(line)[10],
                    'standard_price': sheet.row_values(line)[6],
                }
                record = self.env['product.template'].create(vals)
