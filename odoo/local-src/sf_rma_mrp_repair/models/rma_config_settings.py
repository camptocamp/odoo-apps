# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RMASettings(models.TransientModel):

    _inherit = 'rma.config.settings'

    rma_repair_location_id = fields.Many2one(
        'stock.location', string='Repair current location',
        required=True, related='company_id.rma_repair_location_id',
        help="This is the repair location.")
    rma_repair_line_src_location_id = fields.Many2one(
        'stock.location', string='Repair Operations source location',
        required=True, related='company_id.rma_repair_line_src_location_id',
        help="This is the source location of the spare parts used"
             " in the repair.")
