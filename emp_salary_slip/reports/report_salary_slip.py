from odoo import models,fields,_
from datetime import  date, datetime, timedelta
from os.path import abspath,dirname
class EmplyoeePayrollReport(models.AbstractModel):
    _name = 'report.emp_salary_slip.emp_payroll_report' 
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, lines):
        print("lines", lines)
        format1 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': True, 'bg_color':'#d3dde3', 'color':'black', 'bottom': True, })
        format2 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': True, 'bg_color':'#edf4f7', 'color':'black','num_format': '#,##0.00'})
        format3 = workbook.add_format({'font_size':11, 'align': 'vcenter', 'bold': False, 'num_format': '#,##0.00'})
        format3_colored = workbook.add_format({'font_size':11, 'align': 'vcenter', 'bg_color':'#f7fcff', 'bold': False, 'num_format': '#,##0.00'})
        format4 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': True})
        format5 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': False})
        sheet = workbook.add_worksheet('Salary Slip Report')
     
        format004 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': True,})
        format04 = workbook.add_format({'font_size':12, 'align': 'right', 'bold': True ,'top':True, 'bg_color':'#b2b2b2'})
        format5 = workbook.add_format({'font_size':12, 'align': 'vcenter', 'bold': False})
        format05 = workbook.add_format({'font_size':12, 'align': 'right', 'bold': False})
        format6 = workbook.add_format({'font_size':11, 'align': 'vcenter', 'bold': False})
        format61 = workbook.add_format({'font_size':11, 'bold': False ,'text_wrap': True,'align':'right'})
        main_head = workbook.add_format({'font_size':11, 'align': 'left', 'bold': True,})
        main_head1 = workbook.add_format({'font_size':11, 'align': 'left', 'bold': True, 'right':True ,'bottom':True ,'top':True,'left':True})
        main_head_data = workbook.add_format({'font_size':11, 'align': 'left', 'bold': False,})
        format_01 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14})
        format_010 = workbook.add_format({'bold': True, 'align': 'right', 'font_size': 14})
        format_border_top= workbook.add_format({'font_size':11, 'align': 'left', 'bold': True , 'top':True, 'left':True})
        format_1111= workbook.add_format({'font_size':11, 'align': 'right', 'bold': False ,'num_format': '#,##0.00'})
        
        format_1111_bold= workbook.add_format({'font_size':11, 'align': 'right', 'bold': True ,'num_format': '#,##0.00'})
        format_1111_b= workbook.add_format({'font_size':11, 'align': 'right', 'bold': False ,'num_format': '#,##0.00','right':True})
        format_1111_br= workbook.add_format({'font_size':11, 'align': 'right', 'bold': True ,'num_format': '#,##0.00','right':True ,'bottom':True ,'top':True,'left':True})
        format_01111= workbook.add_format({'font_size':11, 'align': 'left', 'bold': False ,})
        format_01111_for_brd= workbook.add_format({'font_size':11, 'align': 'left', 'bold': False ,'left':True})
        format_border_top_right= workbook.add_format({'font_size':11, 'align': 'left', 'bold': True ,'top':True,'right':True})
#         sheet.merge_range(0, 0, 0, 3, record.company_id.name, format_01)
        sheet.set_column('A:A',20)
        sheet.set_column('B:B',19)
        sheet.set_column('D:D',20)
        sheet.set_column('E:E',19)
        row =2
        for rec in lines:
#             sheet.write('A3','SMC GROUP' , main_head)
            sheet.write(f'A{row+1}','SMC GROUP' , main_head)
#             row+=1
#             sheet.merge_range('A4:C4',lines[0].company_id.street, main_head )
            sheet.merge_range(f'A{row+2}:C{row+2}',rec.company_id.street, main_head )
            pt=abspath(dirname(dirname(dirname(__file__))))+'/emp_salary_slip/static/description/icon.png'
                
#             sheet.insert_image('D3', pt, {'x_scale': 1, 'y_scale': 0.9})
            sheet.insert_image(f'D{row+1}', pt, {'x_scale': 1, 'y_scale': 0.9})
            row+=4
#             sheet.write('A6' ,lines[0].date_from.strftime("%b'%Y"), main_head)
            sheet.write(f'A{row}' ,rec.date_from.strftime("%b'%Y"), main_head)
#             sheet.merge_range('B6:C6','Pay Slip Details' ,main_head)
            sheet.merge_range(f'B{row}:C{row}','Pay Slip Details' ,main_head)
