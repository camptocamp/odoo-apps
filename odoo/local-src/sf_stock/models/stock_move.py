# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class StockMove(models.Model):

    _inherit = "stock.move"

    @api.multi
    def action_done(self):
        super(StockMove, self).action_done()
        for move in self:
            condition = (
                move.state == 'done'
                and move.product_tmpl_id.tracking == 'serial'
                and move.picking_type_id.code == 'outgoing'
            )
            if condition:
                production_lot = move.mapped('quant_ids.lot_id')
                if len(production_lot) > 1:
                    raise UserError(_(
                        'There are different stock.production.lot linked to '
                        'this move quants.'))
                if move.product_id.warranty:
                    product_warranty = move.product_id.warranty
                    warranty_month = int(product_warranty)
                    # As product_warranty is a float, the decimals are
                    # converted to days on 30 days month basis
                    warranty_days = int((product_warranty-warranty_month)*30)
                    warranty_date = (
                        fields.Date.from_string(move.date) +
                        relativedelta(months=warranty_month,
                                      days=warranty_days)
                    )
                else:
                    warranty_date = None
                production_lot.write({
                    'warranty_end_date': warranty_date,
                    'warranty_stock_move_id': move.id
                })
        return True
