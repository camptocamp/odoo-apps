# -*- coding: utf-8 -*-
# Part of SenseFly.
from odoo import fields, models, api
import uuid


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default['uuid'] = uuid.uuid4()
        return super(Partner, self).copy(default)

    is_intragroup = fields.Boolean(string='Is Intragroup',
                                   help='This partner belongs to Parrot Group')
    uuid = fields.Char(
        'UUID', index=True, default=lambda self: '%s' % uuid.uuid4(),
        required=True)

    _sql_constraints = [
        ('unique_uuid', 'UNIQUE(uuid)', 'UUID must be unique!'),
    ]
