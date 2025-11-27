from odoo import fields, models
from datetime import datetime

class ScheduleStudentLesson(models.Model):
    _name = "le.schedule_student_lesson"
    _description = "Schedule Student Lesson"

    schedule_lesson_id = fields.Many2one('le.schedule.lesson')
    student_id = fields.Many2one('res.users')
    payment_id = fields.Many2one('le.payment')

    def payment_action(self):
        today = datetime.today()
        students = self.env['le.group.student'].search([('status', '=', 'active'), 'group_id.payment_type', '=', 'per_lesson'])
        for student in students:
            student.group_id.
