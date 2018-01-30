# -*- coding: utf-8 -*-
from odoo import models, fields


class WizardStockPickingAvailability(models.TransientModel):
    _name = 'wizard.stock.picking.availability'

    def _get_default_picking(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            return self.env['stock.picking'].browse(active_id)
        else:
            return False

    def do_reserve(self):
        pick = self.picking_id
        if self.force_availability:
            pick.force_assign()
            pick.message_post(body="Stock availability forced!")
        else:
            pick.with_context({'no_availability_check': True}).action_assign()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }

    picking_id = fields.Many2one('stock.picking',
                                 default=_get_default_picking,
                                 readonly=True)

    stock_move_lines = fields.One2many(related='picking_id.move_lines',
                                       string='Stock Moves',
                                       readonly=True)

    force_availability = fields.Boolean(string='Force Availability')
