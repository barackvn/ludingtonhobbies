# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import pytz
from odoo.exceptions import ValidationError


class HrEmployeeClock(models.Model):
    _name = 'hr.employee.clock'

    day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], string='Day', required=True)
    clock_in = fields.Float(string='Clock In', required=True)
    clock_out = fields.Float(string='Clock Out', required=True)


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    employee_clock_ids = fields.Many2many('hr.employee.clock', string='Employee Clock')

    def action_employee_clock_notification(self):
        date_time_now = datetime.now()

        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        date_time_now = pytz.utc.localize(date_time_now).astimezone(user_timezone)

        if date_time_now.hour == 20 or True:
            employees = self.env['hr.employee'].search([])
            late_employees_list = []

            absent = True
            to_present = False
            for employee in employees:
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])

                clock_in = None
                clock_out = None

                for clock in employee.employee_clock_ids:
                    if clock.day == datetime.now().strftime("%A").lower():
                        to_present = True
                        clock_in = clock.clock_in
                        clock_out = clock.clock_out

                if to_present:
                    for attendance in attendances:
                        if attendance.check_in.date() == datetime.now().date() or attendance.check_out.date() == datetime.now().date():
                            absent = False

                if clock_in and clock_out:
                    if to_present:
                        if absent:
                            employee_info = \
                                {
                                    'clock_in': 'Absent',
                                    'clock_out': 'Absent',
                                    'check_in': "{:.2f}".format(clock_in),
                                    'check_out': "{:.2f}".format(clock_out),
                                    'employee_name': employee.name,
                                }
                            late_employees_list.append(employee_info)

            for employee in employees:
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])
                for attendance in attendances:
                    if attendance.check_in and attendance.check_out:
                        if attendance.check_in.date() == datetime.now().date() and attendance.check_out.date() == datetime.now().date():
                            for clock in employee.employee_clock_ids:
                                if clock.day == datetime.now().strftime("%A").lower():
                                    user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)

                                    check_in = pytz.utc.localize(attendance.check_in).astimezone(user_timezone)
                                    check_out = pytz.utc.localize(attendance.check_out).astimezone(user_timezone)

                                    str_check_in = str(check_in.hour) + '.' + str(check_in.minute)
                                    float_check_in = float(str_check_in)

                                    str_check_out = str(check_out.hour) + '.' + str(check_out.minute)
                                    float_check_out = float(str_check_out)

                                    if float_check_in > clock.clock_in or float_check_out < clock.clock_out:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': str(check_out.time())[:5],
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)
                                    elif (float_check_out - clock.clock_out) > 0.15:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': str(check_out.time())[:5],
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)
                    elif attendance.check_in and not attendance.check_out:
                        if attendance.check_in.date() == datetime.now().date():
                            for clock in employee.employee_clock_ids:
                                if clock.day == datetime.now().strftime("%A").lower():
                                    user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)

                                    check_in = pytz.utc.localize(attendance.check_in).astimezone(user_timezone)

                                    str_check_in = str(check_in.hour) + '.' + str(check_in.minute)
                                    float_check_in = float(str_check_in)

                                    if float_check_in > clock.clock_in:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': 'None',
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)

            if late_employees_list:
                late_employees_dictionary = {'late_employees_list': late_employees_list}

                template_id = self.env.ref('manage_employee.mail_employee_clock_notifications').id
                self.env['mail.template'].browse(template_id).with_context(late_employees_dictionary).send_mail(self.id, force_send=True)

            employees = self.env['hr.employee'].search([])

            absent = True
            to_present = False
            for employee in employees:
                late_employees_list = []
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])

                clock_in = None
                clock_out = None

                for clock in employee.employee_clock_ids:
                    if clock.day == datetime.now().strftime("%A").lower():
                        to_present = True
                        clock_in = clock.clock_in
                        clock_out = clock.clock_out

                if to_present:
                    for attendance in attendances:
                        if attendance.check_in.date() == datetime.now().date() or attendance.check_out.date() == datetime.now().date():
                            absent = False

                if clock_in and clock_out:
                    if to_present:
                        if absent:
                            employee_info = \
                                {
                                    'clock_in': 'Absent',
                                    'clock_out': 'Absent',
                                    'check_in': "{:.2f}".format(clock_in),
                                    'check_out': "{:.2f}".format(clock_out),
                                    'employee_name': employee.name,
                                }
                            late_employees_list.append(employee_info)
                            late_employees_dictionary = {'late_employees_list': late_employees_list}
                            template_id = self.env.ref('manage_employee.mail_employee_clock_notifications_manager').id
                            self.env['mail.template'].browse(template_id).with_context(late_employees_dictionary).send_mail(employee.parent_id.id, force_send=True)

            for employee in employees:
                late_employees_list = []
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])

                for attendance in attendances:
                    if attendance.check_in and attendance.check_out:
                        if attendance.check_in.date() == datetime.now().date() and attendance.check_out.date() == datetime.now().date():
                            for clock in employee.employee_clock_ids:
                                if clock.day == datetime.now().strftime("%A").lower():
                                    user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)

                                    check_in = pytz.utc.localize(attendance.check_in).astimezone(user_timezone)
                                    check_out = pytz.utc.localize(attendance.check_out).astimezone(user_timezone)

                                    str_check_in = str(check_in.hour) + '.' + str(check_in.minute)
                                    float_check_in = float(str_check_in)

                                    str_check_out = str(check_out.hour) + '.' + str(check_out.minute)
                                    float_check_out = float(str_check_out)

                                    if float_check_in > clock.clock_in or float_check_out < clock.clock_out:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': str(check_out.time())[:5],
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)
                                        late_employees_dictionary = {'late_employees_list': late_employees_list}
                                        template_id = self.env.ref('manage_employee.mail_employee_clock_notifications_manager').id
                                        self.env['mail.template'].browse(template_id).with_context(late_employees_dictionary).send_mail(employee.parent_id.id, force_send=True)
                                    elif (float_check_out - clock.clock_out) > 0.15:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': str(check_out.time())[:5],
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)
                                        late_employees_dictionary = {'late_employees_list': late_employees_list}
                                        template_id = self.env.ref('manage_employee.mail_employee_clock_notifications_manager').id
                                        self.env['mail.template'].browse(template_id).with_context(late_employees_dictionary).send_mail(employee.parent_id.id, force_send=True)
                    elif attendance.check_in and not attendance.check_out:
                        if attendance.check_in.date() == datetime.now().date():
                            for clock in employee.employee_clock_ids:
                                if clock.day == datetime.now().strftime("%A").lower():
                                    user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)

                                    check_in = pytz.utc.localize(attendance.check_in).astimezone(user_timezone)

                                    str_check_in = str(check_in.hour) + '.' + str(check_in.minute)
                                    float_check_in = float(str_check_in)

                                    if float_check_in > clock.clock_in:
                                        employee_info = {
                                                            'clock_in': str(check_in.time())[:5],
                                                            'clock_out': 'None',
                                                            'check_in': "{:.2f}".format(clock.clock_in),
                                                            'check_out': "{:.2f}".format(clock.clock_out),
                                                            'employee_name': employee.name,
                                                        }
                                        late_employees_list.append(employee_info)

                                        late_employees_dictionary = {'late_employees_list': late_employees_list}
                                        template_id = self.env.ref('manage_employee.mail_employee_clock_notifications_manager').id
                                        self.env['mail.template'].browse(template_id).with_context(late_employees_dictionary).send_mail(employee.parent_id.id, force_send=True)
