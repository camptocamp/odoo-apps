# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rma_id = fields.Many2one('sf.rma', string="RMA")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        """
        Specific to create procurement order with conditions
        """
        for line in self:
            order = line.order_id
            repair_states = order.mapped('rma_id.repair_ids.state')
            need_to_create_procurement = (
                # We want to restrict procurement creation only in RMA context
                not order.rma_id or
                (
                    all(
                        state in ['done', 'cancel']
                        for state in repair_states
                    ) and
                    (
                        not order.down_payment_required or
                        not order.down_payment_missing
                    )
                )
            )
            if need_to_create_procurement:
                return super(SaleOrderLine, self)._action_procurement_create()
