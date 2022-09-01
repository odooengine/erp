import xlsxwriter

from odoo import models

from datetime import date, datetime, time,timedelta

from os.path import abspath,dirname



class SmcInvoiceXlsx(models.AbstractModel):
    _name = 'report.invoice_report_xlsx.report_smc_invoice_xlsx_doc'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, record):
#         workbook = xlsxwriter.Workbook("file.xlsx")
        sheet = workbook.add_worksheet('Invoice Xlsx Report') 
        format0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format1 = workbook.add_format({'font_size': 16, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 14, 'align': 'vcenter', })
        format3 = workbook.add_format({'font_size': 14, 'align': 'center', })
        format4 = workbook.add_format({'font_size': 14, 'align': 'center',  'bold': True})
        format_header = workbook.add_format({'font_size': 15, 'align': 'vcenter',  'bold': True})
        format_header1 = workbook.add_format({'font_size': 15, 'align': 'vcenter',  'bold': False})
        sub_header = workbook.add_format({'font_size': 12, 'align': 'right',  'bold': True ,'valign':'vcenter'})
        sub_sub_header = workbook.add_format({'font_size': 12, 'align': 'center',  'bold': True ,'valign':'vcenter','left':True,'right':True,'bottom':True,'top':True})
        
        li_total = workbook.add_format({'font_size': 12, 'align': 'right',  'bold': True ,'valign':'vcenter','left':True,'right':True,'bottom':True,'top':True})
        
        format_td = workbook.add_format({'font_size': 12, 'align': 'center', 'num_format':'#,##0.00', 'bold': False ,'valign':'vcenter','left':True,'right':True,'bottom':True,'top':True})
        format_td_wrap = workbook.add_format({'text_wrap': True ,'font_size': 12, 'align': 'center', 'num_format':'#,##0.00', 'bold': False ,'valign':'vcenter','left':True,'right':True,'bottom':True,'top':True})
        format_td_num = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format':'#,##0.00', 'bold': False ,'valign':'vcenter','left':True,'right':True,'bottom':True,'top':True})
        format_td_num1 =  workbook.add_format({'font_size': 12, 'align': 'right', 'num_format':'#,##0.00', 'bold': False ,'valign':'vcenter',})

        
        sub_header_wrap = workbook.add_format({'font_size': 12, 'align': 'right',  'bold': True,'text_wrap': True ,})
        sub_header_data = workbook.add_format({'font_size': 12, 'align': 'left',  'bold': False ,'valign':'vcenter'})
        sub_header_data_wrap = workbook.add_format({'font_size': 12, 'align': 'left',  'bold': False, 'text_wrap': True})
        format_032 = workbook.add_format({'font_size': 12, 'align': 'left',  'bold': True, 'top': True})
        format_0321 = workbook.add_format({'font_size': 12, 'align': 'left',  'bold': True})
        main_header = workbook.add_format({'font_size': 15, 'align': 'vcenter',  'bold': True})
#         sub_header_data.num_format('#,##0.00')
#         sheet = workbook.add_worksheet('Invoice Xlsx Report')
        image_row = 0
        image_col = 0
        h_row =2
        h_row_add =2
        for rec in record: 
            pt=abspath(dirname(dirname(dirname(__file__))))+'/invoice_report_xlsx/static/description/sm_icon.png'
            
            sheet.insert_image(image_row,image_col, pt, {'x_scale': 0.51, 'y_scale': 0.6})
            
            sheet.merge_range(f'F{h_row}:K{h_row}', 'SHAHID MAHMOOD & CO. (PVT) LTD.',format_header)
            sheet.merge_range(f'F{h_row +h_row_add}:N{h_row +h_row_add+1}', 'Head Office: E-110, Main Boulevard, D.H.A, Lahore-54792',format_header)
            sheet.merge_range(f'F{h_row +h_row_add +2}:L{h_row +h_row_add +3}', 'info@smcgroup.pk Customer Services:',format_header1)
            
            
#             image_row =h_row_add+ h_row +5
            h_row =h_row +9 
