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

    @api.multi
    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        # RMA in this conditions is not invoiced
        is_rma = self.type_id.id == self.env.ref('sf_rma.rma_sale_type').id
        under_warranty_rma = self.rma_id.decision in ('free', 'to_offer')
        if is_rma and under_warranty_rma and self.amount_total == 0:
            self.invoice_status = 'no'
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    repair_line_id = fields.Many2one('mrp.repair.line', string="Repair Line")
    is_rma_product = fields.Boolean(
        string="RMA product",
        compute='_compute_is_rma_product',
        store=True)

    @api.depends('repair_line_id')
    def _compute_is_rma_product(self):
        for line in self:
            rma_route = line.order_id.company_id.rma_sale_line_route_id
            if line.order_id.rma_id and not line.repair_line_id \
                    and line.route_id == rma_route:
                line.is_rma_product = True

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

    @api.depends('invoice_lines.invoice_id.state', 'invoice_lines.quantity')
    def _get_invoice_qty(self):
        for line in self:
            if line.is_rma_product:
                line.qty_invoiced = 0
        super(SaleOrderLine, self)._get_invoice_qty()

    @api.depends('state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice',
                 'qty_invoiced')
    def _compute_invoice_status(self):
        super(SaleOrderLine, self)._compute_invoice_status()

        for line in self:
            # Returned product? Nothing to invoiced
            if line.is_rma_product:
                line.invoice_status = 'no'
