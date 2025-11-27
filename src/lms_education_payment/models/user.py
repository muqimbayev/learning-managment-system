from odoo import fields, models


class UserBalance(models.Model):
    _inherit = "res.users"

    balance = fields.Float(string="Balance", default=0)