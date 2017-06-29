# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
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
                production_lot = move.quant_ids.mapped('lot_id')
                product_warranty = move.product_id.warranty
                warranty_month = int(product_warranty)
                warranty_days = int((product_warranty-warranty_month)*30)
                warranty_date = (
                    fields.Date.from_string(move.date) +
                    relativedelta(months=warranty_month) +
                    relativedelta(days=warranty_days)
                )
                production_lot.write({
                    'warranty_end_date': warranty_date,
                    'warranty_stock_move_id': move.id
                })
        return True
