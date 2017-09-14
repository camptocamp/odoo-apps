# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, _


class DateRange(models.Model):
    _inherit = "date.range"

    code = fields.Char(required=True)

    _sql_constraints = [('uniq_code', 'unique(code, company_id)',
                         _("The code of this range must be unique !"))]
