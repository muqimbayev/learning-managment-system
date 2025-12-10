from odoo import models, fields

class ScheduleTable(models.Model):
    _inherit = "le.schedule.table"

    def _create_student_payment_schedule(self, new_lesson):
        students = new_lesson.group_id.student_ids
        for student in students:
            self.env['le.schedule_student_lesson'].create({
                "schedule_lesson_id": new_lesson.id,
                "student_id": student.id,
                "payment_id": False
            })
