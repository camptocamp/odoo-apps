# -*- coding: utf-8 -*-
# Part of SenseFly.
from odoo import fields, models
import uuid


class Partner(models.Model):
    _inherit = 'res.partner'

    is_intragroup = fields.Boolean(string='Is Intragroup',
                                   help='This partner belongs to Parrot Group')
    uuid = fields.Char(
        'UUID', index=True, default=lambda self: '%s' % uuid.uuid4(),
        required=True)

    _sql_constraints = [
        ('unique_uuid', 'UNIQUE(uuid)', 'UUID must be unique!'),
    ]
