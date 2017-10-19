# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RMASettings(models.TransientModel):

    _inherit = 'rma.config.settings'

    rma_service_service_product_id = fields.Many2one(
        'product.product', string='Repair Service for services', required=True,
        related='company_id.rma_service_service_product_id',
        domain=[('type', '=', 'service')],
        help="This service will appear on RMA sale orders as a placeholder "
             "for imported repair lines with a service product.")

    rma_service_consumable_product_id = fields.Many2one(
        'product.product', string='Repair Service for consumables',
        required=True,
        related='company_id.rma_service_consumable_product_id',
        domain=[('type', '=', 'service')],
        help="This service will appear on RMA sale orders as a placeholder "
             "for imported repair lines with a consumable product.")

    rma_service_stockable_product_id = fields.Many2one(
        'product.product', string='Repair Service for stockables',
        required=True,
        related='company_id.rma_service_stockable_product_id',
        domain=[('type', '=', 'service')],
        help="This product will appear on RMA sale orders as a placeholder "
             "for imported repair lines with a stockable product.")

    rma_service_additional_description = fields.Char(
        string='Additional description',
        related='company_id.rma_service_additional_description',
        help="This text will be appended to the sale order line description, "
             "after the replaced product name, for imported repair lines."
    )