#             h_row_add =13
            
            
            sheet.merge_range(f'G{h_row}:H{h_row +1}', 'INVOICE',main_header)
            
            h_row +=3
            
            
            
            
            sheet.set_column('A:A',18)
            sheet.set_column('B:B',22)
            sheet.set_column('H:H',12)
            sheet.set_column('G:G',12)
            sheet.set_column('I:I',12)
            sheet.set_column('J:J',12)
            
            sheet.write(f'A{h_row}', 'Invoice No. :',sub_header)
            sheet.write(f'B{h_row}', rec.name,sub_header_data)
            sheet.write(f'G{h_row}', 'Branch :',sub_header)
            sheet.merge_range(f'H{h_row}:I{h_row}', rec.create_user.branch_id.name,sub_header_data)
            h_row += 1
            
            sheet.set_row(h_row,30)
            sheet.write(f'A{h_row}',' Invoice Date :',sub_header)
            sheet.write(f'B{h_row}', rec.invoice_date.strftime('%d/%m/%Y'), sub_header_data)
            h_row += 1
            
#             sheet.write(f'{A16', 'Customer:',sub_header)
            sheet.set_row(h_row,22)
            sheet.write(f'A{h_row}', 'Customer:',sub_header)
            sheet.merge_range(f'B{h_row}:E{h_row}', rec.partner_id.name,sub_header_data_wrap)
            sheet.write(f'G{h_row}', 'Printed on :',sub_header) 
            
            current_dateTime = (datetime.now() + timedelta(hours =5)).strftime('%d/%m/%Y %H:%M:%S')
            sheet.merge_range(f'H{h_row}:I{h_row}', current_dateTime,sub_header_data)
            h_row += 1
            
            
            
            sheet.write(f'A{h_row}','Shipping Address:',sub_header)
            sheet.merge_range(f'B{h_row}:E{h_row}', rec.partner_id.street ,sub_header_data)
            sheet.set_row(h_row,22)
            sheet.write(f'G{h_row}', 'User :',sub_header) 
            sheet.merge_range(f'H{h_row}:I{h_row}', rec.user_id.name,sub_header_data)
            h_row += 1
            
            
            
            sheet.write(f'A{h_row}', 'Detail :',sub_header)
            sheet.write(f'B{h_row}', rec.freight ,sub_header_data)
            h_row += 1
            
            
            sheet.write(f'A{h_row}', 'Do # :',sub_header)
            sheet.write(f'B{h_row}', rec.delivery_order.name ,sub_header_data)
            h_row += 1
            
            
            sheet.write(f'A{h_row}', 'CNIC # :',sub_header)
            sheet.write(f'B{h_row}', rec.partner_id.no_cnic ,sub_header_data)
            h_row += 1
            
            
            sheet.write(f'A{h_row}', 'NTN # :',sub_header)
            sheet.write(f'B{h_row}', rec.partner_id.ntn ,sub_header_data)
            
            h_row += 1
            sheet.write(f'A{h_row}' ,'Sr', sub_sub_header)
