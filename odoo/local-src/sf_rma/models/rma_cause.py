# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class RMA(models.Model):
    _name = 'sf.rma.cause'

    name = fields.Char()
