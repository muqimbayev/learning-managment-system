from odoo import models, fields


class Group(models.Model):
    """
    FSWD - 1
    """
    _inherit = "le.group"
    payment_type = fields.Selection([('per_lesson', 'Per Lesson'), ('per_month', 'Per Month')])
    
