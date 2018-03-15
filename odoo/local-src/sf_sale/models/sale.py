# -*- coding: utf-8 -*-
# Part of sensefly.
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    second_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson (2nd)',
        help='This person is also related with the sale.'
    )

    def _reset_delivery_method(self, order_lines):
        """Check if reset delivery method is needed.
        Delivery method field must be reseted when a change that
        affects shipping calculation is applied on sale order lines"""

        def is_service(product_id):
            if product_id:
                product = self.env['product.product'].browse(product_id)
                if product.type == 'service':
                    return True
            return False

        # RMAs under warranty? Do not reset delivery method.
        # SO of type RMA and RMA with decision Free or Commercial Gesture
        if self.type_id.id == self.env.ref('sf_rma.rma_sale_type').id \
                and self.rma_id.decision in ('free', 'to_offer'):
            return False

        # Check the changes on the order lines
        to_reset = False
        for line_vals in order_lines:
            if len(line_vals) > 1 and line_vals[1]:
                line = self.env['sale.order.line'].browse(line_vals[1])
                line_product_type = line.product_id.type

            # New record. Adding physical product
            if line_vals[0] == 0 \
                    and not is_service(line_vals[2]['product_id']):
                to_reset = True
                break
            # Update linked record.
            # Changing qty of physical product
            elif line_vals[0] == 1 \
                    and line_product_type != 'service' \
                    and 'product_uom_qty' in line_vals[2]:
                to_reset = True
                break
            # Update linked record.
            # Changing from a service to a physical product
            elif line_vals[0] == 1 and line_product_type == 'service' \
                    and 'product_id' in line_vals[2] \
                    and not is_service(line_vals[2]['product_id']):
                to_reset = True
                break
            # Remove and delete the linked record
            elif line_vals[0] == 2 and line_product_type != 'service':
                to_reset = True
                break
        return to_reset

    @api.multi
    def write(self, vals):
        for sale_order in self:
            # Reset delivery method (except for delivery method managers)
            delivery_method_man = self.env.user.has_group(
                'sf_stock.group_delivery_method_manager'
            )
            if sale_order.state in ('draft', 'sent') \
                    and 'order_line' in vals \
                    and not delivery_method_man \
                    and self._reset_delivery_method(vals['order_line']):
                sale_order.carrier_id = False

            # Propagate carrier to stock.picking when confirming SO
            # is confirmed
            if self.env.context.get('action_confirm', False) \
                    and sale_order.picking_ids:
                for pick in sale_order.picking_ids:
                    pick_type = pick.picking_type_id
                    pick_type_xml_id = pick_type.get_xml_id()[pick_type.id]
                    # - senseFly SA propagate carrier to the Reserve and Pack
                    # - sensefly Inc propagate carrier to the Delivery Order
                    if pick_type_xml_id in (
                            '__setup__.stock_pick_type_reserve_pack',
                            '__setup__.picking_type_out_inc'):
                        pick.carrier_id = sale_order.carrier_id

        return super(SaleOrder, self).write(vals)

    @api.multi
    def action_confirm(self):
        return super(SaleOrder,
                     self.with_context(action_confirm=True)
                     ).action_confirm()

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self,
                                             'sf_sale.sf_report_saleorder')

    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()

        # Replace default email template
        ir_model_data = self.env['ir.model.data']

        try:
            template_id = ir_model_data.get_object_reference(
                'sf_sale', 'sf_email_template_edi_sale')[1]
        except ValueError:
            template_id = False

        res['context'].update(
            {
                'default_use_template': bool(template_id),
                'default_template_id': template_id
             })
        return res

    @api.model
    def get_move_from_line(self, line):
        # Override standard method to cope with Warehouse -> Outgoing shipping
        # configuration: 1. ship_only; 2. two_steps; 3. pick_pack_ship

        move = self.env['stock.move']
        lot_count = 0
        for p in line.order_id.picking_ids.sorted(
                key=lambda r: r.picking_type_id.sequence, reverse=True):
            for m in p.move_lines:
                if line.lot_id == m.restrict_lot_id:
                    move = m
                    lot_count += 1

        delivery_steps = self.warehouse_id.delivery_steps
        preconditions = [
            delivery_steps == 'ship_only' and lot_count == 1,
            delivery_steps == 'pick_ship' and lot_count == 2,
            delivery_steps == 'pick_pack_ship' and lot_count == 3
        ]

        lot_count_ok = any(preconditions)

        # if counter is different of the number of delivery steps,
        # it means that something goes wrong
        if not lot_count_ok:
            raise ValidationError(_('Can\'t retrieve lot on stock'))
        return move

    @api.model
    def _check_move_state(self, line):
        # When the payment term requires a down payment,
        # there's no need check stock moves state
        if self.payment_term_id.down_payment_required:
            return True
        return super(SaleOrder, self)._check_move_state(line)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_to_invoice_qty(self):
        """
        Change computation of the quantity to invoice.

        If the quantity delivered is used, we set it to the ordered quantity
        only if the total quantity is delivered.

        Otherwise, when the invoice policy is order, no change to the quantity
        to invoice, it is calculated from the ordered quantity.

        """
        on_deliver_lines = self.filtered(
            lambda rec: (rec.product_id.invoice_policy != 'order' and
                         rec.order_id.state in ['sale', 'done']))

        for line in on_deliver_lines:
            if line.product_uom_qty == line.qty_delivered:
                line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
            else:
                line.qty_to_invoice = 0

        other_lines = self - on_deliver_lines
        super(SaleOrderLine, other_lines)._get_to_invoice_qty()


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_ids = fields.One2many(
        'sale.order', 'procurement_group_id', string='Sale Orders',
        readonly=True)
