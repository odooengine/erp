from odoo import models


class PartnerProductReport(models.AbstractModel):
    _name = 'report.account_partner_reports.partner_product_wise_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, report):
        sheet = workbook.add_worksheet('Test Report')
        center = workbook.add_format({'align': 'center', 'font_size': 8})
        style = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 8})
        date_style = workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'center', 'font_size': 8})

        sheet.set_column('E:E', 12)
        sheet.set_column('F:F', 30)
        sheet.set_column('G:G', 30)
        sheet.set_column('H:H', 12)
        sheet.set_column('I:I', 22)
        sheet.set_column('J:J', 39)

        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        invoices = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('invoice_date', '>=', rec_model.date_from),
             ('invoice_date', '<=', rec_model.date_to), ('partner_id', '=', rec_model.partner_id.id)])

        row = 7
        col = 3

        for obj in report:
            sheet.write(1, 9, 'SHAHID MAHMOOD & CO. (PVT) LTD.', style)
            sheet.write(2, 9, f"Head Office:{self.env.user.company_id.street}", style)
            sheet.write(3, 9, self.env.user.company_id.email, style)
            sheet.write(5, 8, 'Client Account Statement', style)
            col += 1
            sheet.write(row, col, 'Partner', style)
            col += 1
            sheet.write(row, col, obj.partner_id.name, center)
            sheet.write(8, 4, 'Date:', style)
            sheet.write(8, 5, f"{obj.date_from} to {obj.date_to}", date_style)

            r = 10
            c = 4
            sheet.write(r, c, 'Date', style)
            c += 1
            sheet.write(r, c, 'Invoice#', style)
            c += 1
            sheet.write(r, c, 'Item Details', style)
            c += 1
            sheet.write(r, c, 'Article No', style)
            c += 1
            sheet.write(r, c, 'Finish No', style)
            c += 1
            sheet.write(r, c, 'System Code', style)
            c += 1
            sheet.write(r, c, 'Unit', style)
            c += 1
            sheet.write(r, c, 'Rate', style)
            c += 1
            sheet.write(r, c, 'Qty', style)
            c += 1
            sheet.write(r, c, 'Discount', style)
            c += 1
            sheet.write(r, c, 'Net Amount', style)

        for i in invoices:
            for line in i.invoice_line_ids:
                r += 1
                co = 4
                sheet.write(r, co, i.invoice_date, date_style)
                co += 1
                sheet.write(r, co, i.name, center)
                co += 1
                sheet.write(r, co, line.product_id.name, center)
                co += 1
                sheet.write(r, co, line.product_id.article_no, center)
                co += 1
                sheet.write(r, co, line.product_id.finish_no, center)
                co += 1
                sheet.write(r, co, line.product_id.system_code, center)
                co += 1
                sheet.write(r, co, line.product_uom_id.name, center)
                co += 1
                sheet.write(r, co, line.price_unit, center)
                co += 1
                sheet.write(r, co, line.quantity, center)
                co += 1
                sheet.write(r, co, line.discount, center)
                co += 1
                sheet.write(r, co, line.price_subtotal, center)
