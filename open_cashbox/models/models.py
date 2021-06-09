# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosSessionInherited(models.Model):
    _inherit = 'pos.session'
