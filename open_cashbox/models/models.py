# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosSessionInherited(models.Model):
    _inherit = 'pos.session'

    def action_open_cash_box(self):
        for rec in self:
            rec.cash_register_id.open_cashbox_id()
