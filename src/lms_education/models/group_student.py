from odoo import models, fields


class GroupStudent(models.Model):
    _name = "le.group.student"
    _description = "Group Student"
    _rec_name = "student_id"

    group_id = fields.Many2one("le.group", string="Group", required=True)
    student_id = fields.Many2one("res.users", string="Student", required=True)
    status = fields.Selection([
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("frozen", "Frozen")
    ], string="Status", required=True, default="inactive")
    # student_schedule_lesson_ids = fields.One2many('le.schedule_student_lesson', 'student_id')
    attandance_count = fields.Integer(default=10)

    def action_attendance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Attendance',
            'res_model': 'le.schedule_student_lesson',
            'view_mode': 'list,form',
            'domain': [
                ('student_id', '=', self.id),
            ],
            'context': {
                'default_student_id': self.id
            }
        }
