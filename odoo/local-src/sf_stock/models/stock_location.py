# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_department_location = fields.Boolean(string='Is a Department Location',
                                            help='This location has '
                                                 'department link to an '
                                                 'analytic account.')
