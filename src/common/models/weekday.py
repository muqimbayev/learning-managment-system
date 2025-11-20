from odoo import models, fields


class Weekday(models.Model):
    _name = "common.weekday"
    _description = "Weekday"

    name = fields.Char(string="Name", required=True)
    sequence_num = fields.Integer(string="Sequence", default=0)
