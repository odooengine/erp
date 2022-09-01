from dateutil.relativedelta import relativedelta

from odoo import models, api
from datetime import date
from datetime import timedelta, datetime


class LocalReport(models.AbstractModel):
    _name = 'report.local_purchase_report.test_report_id_print'
    _description = 'Local Purchase Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('Local Purchase Report')
        resul = self.env['local.purchase'].browse(self.env.context.get('active_ids'))
        record = self.env['purchase.order'].search([('order_line.product_id', '=', resul.product_id.id)] , limit=1)
        rec = self.env['sale.order'].search([('order_line.product_id', '=', resul.product_id.id)] , limit=1)
        print(record)
        print(resul.product_id.product_tmpl_id.article_no)
        print(rec)
        result = []
        res = []
        for r in record.order_line:
            if r.article_no == resul.product_id.product_tmpl_id.article_no:
                result.append(r)
        print(result)
        for i in rec.order_line:
            if i.article_no == resul.product_id.product_tmpl_id.article_no:
                res.append(i)
        print(res)
        return {
            'doc_ids': docids,
            'doc_model': 'local.purchase',
            'record': record,
            'rec': rec,
            'result': result,
            'res': res,
        }