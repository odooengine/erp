from odoo import models
import string
from datetime import datetime,date, timedelta


class PayrollReport(models.AbstractModel):
    _name = 'report.xlsx_payroll_report.xlsx_payroll_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # print("lines", lines)
        # workbook = xlsxwriter.Workbook(file_name, {'in_memory': True})
        print(workbook)
        format_left = workbook.add_format(
            {'font_size': 15, 'align': 'left', 'bold': True, 'bg_color': '#d3dde3', 'color': 'black',
             'bottom': True, })
        format1 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'bold': True, 'bg_color': '#d3dde3', 'color': 'black',
             'bottom': True, })
        format2 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'bold': True, 'bg_color': '#edf4f7', 'color': 'black',
             'num_format': '#,##0.00'})
        format3_left = workbook.add_format({'font_size': 14, 'align': 'left', 'bold': False, 'num_format': '#,##0.00'})
        format3_left.set_bottom()
        format3 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': False, 'num_format': '#,##0.00'})
        format3.set_bottom()

        format3_colored = workbook.add_format(
            {'font_size': 11, 'align': 'vcenter', 'bg_color': '#f7fcff', 'bold': False, 'num_format': '#,##0.00'})
        format4 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format5 = workbook.add_format({'font_size': 13, 'align': 'vcenter', 'bold': False})
        # sheet = workbook.add_worksheet('Payslip Reportss')

        # Fetch available salary rules:
        used_structures = []
        for sal_structure in lines.slip_ids.struct_id:
            if sal_structure.id not in used_structures:
                used_structures.append([sal_structure.id, sal_structure.name])
        used_addresses = []
        for rec in lines.slip_ids:
            if rec.employee_id.address_id.id not in used_addresses:
                used_addresses.append(rec.employee_id.address_id.id)
        # Logic for each workbook, i.e. group payslips of each salary structure into a separate sheet:
        # print(used_addresses)
        struct_count = 1
        for used_address in used_addresses:
            # Generate Workbook
            address = self.env['res.partner'].browse([used_address])
            sheet = workbook.add_worksheet(str(struct_count) + ' - ' + str(address.name))
            cols = list(string.ascii_uppercase) + ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK',
                                                   'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV',
                                                   'AW', 'AX', 'AY', 'AZ']
            rules = []
            col_no = 2
            # Fetch available salary rules:
            for item in lines.slip_ids.struct_id.rule_ids:
                # if item.employee_id.address_id.id == address.id:
                col_title = ''
                row = [None, None, None, None, None]
                row[0] = col_no
                row[1] = item.code
                row[2] = item.name
                col_title = str(cols[col_no]) + ':' + str(cols[col_no])
                row[3] = col_title
                if len(item.name) < 8:
                    row[4] = 12
                else:
                    row[4] = len(item.name) + 2
                if row[1] not in ['BASIC', 'OC', 'ADS']:
                    rules.append(row)
                    col_no += 1

            # Report Details:
            company_name = ''
            batch_period = ''
            for item in lines.slip_ids:
                if item.employee_id.address_id.id == address.id:
                    batch_period = str(item.date_from.strftime('%B %d, %Y')) + '  To  ' + str(
                        item.date_to.strftime('%B %d, %Y'))
                    company_name = item.company_id.name
                    break
            # Company Name
            sheet.write(0, 0, company_name, format4)

            sheet.write(0, 2, 'Payslip Period:', format4)
            sheet.write(0, 3, batch_period, format4)

            sheet.write(1, 2, 'Work Address:', format4)
            sheet.write(1, 3, address.name, format4)

            # List report column headers:
            sheet.write(2, 0, 'Employee Name', format_left)
            sheet.write(2, 1, 'Department', format_left)
            sheet.write(2, 2, 'Gross Salary', format1)
            sheet.write(2, 3, 'Old Advance', format1)
            sheet.write(2, 4, 'Current Advance', format1)
            sheet.write(2, 5, 'Abs Days', format1)
            sheet.write(2, 6, 'Days Deduction', format1)
            sheet.write(2, 7, 'Old Deduction', format1)
            sheet.write(2, 8, 'Current Deduction', format1)
            sheet.write(2, 9, 'Total Deduction', format1)
            sheet.write(2, 10, 'Net Salary', format1)
            # for rule in rules:
            #     sheet.write(2, rule[0]+5, rule[2], format1)

            # Generate names, dept, and salary items:
            x = 3
            e_name = 3
            has_payslips = False
            emp_list = []
            for em in lines:
                for ei in em.slip_ids:
                    if ei.employee_id.id not in emp_list:
                        emp_list.append(ei.employee_id.id)
            for res in emp_list:
                br_emp = self.env['hr.employee'].browse([res])
                sheet.write(e_name, 0, br_emp.name, format3_left)
                sheet.write(e_name, 1, br_emp.department_id.name, format3_left)

                for l in lines:
                    for slip in l.slip_ids:
                        if slip.employee_id.id == res and slip.employee_id.address_id.id == address.id:
                            has_payslips = True
                            sheet.write(x, 2, slip.net_wage_basic, format3)
                            sheet.write(x, 3, slip.balance, format3)
                            sheet.write(x, 4, slip.current_balance, format3)
                            sheet.write(x, 5, slip.meal_allowance, format3)
                            sheet.write(x, 6, slip.days_dec, format3)
                            sheet.write(x, 7, slip.conveyance, format3)
                            sheet.write(x, 8, slip.mobile_allowance, format3)
                            sheet.write(x, 9, slip.total_deductions, format3)
                            sheet.write(x, 10, slip.net_wage_total, format3)
                            # for line in slip.line_ids:
                            #     for rule in rules:
                            #         if line.code == rule[1]:
                            #             if line.amount > 0:
                            #                 sheet.write(x, rule[0]+5, line.amount, format3_colored)
                            #             else:
                            #                 sheet.write(x, rule[0]+5, line.amount, format3)

                            x += 1
                            e_name += 1
            # sheet.set_border()
            # for slip in lines.slip_ids:
            #     # if lines.slip_ids:
            #     if slip.employee_id.address_id.id == address.id:
            #         has_payslips = True
            #         sheet.write(e_name, 0, slip.employee_id.name, format3)
            #         sheet.write(e_name, 1, slip.employee_id.department_id.name, format3)
            #         for line in slip.line_ids:
            #             for rule in rules:
            #                 if line.code == rule[1]:
            #                     if line.amount > 0:
            #                         sheet.write(x, rule[0], line.amount, format3_colored)
            #                     else:
            #                         sheet.write(x, rule[0], line.amount, format3)
            #         x += 1
            #         e_name += 1
            # Generate summission row at report end:

            sum_x = e_name
            if has_payslips == True:
                sheet.write(sum_x, 0, 'Total', format2)
                sheet.write(sum_x, 1, '', format2)
                for i in range(2, col_no+4):
                    sum_start = cols[i] + '3'
                    sum_end = cols[i] + str(sum_x)
                    sum_range = '{=SUM(' + str(sum_start) + ':' + sum_end + ')}'
                    # print(sum_range)
                    sheet.write_formula(sum_x, i, sum_range, format2)
                    i += 1

            # set width and height of colmns & rows:
            sheet.set_column('A:A', 36)
            sheet.set_column('B:B', 22)
            for rule in rules:
                sheet.set_column(rule[3], rule[4])
            sheet.set_column('C:C', 27)
            sheet.set_column('H:H', 17)
            sheet.set_column('G:G', 19)
            sheet.set_column('I:I', 20)
            sheet.set_column('J:J', 19)
            sheet.set_column('K:K', 17)
            struct_count += 1
