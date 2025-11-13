from odoo import models, fields, api

class Users(models.Model):
    _inherit = "res.users"

    payment_ids = fields.One2many("lp.payment", "user_id", string="Payments")
    payment_count = fields.Integer(string="Payment Count", compute="_compute_payment_count")

    @api.depends("payment_ids")
    def _compute_payment_count(self):
        for user in self:
            user.payment_count = len(user.payment_ids)

    def action_view_payments(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Payments",
            "res_model": "lp.payment",
            "view_mode": "list,form",
            "domain": [("user_id", "=", self.id)],
        }
