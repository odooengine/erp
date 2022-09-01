from odoo import models, api
from datetime import timedelta, datetime


class EmpReport(models.AbstractModel):
    _name = 'report.hr_report_bonus.bonus_report_id_print'
    _description = 'Bonus Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        result = self.env['bonus.report'].browse(self.env.context.get('active_ids'))
        # print(result.department_id.name)
        data = self.env['hr.contract'].search([('employee_id.address_id', '=', result.word_address_id.id),('state' ,'=','open')])
        print(data)
        return {
            'doc_ids': docids,
            'doc_model': 'bonus.report',
            'date_wizard': result,
            'data': data,
        }

    # hr.contract(75, 76, 77, 78, 79, 80, 180, 190, 198)

