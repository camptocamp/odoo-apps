# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class StockMove(models.Model):

    _inherit = "stock.move"

    def _compute_amount(self):
        """Compute the stock move price value
        based on the information of the related sale line"""
        for move in self:
            sale_line_id = move.procurement_id.sale_line_id
            if sale_line_id:
                price = sale_line_id.price_unit * \
                        (1 - (sale_line_id.discount or 0.0) / 100.0)
                taxes = sale_line_id.tax_id.compute_all(
                    price,
                    sale_line_id.currency_id,
                    move.product_uom_qty,
                    product=move.product_id,
                    partner=sale_line_id.order_id.partner_shipping_id)
                move.update({
                    'price_tax': taxes['total_included'] - taxes[
                        'total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })

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
                production_lots = move.mapped('quant_ids.lot_id')
                for lot in production_lots:
                    if lot.first_outgoing_stock_move_id:
                        continue
                    if move.product_id.warranty:
                        product_warranty = move.product_id.warranty
                        warranty_month = int(product_warranty)
                        # As product_warranty is a float, the decimals are
                        # converted to days on 30 days month basis
                        warranty_days = int(
                            30 * (product_warranty-warranty_month))
                        warranty_date = (
                            fields.Date.from_string(move.date) +
                            relativedelta(months=warranty_month,
                                          days=warranty_days)
                        )
                    else:
                        warranty_date = None
                    lot.write({
                        'warranty_end_date': warranty_date,
                        'first_outgoing_stock_move_id': move.id
                    })
        return True

    currency_id = fields.Many2one(
        related='procurement_id.sale_line_id.currency_id',
        string='Currency',
        readonly=True)
    price_subtotal = fields.Monetary(
        compute='_compute_amount',
        string='Subtotal', readonly=True
    )
    price_tax = fields.Monetary(
        compute='_compute_amount',
        string='Taxes', readonly=True
    )
    price_total = fields.Monetary(
        compute='_compute_amount',
        string='Total', readonly=True
    )
