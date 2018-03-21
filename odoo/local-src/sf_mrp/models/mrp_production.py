# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def open_produce_product(self):
        """ override base mrp.production open_produce_product method """
        self.ensure_one()

        for move in self.move_raw_ids:
            if move.has_tracking in ['lot', 'serial'] and \
                    move.product_uom_qty != move.quantity_done:
                raise ValidationError('Not all lot material consumed!')

        action = self.env.ref('mrp.act_mrp_product_produce').read()[0]
        return action

    @api.model
    def _revert_stock_move(self, move):
        new_move = move.copy({
            'state': 'draft',
            'location_id': move.location_dest_id.id,
            'location_dest_id': move.location_id.id,
            'origin_returned_move_id': move.id,
            'procure_method': 'make_to_stock'
        })
        move.move_dest_id = new_move
        new_move.action_confirm()
        new_move.action_assign()
        new_move.action_done()
        return new_move

    @api.multi
    def button_cancel_mo(self):
        if not self.env.user.has_group('sf_mrp.group_mrp_cancel_mo'):
            raise UserError("Only users in group "
                            "'sf_mrp.group_mrp_cancel_mo' can cancel MO")
        limit_date = date.today().replace(day=1)
        for mo in self:
            if (mo.state == 'done' and
                    fields.Date.from_string(mo.date_finished) < limit_date):
                raise ValidationError(
                    'Cannot cancel done order from last month or older')

            mo.post_inventory()
            for move in mo.move_finished_ids.filtered(
                    lambda m: m.state != 'cancel'):
                if move.state != 'done':
                    move.action_cancel()
                else:
                    if not all(
                            location_id == move.location_dest_id
                            for location_id in
                            move.quant_ids.mapped('location_id')):
                        raise ValidationError(
                            'Cannot cancel order if finished products are '
                            'no longer in stock')
                    self._revert_stock_move(move)

            for move in mo.move_raw_ids.filtered(
                    lambda m: m.state != 'cancel'):
                if move.state != 'done':
                    move.action_cancel()
                else:
                    self._revert_stock_move(move)

            mo.action_cancel()
