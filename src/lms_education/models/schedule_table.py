from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class ScheduleTable(models.Model):
    _name = "le.schedule.table"
    _description = "Schedule Table"

    name = fields.Char(string="Name", required=True)
    group_id = fields.Many2one("le.group", string="Group", required=True)
    schedule_lesson_ids = fields.One2many("le.schedule.lesson", "schedule_table_id", string="Schedule Lessons")

    teacher_id = fields.Many2one("res.users", string="Teacher", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    weekday_ids = fields.Many2many("common.weekday", string="Weekdays", required=True)
    lesson_start_time = fields.Float(string="Start Time", required=True)
    lesson_end_time = fields.Float(string="End Time", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        weekday_index = {
                    "monday": 0,
                    "tuesday": 1,
                    "wednesday": 2,
                    "thursday": 3,
                    "friday": 4,
                    "saturday": 5,
                    "sunday": 6,
                }

        for rec in records:
            lesson_count = self.env['le.lesson'].search([('course_id', '=', rec.group_id.course_id.id)])

            group_check = self.env["le.schedule.table"].search_count([
                ("group_id", "=", rec.group_id.id),
                    ("lesson_start_time", "<", rec.lesson_end_time), ("lesson_end_time", ">", rec.lesson_start_time),
                ("weekday_ids", "in", rec.weekday_ids.ids),
            ])
            if group_check > 1:  
                raise ValidationError("Bu guruhni shu vaqtda darsi bor")

            teacher_check = self.env["le.schedule.table"].search_count([
                ("teacher_id", "=", rec.teacher_id.id),
                    ("lesson_start_time", "<", rec.lesson_end_time), ("lesson_end_time", ">", rec.lesson_start_time),
                ("weekday_ids", "in", rec.weekday_ids.ids),
            ])
            if teacher_check > 1:
                raise ValidationError("Bu o'qituvchini shu vaqtda darsi bor")

            current_date = rec.start_date
            count = 0
        
            # week_numbers = [int(x) for x in rec.weekday_ids.mapped("sequence_num")]
            week_numbers = [weekday_index[w.name.lower()] for w in rec.weekday_ids]        

            while count < len(lesson_count):
                if current_date.weekday() in week_numbers:
                    new_lesson = self.env["le.schedule.lesson"].create({
                        "name": f"{lesson_count[count].name}",
                        "schedule_table_id": rec.id,
                        "lesson_date": current_date,
                        "lesson_start_time": rec.lesson_start_time,
                        "lesson_end_time": rec.lesson_end_time,
                        'group_id': rec.group_id.id
                    })
                    count += 1

                    #Lesson Payment uchun scheule
                    lesson_id = new_lesson.id
                    students = rec.group_id.student_ids
                    for student in students:
                        self.env['le.schedule_student_lesson'].create({"schedule_lesson_id": lesson_id, "student_id": student.id, "payment_id": False})

                current_date += timedelta(days=1)

        return records
