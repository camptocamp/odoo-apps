# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _


class DateRange(models.Model):
    _inherit = "date.range"

    @api.model
    def create(self, values):
        """By default the code will be the name"""
        if 'name' in values and not values.get('code', False):
            values['code'] = values['name'].lower()
        return super(DateRange, self).create(values)

    code = fields.Char(required=True)

    _sql_constraints = [('uniq_code', 'unique(code, company_id)',
                         _("The code of this range must be unique !"))]
