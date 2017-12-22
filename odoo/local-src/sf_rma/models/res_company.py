# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    rma_sale_line_route_id = fields.Many2one(
        'stock.location.route')
