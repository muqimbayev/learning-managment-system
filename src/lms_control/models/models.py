from odoo import models, fields

class ScheduleTable(models.Model):
    _inherit = "le.schedule_student_lesson"

    attendance = fields.Boolean(string="Attended", default=False)
    attandance_date = fields.Datetime(default=fields.Datetime.now())

class ScheduleLesson(models.Model):
    _inherit = "le.schedule.lesson"

    def button_passed(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'le.schedule_student_lesson',
            'view_mode': 'list',
            'views': [
                (self.env.ref('lms_control.attendance_lesson_list_view').id, 'list')
            ],
            'target': 'new', 
            'domain': [('schedule_lesson_id', '=', self.id), ('student_id.status', '=', 'active')],
            'context': {
                'default_schedule_lesson_id': self.id,
            }
        }
