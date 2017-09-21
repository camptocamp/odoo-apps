# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


class PackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.multi
    @api.depends(
        'linked_move_operation_ids.move_id.procurement_id.sale_line_id')
    def _compute_sale_lines(self):
        for operation in self:
            operation.sale_line_ids = operation.linked_move_operation_ids.\
                mapped('move_id.procurement_id.sale_line_id')

    sale_line_ids = fields.One2many(
        'sale.order.line',
        string='Sale Line',
        compute='_compute_sale_lines',
        help='The sale order line that gave origin to this operation.')
