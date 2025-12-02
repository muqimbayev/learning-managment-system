from odoo import fields, models, api
from datetime import datetime
from datetime import datetime, time

class ScheduleStudentLesson(models.Model):
    _name = "le.schedule_student_lesson"
    _description = "Schedule Student Lesson"

    schedule_lesson_id = fields.Many2one('le.schedule.lesson')
    student_id = fields.Many2one('res.users')
    payment_id = fields.Many2one('le.payment')

    def float_to_time(self, f):
        hour = int(f)
        minute = int((f - hour) * 60)
        return time(hour, minute)

    def payment_action_daily(self):
        today = datetime.today().date()
        now_time = datetime.now().time()
        students = self.env['le.group.student'].search([('status', '=', 'active'), ('group_id.payment_type', '=', 'per_lesson')])
        for student in students:
            for table in student.group_id.table_schedule_ids:
                for lesson in table.schedule_lesson_ids:
                    lesson_end = self.float_to_time(lesson.lesson_end_time)
                    amount = 1000
                    amount_teacher = 200
                    if lesson.lesson_date <= today and lesson_end <= now_time:
                        self.env['le.payment'].create({'detailed_type': 'lesson_payment', 'schedule_student_lesson_id':self.id, 'amount':amount})
                        student.student_id.balance = student.student_id.balance - amount
                        #Teacher
                        self.env['le.payment'].create({'detailed_type': 'expense', 'teacher_id': self.schedule_lesson_id.schedule_table_id.teacher_id.id, 'amount':amount})
                        self.schedule_lesson_id.schedule_table_id.teacher_id.balance+=amount_teacher

                        




    def payment_action_monthly(self):
        today = datetime.today().date()
        now_time = datetime.now().time()
        students = self.env['le.group.student'].search([('status', '=', 'active'), ('group_id.payment_type', '=', 'per_month')])
        for student in students:
            for table in student.group_id.table_schedule_ids:
                for lesson in table.schedule_lesson_ids:
                    lesson_end = self.float_to_time(lesson.lesson_end_time)
                    amount = 10000
                    amount_teacher = 2000
                    if lesson.lesson_date <= today and lesson_end <= now_time: #Oylik pul yechish uchun groupga start_date qo'shsak shunda boshlangan kun agar bugungu kun bilan teng bo'lsa oylik pul yechib olamiz.
                        self.env['le.payment'].create({'detailed_type': 'lesson_payment', 'schedule_student_lesson_id':self.id, 'amount':amount})
                        student.student_id.balance-=amount
                        #Teacher
                        self.env['le.payment'].create({'detailed_type': 'expense', 'teacher_id': self.schedule_lesson_id.schedule_table_id.teacher_id.id, 'amount':amount})
                        self.schedule_lesson_id.schedule_table_id.teacher_id.balance+=amount_teacher



        