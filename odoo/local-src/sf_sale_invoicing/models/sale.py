# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api, _, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    down_payment_required = fields.Boolean(
        related='payment_term_id.down_payment_required',
        readonly=True,
    )
    down_payment_missing = fields.Boolean(
        compute='_compute_down_payment_missing',
        store=True
    )

    @api.multi
    @api.depends('order_line', 'order_line.product_id', 'payment_term_id',
                 'payment_term_id.down_payment_required', 'state',
                 'invoice_status')
    def _compute_down_payment_missing(self):

        down_payment_product = self.env[
            'sale.advance.payment.inv']._default_product_id()

        for sale in self:
            if (
                    sale.payment_term_id.down_payment_required and
                    sale.invoice_status != 'invoiced' and
                    sale.state not in ('cancel', 'done')
            ):
                sale.down_payment_missing = not bool(sale.order_line.filtered(
                    lambda l: l.product_id == down_payment_product
                ))
            else:
                sale.down_payment_missing = False

    @api.multi
    def _prepare_invoice(self):
        """ Adds fiscal position from picking partner on account invoice"""
        res = super(SaleOrder, self)._prepare_invoice()
        picking_partner = self.picking_ids.filtered(
            lambda p:
            p.state != 'cancel' and
            p.picking_type_id.code == 'outgoing').mapped('partner_id')
        if picking_partner and len(picking_partner) == 1:
            res.update({
                'fiscal_position_id':
                    picking_partner.property_account_position_id.id
            })
        elif picking_partner and len(picking_partner) > 1:
            raise UserError(_('It is not possible to have more than one '
                              'delivery order partner per sale order!'))
        return res

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """ Ensure one invoice is created per sale order """
        return super(SaleOrder, self).action_invoice_create(grouped=True)


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        """ Do not create procurement if down payment is missing on
        sale order"""
        lines_to_procure = self.filtered(
            lambda l: not l.order_id.down_payment_missing)
        res = super(SaleOrderLine,
                    lines_to_procure)._action_procurement_create()
        return res
