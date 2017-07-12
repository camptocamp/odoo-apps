# -*- coding: utf-8 -*-
# Part of SenseFly.
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    is_intragroup = fields.Boolean(string='Is Intragroup',
                                   help='This partner belongs to Parrot Group')
