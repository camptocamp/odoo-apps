# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class CountryGroup(models.Model):
    _inherit = "res.country.group"

    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
