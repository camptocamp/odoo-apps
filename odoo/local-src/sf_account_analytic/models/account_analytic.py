# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    user_id = fields.Many2one('res.users',
                              string='Owner',
                              track_visibility='onchange')
