# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    rma_service_service_product_id = fields.Many2one(
        'product.product')

    rma_service_consumable_product_id = fields.Many2one(
        'product.product')

    rma_service_stockable_product_id = fields.Many2one(
        'product.product')

    rma_service_additional_description = fields.Char(translate=True)
