# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RMASettings(models.TransientModel):

    _name = 'rma.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    rma_sale_line_route_id = fields.Many2one(
        'stock.location.route', string='Sale Line route',
        required=True,
        related='company_id.rma_sale_line_route_id',
        help="This route will be used in the sale order line.")
