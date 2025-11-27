from odoo import models, fields
from datetime import timedelta

class ScheduleLesson(models.Model):
    _name = "le.schedule.lesson"
    _description = "Schedule Lesson"
    _order = "lesson_date"
    
    name = fields.Char(string="Name", required=True)
    schedule_table_id = fields.Many2one("le.schedule.table", string="Schedule", required=True)
    group_id = fields.Many2one('le.group', string="Group")
    lesson_date = fields.Date(string="Lesson Date", required=True)
    lesson_start_time = fields.Float(string="Start Time", required=True)
    lesson_end_time = fields.Float(string="End Time", required=True)
    status = fields.Selection([('draft', 'Yangi'), ('passed', "O'tilgan"), ('canceled', 'Bekor qilingan'), ('transfer', "Ko'chirildi")], default="draft")

    def leaving_lesson(self):
        self.status = 'transfer'
        name = self.name

        lessons = self.env['le.schedule.lesson'].search([('status', '=', 'draft'), ('schedule_table_id', '=', self.schedule_table_id.id), 
        ('lesson_date', '>', self.lesson_date)], order='lesson_date asc')
        print(lessons)
        for lesson in lessons:
            lesson_name = lesson.name
            lesson.name = name
            name = lesson_name

        weekday_index = {
                    "monday": 0,
                    "tuesday": 1,
                    "wednesday": 2,
                    "thursday": 3,
                    "friday": 4,
                    "saturday": 5,
                    "sunday": 6,
                }
        week_numbers = [weekday_index[w.name.lower()] for w in lessons[0].schedule_table_id.weekday_ids]        
        
        lesson_date = lessons[-1].lesson_date+timedelta(days=1)
        while True:
            if lesson_date.weekday() in week_numbers:
                self.env['le.schedule.lesson'].create({'name':name, 'schedule_table_id':self.schedule_table_id.id, 'group_id': self.group_id.id, 'lesson_date':lesson_date, "lesson_start_time": self.lesson_start_time, "lesson_end_time":self.lesson_end_time})
                break
            lesson_date += timedelta(days=1)

    def transfer_lesson(self):
        pass

    def delete_lesson(self):

        lessons = self.env['le.schedule.lesson'].search(
            [('schedule_table_id', '=', self.schedule_table_id.id)],
            order='lesson_date asc, id asc'
        )

        lesson_id = lessons.ids.index(self.id)

        next_lessons = lessons[lesson_id+1:]

        prev_name = next_lessons[0].name 
        self.name = prev_name           

        for i in range(1, len(next_lessons)):
            current_lesson = next_lessons[i]
            next_lessons[i-1].name = current_lesson.name  
        next_lessons[-1].unlink()

        
    def button_passed(self):
            self.status = "passed"

    
        


