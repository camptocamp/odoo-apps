# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RMASettings(models.TransientModel):

    _inherit = 'rma.config.settings'

    rma_service_product_id = fields.Many2one(
        'product.product', string='Repair Service', required=True,
        related='company_id.rma_service_product_id',
        domain=[('type', '=', 'service')],
        help="This product will appear on RMA sale orders as a placeholder "
             "for imported repair lines.")
