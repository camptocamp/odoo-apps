# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    rma_id = fields.Many2one('sf.rma', string="RMA")

    @api.model
    def _check_move_state(self, line):
        # When the rma decision is to invoice, we need to be able to
        # confirm the SO + create Invoice.
        # At this point the repair is not finished yet, no procurements
        # were created, so no need to check move state.
        if self.rma_id and self.rma_id.decision == 'to_invoice':
            return True
        return super(SaleOrder, self)._check_move_state(line)

    @api.multi
    def write(self, vals):
        result = super(SaleOrder, self).write(vals)
        if 'down_payment_missing' in vals:
            for sale in self:
                if sale.state == 'sale':
                    sale.order_line._action_procurement_create()
        return result


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
