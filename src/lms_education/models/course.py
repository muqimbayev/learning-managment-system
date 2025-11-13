from odoo import models, fields


class Course(models.Model):
    """
    Full Stack Web Development
    """
    _name = "le.course"
    _description = "Course"

    name = fields.Char(string="Name", required=True)
    lesson_ids = fields.One2many("le.lesson", "course_id", string="Lessons")
    subject_ids = fields.Many2many("le.subject", string="Subjects")
    status = fields.Selection([
        ("draft", "Draft"),
        ("open", "Open"),
        ("closed", "Closed"),
    ], default="draft", required=True)

    def create_schedule_lesson(self):
            self.ensure_one()

            return {
                "type": "ir.actions.act_window",
                "res_model": "le.schedule.table",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_group_id": self.id,  
                }
            }