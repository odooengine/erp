from odoo import models, api
from datetime import timedelta, datetime
from itertools import groupby


class EmpReport(models.AbstractModel):
    _name = 'report.hr_attendance_report.attendance_report_id_print'
    _description = 'Attendance Report'

    def get_days(self, result):
        delta = result.date_to - result.date_from  # returns timedelta
        # print('days', delta.days)
        days = []
        for i in range(delta.days+1):
            diff = result.date_from + timedelta(days=i)
            days.append([diff.day, diff.strftime('%a'), diff])
        return days

    @api.model
    def _get_report_values(self, docids, data=None):
        result = self.env['attendance.report'].browse(self.env.context.get('active_ids'))
        # print(result.department_id.name)
        d = self.env['user.attendance'].search([])
        for x in d:
            x.address_id = x.employee_id.address_id
            x.department_id = x.employee_id.department_id.id
        # data = self.env['hr.attendance'].search([('employee_id.address_id', '=', result.word_address_id.id)])
        data = self.env['user.attendance'].search([('employee_id.address_id', '=', result.word_address_id.id)]).sorted(key=lambda r: r.timestamp)
        days = []
        week_days = []
        emp = []
        for rec in data:
            # if rec.timestamp.date() >= result.date_from and rec.timestamp.date() <= result.date_to:
            #     days.append(rec.timestamp.date().day)
            #     week_days.append(rec.timestamp.strftime('%A'))
            emp.append(rec.employee_id.id)
        # print(data.mapped('timestamp')[0].date().day)
        # print(len(days))
        # up_days = [key for key, _group in groupby(days)]
        # up_week = [key for key, _group in groupby(week_days)]
        emp = list(dict.fromkeys(emp))

        up_days = self.get_days(result)
        # print(up_week)
        employees = self.env['hr.employee'].browse(emp)
        return {
            'doc_ids': docids,
            'doc_model': 'attendance.report',
            'date_wizard': result,
            'data': data,
            'employees': employees,
            'departments': data.mapped('department_id'),
            'days': up_days,
            'cols': len(up_days)+6,
            # 'get_attendance': self.get_attendance(day),
        }
