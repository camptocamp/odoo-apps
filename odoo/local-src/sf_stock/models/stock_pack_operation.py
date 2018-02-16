# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _


class PackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.multi
    @api.depends(
        'linked_move_operation_ids.move_id.procurement_id.sale_line_id')
    def _compute_sale_lines(self):
        for operation in self:
            stock_moves = operation.linked_move_operation_ids.\
                mapped('move_id')

            while stock_moves.mapped('procurement_id.move_dest_id'):
                stock_moves = stock_moves.mapped('procurement_id.move_dest_id')
            operation.sale_line_ids = stock_moves.mapped(
                'procurement_id.sale_line_id'
            )

    @api.multi
    def action_split_lots(self):
        # We override this method to workaround the bug reported on
        # https://jira.camptocamp.com/browse/BSSFL-449
        # TODO create issue to fix OCA module

        action_ctx = dict(self.env.context)
        # If it's a returned stock move, we do not want to create a lot
        returned_move = any(self.mapped(
            'linked_move_operation_ids.move_id.origin_returned_move_id'))
        picking_type = self.mapped('picking_id.picking_type_id')
        action_ctx.update({
            'serial': 'serial' in self.mapped('product_id.tracking'),
            'only_create':
                picking_type.use_create_lots and
                not picking_type.use_existing_lots
                and not returned_move,
            'create_lots': picking_type.use_create_lots,
            'state_done': all([lot.picking_id.state == 'done'
                               for lot in self]),
            'show_reserved': any(
                [lot for lot in self.mapped('pack_lot_ids')
                 if lot.qty_todo > 0.0])})
        view_id = self.env.ref('stock.view_pack_operation_lot_form').id
        return {
            'name': _('Lot/Serial Number Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.pack.operation',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'res_id': self.ids,
            'context': action_ctx}

    sale_line_ids = fields.One2many(
        'sale.order.line',
        string='Sale Line',
        compute='_compute_sale_lines',
        help='The sale order line that gave origin to this operation.')
