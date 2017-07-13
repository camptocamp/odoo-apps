# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class DateRange(models.Model):
    _inherit = "date.range"

    code = fields.Char()
