# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models, _


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    lot_rma_id = fields.Many2one('stock.location', 'RMA Location')

    @api.multi
    def create_locations_rma(self):
        """
        Create a RMA location for RMA movements that takes place when internal,
        outgoing or incoming pickings are made from/to this location
        """
        location_obj = self.env['stock.location']

        for warehouse in self:
            if not warehouse.lot_rma_id:
                location = location_obj.with_context(
                    active_test=False
                ).create({
                    'name': _('RMA'),
                    'usage': 'internal',
                    'location_id': warehouse.view_location_id.id,
                    'company_id': warehouse.company_id.id,
                    'active': True,
                })
                warehouse.lot_rma_id = location

    def create(self, vals):
        """
        Create RMA location
        """
        warehouse = super(Warehouse, self).create(vals=vals)
        warehouse.create_locations_rma()
        return warehouse
