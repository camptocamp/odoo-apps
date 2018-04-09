# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
import uuid


class ProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    uuid = fields.Char(
        'UUID', index=True, default=lambda self: '%s' % uuid.uuid4(),
        required=True)
    invitation_key = fields.Char(
        string='Invitation key',
        help='The person or entity with this key, owns the product '
             'with this serial number')
    warranty_end_date = fields.Date('Warranty end date')
    first_outgoing_stock_move_id = fields.Many2one(
        'stock.move', string='First outgoing stock move')
    product_tracking = fields.Selection(related='product_id.tracking',
                                        readonly=True,
                                        string='Product tracking')

    notes = fields.Text(string='Comment')

    _sql_constraints = [
        ('unique_uuid', 'UNIQUE(uuid)', 'UUID must be unique!'),
        ('unique_invitation_key', 'UNIQUE(invitation_key)',
         'Invitation key must be unique!'),
    ]
