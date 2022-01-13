from odoo import models, fields, api,_



class POProductReport(models.AbstractModel):
    _name = 'report.report_product_purchase.po_product_report'
    
    def getKey(self , size_dict):
        return list(size_dict.keys())[0]
    
    
    def getmatched_colVal(self, col,val_size):
        for a in val_size:
            dict_key = list(a.keys())[0]
            if dict_key == col:
                    return a[dict_key]
               
        return 'no match' 
    
    
    
    def getSizeColorValue(self,product_id,qty):
        color_data={}
        size_val ={}
        size_data =[]
        for ptav in product_id.product_template_attribute_value_ids:
           
            if ptav.attribute_id.name.lower() == 'size':
                size_val={ptav.name : qty}
                size_data.append({ ptav.name : qty})
    
            elif ptav.attribute_id.name.lower() == 'color': 
                color_data={'color':ptav.name }
    
        return size_data,color_data 
    
    @api.model
    def _get_report_values(self, docids, data=None):

        po_record = self.env["purchase.order"].search([("id","in",docids)])
        size_attrib = self.env['product.attribute'].search([])
#         po_record.order_line.product_id.product_template_attribute_value_ids.filtered(lambda r:(r.attribute_id.name).lower() == 'size' )

        for rec in size_attrib:
            if rec.name.lower()== 'size':
                size_attrib = rec 
        if size_attrib:
            size_values= size_attrib.value_ids
            sv_names = size_values.mapped('name')
        if po_record.order_line:
           
            
            color_obj = po_record.order_line.product_id.product_template_attribute_value_ids.filtered(lambda r:(r.attribute_id.name).lower() == 'color' )  
            color_list = color_obj.mapped('name')
#           
        
      
        
        
        val=[]
        qnti=0.0;
        size_lst = []
        prd_tmpl = ''
        for line in po_record.order_line:
            update_flag=False
            prd_tmpl=line.product_id.product_tmpl_id
            
            for item in val:
                if item['prod_tmpl']==prd_tmpl:
                    if line.product_id.product_template_attribute_value_ids:
                        for ptav in line.product_id.product_template_attribute_value_ids:
                            if ptav.attribute_id.name.lower() == 'color' and  item['color'] ==  ptav.name:
                                s_val= line.product_id.product_template_attribute_value_ids.filtered(lambda q:q.attribute_id.name.lower() == 'size')
                                item['size'].append({ s_val.name:line.product_qty })
                                item['price'] += line.price_unit
                                update_flag = True
                        continue 
            else:
                if update_flag == False:
                    data_dict={}
                    data_dict ={
                        'prod_tmpl':line.product_id.product_tmpl_id,
                        'product_id':line.product_id,
                        'price':line.price_unit,
                        }
                    size,color =self.getSizeColorValue(line.product_id, line.product_qty)    
                    if line.product_id.product_template_attribute_value_ids:
                        for ptav in line.product_id.product_template_attribute_value_ids:
                            if ptav.attribute_id.name.lower() == 'size':
                                size_dict={}
                                size_data =[]
                                size_data.append({ ptav.name : line.product_qty,})
        #                             val['size'] = ptav.name
                                data_dict['size']=size_data
                            elif ptav.attribute_id.name.lower() == 'color':
                                data_dict['color'] = ptav.name 
        
        
                    val.append(data_dict)
        return {
                'po_record':po_record,
                'size_colspan': len(size_values)+1,
                'size_values':size_values,
                'sv_names':size_values.mapped('name'),
                'color_list':color_list,
                'val':val,
                'get_key':self.getKey,
                 'getmatched_colVal':self.getmatched_colVal
                }
        