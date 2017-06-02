# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    entity_type_id = fields.Many2one(
        'res.partner.entity.type',
        string="Entity Type"
    )
