# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class EntityType(models.Model):
    _name = 'res.partner.entity.type'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
