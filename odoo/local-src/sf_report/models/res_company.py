# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class Country(models.Model):
    _inherit = "res.company"

    report_logo = fields.Binary(string="Reporting Logo")
