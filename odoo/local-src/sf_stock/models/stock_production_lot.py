# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    warranty_end_date = fields.Date('Warranty end date')
    first_outgoing_stock_move_id = fields.Many2one(
        'stock.move', string='First outgoing stock move')
    product_tracking = fields.Selection(related='product_id.tracking',
                                        readonly=True,
                                        string='Product tracking')

    notes = fields.Text(string='Comment')
