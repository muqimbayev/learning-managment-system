from odoo import models, fields


class Group(models.Model):
    """
    FSWD - 1
    """
    _name = "le.group"
    _description = "Group"

    name = fields.Char(string="Name", required=True)
    course_id = fields.Many2one("le.course", string="Course", required=True)
    student_ids = fields.One2many("le.group.student", "group_id", string="Students")
    table_schedule_ids = fields.One2many('le.schedule.table', 'group_id')
    lesson_count = fields.Integer(default=10)

    def button_lesson(self):
        return {
            "name": "Darslar",
            "type": "ir.actions.act_window",
            "res_model": "le.schedule.lesson",
            "view_mode": "list,form",
            "domain": [('group_id', "=", self.id)],
        }
        
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