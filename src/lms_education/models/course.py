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

    
    def action_open(self):
        for record in self:
            if record.status == "draft" or record.status == "closed":
                record.status = "open"

    def action_close(self):
        for record in self:
            if record.status == "draft" or record.status == "open":
                record.status = "closed"

    def action_reset_draft(self):
        for record in self:
            if record.status == "closed":
                record.status = "draft"


