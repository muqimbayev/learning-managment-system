from odoo import fields, models, api
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

    #per lesson bilan kelishilgan

    @api.model
    def payment_action_daily(self):
        today = datetime.today().date()
        now_time = datetime.now().time()

        # Active studentlar olinadi  per lesson uchun
        students = self.env['le.group.student'].search([
            ('status', '=', 'active'),
            ('group_id.payment_type', '=', 'per_lesson')
        ])

        for gs in students:  # gs = group student obejtlarini
            for table in gs.group_id.table_schedule_ids:
                for lesson in table.schedule_lesson_ids:

                    # dars vaqtini tekshirish
                    lesson_end = self.float_to_time(lesson.lesson_end_time)
                    if not (lesson.lesson_date <= today and lesson_end <= now_time):
                        continue

                    ssl = self.search([
                        ('schedule_lesson_id', '=', lesson.id),
                        ('student_id', '=', gs.student_id.id)
                    ], limit=1)

                    # avoid double payment
                    if ssl.payment_id:
                        continue

                    # narxlar shunchaki yozib qo'yildi
                    amount = 1000
                    teacher_amount = 200

                    # payment modeli yaratiladi
                    pay = self.env['le.payment'].create({
                        'detailed_type': 'lesson_payment',
                        'schedule_student_lesson_id': ssl.id,
                        'amount': amount,
                    })
                    ssl.payment_id = pay.id

                    # balansini yangilanadi
                    gs.student_id.balance -= amount

                    # teacher uchun to'lov agar 1 ta dars uchun olmoqchi bo'lsa
                    if table.teacher_payment_type == 'per_lesson':
                        self.env['le.payment'].create({
                            'detailed_type': 'expense',
                            'teacher_id': table.teacher_id.id,
                            'amount': teacher_amount,
                        })
                        table.teacher_id.balance += teacher_amount

    # MONTHLY to'lovlar
    @api.model
    def payment_action_monthly(self):
        today = datetime.today().date()
        now_time = datetime.now().time()

        students = self.env['le.group.student'].search([
            ('status', '=', 'active'),
            ('group_id.payment_type', '=', 'per_month')
        ])

        for gs in students:
            for table in gs.group_id.table_schedule_ids:
                for lesson in table.schedule_lesson_ids:

                    lesson_end = self.float_to_time(lesson.lesson_end_time)
                    if not (lesson.lesson_date <= today and lesson_end <= now_time):
                        continue

                    ssl = self.search([
                        ('schedule_lesson_id', '=', lesson.id),
                        ('student_id', '=', gs.student_id.id)
                    ], limit=1)

                    if ssl.payment_id:
                        continue

                    # narxlar shunchaki yozib qo'yildi
                    amount = 10000
                    teacher_amount = 2000

                    pay = self.env['le.payment'].create({
                        'detailed_type': 'lesson_payment',
                        'schedule_student_lesson_id': ssl.id,
                        'amount': amount,
                    })
                    ssl.payment_id = pay.id

                    gs.student_id.balance -= amount

                    if table.teacher_payment_type == 'per_month':
                        self.env['le.payment'].create({
                            'detailed_type': 'expense',
                            'teacher_id': table.teacher_id.id,
                            'amount': teacher_amount,
                        })
                        table.teacher_id.balance += teacher_amount
