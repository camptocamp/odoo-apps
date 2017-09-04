# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpRepair(models.Model):

    _inherit = 'mrp.repair'

    @api.multi
    def action_repair_done(self):
        """ Custom redefinition of action_repair_done with no call to super
        because we don't want to create a stock move should the operation be
        of type replace.
        Otherwise it creates stock move for operation and stock move for final
        product of repair order.
        @return: Move ids of final products

        """
        # ***************************** Odoo code *****************************
        if self.filtered(lambda repair: not repair.repaired):
            raise UserError(_(
                "Repair must be repaired in order to make the product moves."))
        res = {}
        Move = self.env['stock.move']
        for repair in self:
            moves = self.env['stock.move']
            for operation in repair.operations:
                # ************************ Custom code ************************
                if operation.type == 'replace':
                    continue
                # ************************* Odoo code *************************
                move = Move.create({
                    'name': operation.name,
                    'product_id': operation.product_id.id,
                    'restrict_lot_id': operation.lot_id.id,
                    'product_uom_qty': operation.product_uom_qty,
                    'product_uom': operation.product_uom.id,
                    'partner_id': repair.address_id.id,
                    'location_id': operation.location_id.id,
                    'location_dest_id': operation.location_dest_id.id,
                })
                moves |= move
                operation.write({'move_id': move.id, 'state': 'done'})
            move = Move.create({
                'name': repair.name,
                'product_id': repair.product_id.id,
                'product_uom': repair.product_uom.id or
                repair.product_id.uom_id.id,
                'product_uom_qty': repair.product_qty,
                'partner_id': repair.address_id.id,
                'location_id': repair.location_id.id,
                'location_dest_id': repair.location_dest_id.id,
                'restrict_lot_id': repair.lot_id.id,
            })
            moves |= move
            moves.action_done()
            res[repair.id] = move.id
        return res


class MrpRepairLine(models.Model):

    _inherit = 'mrp.repair.line'

    type = fields.Selection(selection_add=[('replace', 'Replace')])

    cause_id = fields.Many2one('mrp.repair.cause', string='Cause',
                               ondelete='restrict')


class MrpRepairCause(models.Model):

    _name = 'mrp.repair.cause'

    name = fields.Char('Name', required=True, translate=True)

    active = fields.Boolean(default=True)