#         row = 8
#         for rec in lines:
            row += 2
            
            col =0
            sheet.write(row, col, 'Name:', main_head)
            sheet.merge_range(row,col+1,row,col+2, rec.employee_id.name, main_head_data)
            row +=1
            col=0
            sheet.write(row, col, 'Designation: ', main_head)
            sheet.merge_range(row,col+1,row,col+2, rec.employee_id.job_title, main_head_data)
            row +=1
            col=0
            sheet.write(row, col, 'Email: ', main_head)
            sheet.merge_range(row,col+1,row,col+2, rec.employee_id.work_email, main_head_data)
         
            
            row +=2
            col = 0
            sheet.write(row, col, 'Salary:', format_border_top)
            sheet.write(row, col+1, 'RS. ', format_border_top_right)
            
#             sheet.write(row, col+3, 'Deduction:', format_border_top)
#             sheet.write(row, col+4, 'RS. ', format_border_top_right)
#             
            
            
            
            
            #static
    #         sheet.write(8, 0, 'Name:', main_head)
    #         sheet.write(9, 0, 'Designation: ', main_head)
    #         sheet.write(10, 0, 'Email: ', main_head)
    #         
    #         sheet.merge_range(8,1,8,2, lines.employee_id.name, main_head_data)
    #         sheet.merge_range(9, 1,9,2, lines.employee_id.job_title, main_head_data)
    #         sheet.merge_range(10, 1,10,2, lines.employee_id.work_email, main_head_data)
    #         
    #         
    #         sheet.write(12, 0, 'Salary:', format_border_top)
    #         sheet.write(12, 1, 'RS. ', format_border_top_right)
    #         
    #         sheet.write(12, 3, 'Deduction:', format_border_top)
    #         sheet.write(12, 4, 'RS. ', format_border_top_right)
            #static
            row +=1
            col=0
            if rec.line_ids:
                other_lines = {}
                deduction_lines = rec.line_ids.filtered(lambda r:r.category_id.name =='Deduction')
                salary_lines = rec.line_ids.filtered(lambda r:r.category_id.name =='Basic')
                other_lines[salary_lines.name] =salary_lines.total
                other_lines['House Rent'] = 0.0
                other_lines['Utility Allowance'] = 0.0
                other_lines['Conveyance Allowance'] = 0.0
                other_lines['Medical'] = 0.0
#                 other_lines  = rec.line_ids - deduction_lines
                o_line_total = 0.0
                deduct_line_total =0.0
                
    
                
                st_row= row
                for ol in other_lines:
                    sheet.write(row,col,ol,format_01111_for_brd)
                    col +=1
                    sheet.write(row,col,other_lines[ol],format_1111_b)
                    o_line_total += other_lines[ol]
                    col=0
                    row +=1
                
                ol_last_row = row
                     

                row = st_row
                col=3
#                 deduction_lines = deduction_lines.sorted(key = 'total',reverse=True)    
#                 for dl in deduction_lines:
#                     if dl.total >0.00:
#                         sheet.write(row,col,dl.name,format_01111_for_brd)
#                         col +=1
#                         sheet.write(row,col,dl.total,format_1111_b)
#                         deduct_line_total += dl.total
#                         col=3
#                         row +=1 
#                     else:
#                         sheet.write(row,col,'',format_01111_for_brd)
#                         col +=1
#                         sheet.write(row,col,'',format_1111_b)
#                         col=3
#                         row +=1 
#                         continue 
    #             col=3    
    #             sheet.write(row,col,'Total' ,main_head)
    #             col+=1
    #             sheet.write(row,col,deduct_line_total ,format_1111)      
                dl_last_row = row
                
                row  = max(ol_last_row,dl_last_row)
                col = 0
                sheet.write(row,col,'Total' ,main_head1)
                col+=1
                sheet.write(row,col,o_line_total ,format_1111_br)     
                
#                 col=3    
#                 sheet.write(row,col,'Total' ,main_head1)
#                 col+=1
#                 sheet.write(row,col,deduct_line_total ,format_1111_br)    
#                 
                
                row +=3
                col=0  
#                 sheet.write(row,col,'Salary',format_01111)
#                 sheet.write(row,col+1,o_line_total,format_1111)
#                 row +=1
#                 sheet.write(row,col,'Deduction',format_01111)
#                 sheet.write(row,col+1,f'({deduct_line_total})',format_1111) 
#                 row +=1
                sheet.write(row,col,'Net Income' ,main_head1)
#                 net_sal =  o_line_total - deduct_line_total
                net_sal =  o_line_total
                sheet.write(row,col+1,net_sal,format_1111_br)
            
            row +=5
            
            
            
            
            
            