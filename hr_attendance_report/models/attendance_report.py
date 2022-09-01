import datetime

from odoo import fields, models
from pytz import timezone


class AttendanceReport(models.TransientModel):
    _name = "attendance.report"
    _description = "Attendance Report"

    word_address_id = fields.Many2one('res.partner', string='Work Address')
    date_from = fields.Date()
    date_to = fields.Date()

    def report_pdf_print(self):
        print("click")
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('hr_attendance_report.attendance_report_pdf').report_action(self, data=data)

    # def get_attendance(self, d, emp):
        # # data = self.env['hr.attendance'].search([('employee_id', '=', emp.id)]).sorted(key=lambda r: r.timestamp)
        # data = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
        # boool = 'A'
        # if not data and d[1] == 'Sun':
        #     boool = '-'
        #
        # for rec in data:
        #
        #     if d[2] <= datetime.datetime.today().date() and d[1] != 'Sun':
        #         if rec.check_in.date() == d[2]:
        #             if rec.employee_id.shift_id:
        #                 if rec.check_in:
        #                     shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
        #                     shift_in = (datetime.datetime.min + shift_in).time()
        #                     check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
        #                     if check_in:
        #                         boool = 'P'
        #                     if check_in > shift_in:
        #                         boool = 'L'
        #                 if rec.check_out:
        #                     shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
        #                     shift_out = (datetime.datetime.min + shift_out).time()
        #                     check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
        #                     if shift_out:
        #                         boool = 'P'
        #                     if check_out < shift_out:
        #                         boool = 'E'
        #                 if rec.check_in and rec.check_out:
        #                     shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
        #                     shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
        #                     shift_in = (datetime.datetime.min + shift_in).time()
        #                     shift_out = (datetime.datetime.min + shift_out).time()
        #                     check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
        #                     check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
        #                     if check_in > shift_in and check_out < shift_out:
        #                         boool = 'LE'
        #     else:
        #         boool = ' - '
        # return boool

    def action_reset(self, emp):
        emp.late_in = 0
        emp.late_out = 0
        emp.st = 0
        emp.ot = 0
        return True

    def get_overtime(self, emp):
        time = (emp.st*9) - emp.ot
        if time < 0:
            return abs(time)
        else:
            return 0

    def get_public_holiday(self, date):
        print('hhh')
        leaves = self.env['public.holidays'].search([])
        print(leaves)
        check = False
        for leave in leaves:
            if date[2] >= leave.date_from and date[2] <= leave.date_to and date[1] != 'Sun':
                check = True
        return check

    def get_attendance(self, d, emp):
        data = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
        # data = self.env['hr.attendance'].search([('employee_id', '=', 25)])
        print(d)
        boool = 'A'
        if not data and d[1] == 'Sun':
            boool = '-'
        holiday = self.get_public_holiday(d)
        if not holiday:
            for rec in data:
                if d[2] <= datetime.datetime.today().date() and d[1] != 'Sun':
                    if rec.check_in.date() == d[2]:
                        if rec.employee_id.shift_id:
                            if rec.check_in and rec.check_out:
                                shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
                                shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
                                shift_in = shift_in + datetime.timedelta(minutes=20)
                                shift_in = (datetime.datetime.min + shift_in).time()
                                shift_out = (datetime.datetime.min + shift_out).time()
                                check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
                                check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
                                if check_in and check_out:
                                    if check_in > shift_in:
                                        rec.employee_id.late_in = rec.employee_id.late_in + 1
                                    if check_in > shift_in and check_out < shift_out:
                                        boool = 'P'
                                        # rec.employee_id.late_in = rec.employee_id.late_in + 1
                                t = (rec.check_out - rec.check_in).total_seconds()/3600
                                rec.employee_id.ot = rec.employee_id.ot + t
                                if emp.id == 25:
                                    print(check_in)
                                    print(rec.employee_id.late_in)
                            if rec.check_in and not rec.check_out:
                                shift_in = datetime.timedelta(hours=rec.employee_id.shift_id.check_in)
                                shift_in = shift_in + datetime.timedelta(minutes=20)
                                shift_in = (datetime.datetime.min + shift_in).time()
                                check_in = rec.check_in.astimezone(timezone('Asia/Karachi')).time()
                                boool = 'P'
                                if check_in > shift_in:
                                    rec.employee_id.late_in = rec.employee_id.late_in + 1
                                if emp.id == 25:
                                    print(check_in)
                                    print(rec.employee_id.late_in)
                            if rec.check_out:
                                shift_out = datetime.timedelta(hours=rec.employee_id.shift_id.check_out)
                                shift_out = (datetime.datetime.min + shift_out).time()
                                check_out = rec.check_out.astimezone(timezone('Asia/Karachi')).time()
                                boool = 'P'
                                if check_out > shift_out:
                                    rec.employee_id.late_out = rec.employee_id.late_out + 1

                else:
                    boool = ' - '
            if boool == 'P':
                emp.st = emp.st + 1

            if boool == 'A':
                check = self.get_time_off(emp, d)
                if check:
                    boool = 'L'
        else:
            boool = 'H'
        return boool

    def get_time_off(self, emp, d):
        # print(d)
        timeoff = self.env['hr.leave'].search([('employee_id', '=', emp.id)])
        print(d[2])
        check = False
        for rec in timeoff:
            if d[2] >= rec.request_date_from and d[2] <= rec.request_date_to:
                check = True
        return check