#             sheet.set_row(h_row,22)
            sheet.write(f'B{h_row}' ,'Item Description', sub_sub_header)
            sheet.write(f'C{h_row}' ,'Article', sub_sub_header)
            sheet.write(f'D{h_row}' ,'Finish', sub_sub_header)
            sheet.write(f'E{h_row}' ,'Unit', sub_sub_header)
            sheet.write(f'F{h_row}' ,'Qty', sub_sub_header)
            sheet.write(f'G{h_row}' ,'Rate', sub_sub_header)
            sheet.write(f'H{h_row}' ,'Disc%', sub_sub_header)
            sheet.write(f'I{h_row}' ,'Amount', sub_sub_header)
            sheet.write(f'J{h_row}' ,'Net Amt', sub_sub_header)
            h_row +=1
            
            col =0
            total_gross =0.0
            tot_lines_qty=0.0
            
            total_amount = 0.0
            total_net_amount= 0.0
            total_discount_amount=0.0
            sr=1
            for line in rec.invoice_line_ids:
                total_gross = total_gross + (line.price_unit * line.quantity)
                col =0
                
                sheet.write(h_row ,col , sr ,format_td)
                sr +=1
                col +=1
                
                
                sheet.set_row(h_row , 30)
                sheet.write(h_row ,col , line.product_id.name ,format_td_wrap)
                col +=1
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.product_id.article_no ,format_td)
                 
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.product_id.finish_no ,format_td)
                 
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.product_uom_id.name ,format_td)
                 
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.quantity,format_td)
                    tot_lines_qty += line.quantity
                    
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.price_unit,format_td)
                 
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                
                if line.product_id.type != 'service':
                    sheet.write(h_row ,col , line.discount,format_td)
                    total_discount_amount = (total_discount_amount + ((line.discount * (line.price_unit * line.quantity))/100))
                 
                elif not line.product_id.type != 'service': 
                    sheet.write(h_row ,col ,'',format_td)  
                col +=1
                
                line_amount = line.price_unit * line.quantity
                sheet.write(h_row ,col , line_amount, format_td_num)
                total_amount += line_amount
                
                
                col +=1
                
                
                sheet.write(h_row ,col , line.price_subtotal, format_td_num)
                total_net_amount += line.price_subtotal
                col +=1
                h_row += 1
                
            h_row += 1
            col =5
                
            sheet.merge_range(f'A{h_row}:E{h_row}','Total:',li_total )
            sheet.write(h_row-1 ,col,tot_lines_qty , format_td)
            col += 1
            
            sheet.write(h_row-1 ,col,' ' , format_td)
            col += 1
            sheet.write(h_row-1 ,col,'' , format_td)
            col += 1
            sheet.write(h_row-1 ,col,total_amount , format_td_num)
            col += 1
            sheet.write(h_row-1 ,col,total_net_amount , format_td_num)
            col += 1
            
             
            h_row += 3   
            sheet.merge_range(f'G{h_row}:H{h_row}','Gross Total:',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',total_gross , format_td_num1)
            h_row += 1
         
            sheet.merge_range(f'G{h_row}:H{h_row}','Discount:',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',total_discount_amount , format_td_num1)
            h_row += 1
            
            
            sheet.merge_range(f'G{h_row}:H{h_row}','Net Payable:',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',rec.amount_untaxed , format_td_num1)
            h_row += 1 
            
            
            sheet.merge_range(f'G{h_row}:H{h_row}','Tax 17.0 % :',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',rec.amount_tax , format_td_num1)
            h_row += 1 
            
            
            sheet.merge_range(f'G{h_row}:H{h_row}','Sec Dicount :',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',rec.second_discount , format_td_num1)
            h_row += 1
            
            
            sheet.merge_range(f'G{h_row}:H{h_row}','Balance:',sub_header )    
            sheet.merge_range(f'I{h_row}:J{h_row}',rec.amount_total , format_td_num1)
            h_row += 3 
            
            
            sheet.merge_range(f'A{h_row}:B{h_row}','Terms and Conditions:',sub_header ) 
            
            h_row += 1
            sheet.merge_range(f'A{h_row}:H{h_row+10}',rec.narration , sub_header_data)
            
            h_row += 12
            sheet.merge_range(f'A{h_row}:B{h_row}',rec.invoice_user_id.name , sub_header_data)
            h_row += 1
            
            sheet.merge_range(f'A{h_row}:B{h_row}',rec.invoice_user_id.email , format_032) 
            sheet.merge_range(f'D{h_row}:F{h_row}','Manager' , format_032) 
            sheet.merge_range(f'H{h_row}:J{h_row}','Customer' , format_032) 
            h_row += 1
            
            sheet.merge_range(f'A{h_row}:B{h_row}',rec.invoice_user_id.phone , format_0321)
              
            h_row += 4
            image_row = h_row -1
            
            
            
            
#             sheet.write('A19',' Do # :',sub_header)
#             sheet.write('A20', 'CNIC # :',sub_header)
#             sheet.write('A20', 'NTN # :',sub_header)
            
            
            
#             sheet.write('B14', rec.name, sub_header_data)
            
        