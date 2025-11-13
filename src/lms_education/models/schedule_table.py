from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class ScheduleTable(models.Model):
    _name = "le.schedule.table"
    _description = "Schedule Table"

    name = fields.Char(string="Name", required=True)
    group_id = fields.Many2one("le.course", string="Group", required=True)
    schedule_lesson_ids = fields.One2many("le.schedule.lesson", "schedule_table_id", string="Schedule Lessons")

    teacher_id = fields.Many2one("res.users", string="Teacher", required=True)

    start_date = fields.Date(string="Start Date", required=True)
    weekday_ids = fields.Many2many("common.weekday", string="Weekdays", required=True)
    lesson_start_time = fields.Float(string="Start Time", required=True)
    lesson_end_time = fields.Float(string="End Time", required=True)
    lesson_count = fields.Integer(string="Lesson count", default=10)

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

            group_check = self.env["le.schedule.table"].search_count([
                ("group_id", "=", rec.group_id.id),
                ("lesson_start_time", "=", rec.lesson_start_time),
                ("weekday_ids", "in", rec.weekday_ids.ids),
            ])
            if group_check > 1:  
                raise ValidationError("Bu guruhni shu vaqtda darsi bor")

            teacher_check = self.env["le.schedule.table"].search_count([
                ("teacher_id", "=", rec.teacher_id.id),
                ("lesson_start_time", "=", rec.lesson_start_time),
                ("weekday_ids", "in", rec.weekday_ids.ids),
            ])
            if teacher_check > 1:
                raise ValidationError("Bu o'qituvchini shu vaqtda darsi bor")

            weekday_numbers = [weekday_index[w.name.lower()] for w in rec.weekday_ids]

            current_date = rec.start_date
            count = 1

            while count <= rec.lesson_count:
                if current_date.weekday() in weekday_numbers:
                    self.env["le.schedule.lesson"].create({
                        "name": f"{rec.group_id.name} - {count}",
                        "schedule_table_id": rec.id,
                        "lesson_date": current_date,
                        "lesson_start_time": rec.lesson_start_time,
                        "lesson_end_time": rec.lesson_end_time,
                    })
                    count += 1

                current_date += timedelta(days=1)

        return records