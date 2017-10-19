# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, _


class AccountAnalyticTag(models.Model):
    _inherit = "account.analytic.tag"

    code = fields.Char()

    _sql_constraints = [('uniq_code', 'unique(code)',
                         _("The code of this account must be unique !"))]
