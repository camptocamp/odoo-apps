# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class Country(models.Model):
    _inherit = "res.country"

    free_trade_agreement = fields.Boolean(string='Free Trade Agreement')
    agreement_desc = fields.Text("Free Trade Agreement Details")


class CountryGroup(models.Model):
    _inherit = "res.country.group"

    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
