# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sf_state = fields.Selection(
        selection=[
            ('waiting_delivery_method', 'Waiting delivery method'),
            (
                'waiting_send_quotation_to_customer',
                'Waiting send quotation to customer'
            ),
            ('waiting_customer_confirmation', 'Waiting customer confirmation'),
            ('waiting_down_payment_creation', 'Waiting down payment creation'),
            (
                'waiting_down_payment_validation',
                'Waiting down payment validation'
            ),
            ('waiting_reservation', 'Waiting reservation'),
            ('packing_in_waiting', 'Packing in waiting'),
            ('delivery_in_waiting', 'Delivery in waiting'),
            ('waiting_send_customer', 'Waiting send customer'),
            ('receipt_in_waiting', 'Receipt in waiting'),
            ('waiting_invoice_creation', 'Waiting invoice creation'),
            ('waiting_customer_payment', 'Waiting customer payment'),
            ('lock', 'Lock'),
            ('cancel', 'Cancel'),
            ('unavailable_sf_state', 'Sensefly state unavailable'),
            ('waiting_freight_labelling', 'Freight labeling in waiting'),
            ('paid', 'Paid'),
        ],
        string='Sensefly state',
        compute='_compute_sf_state',
        default='unavailable_sf_state',
    )

    def check_number_of_picking(self, sale, nb_picking):
        if nb_picking == 3:
            return(
                len(sale.picking_ids.filtered(
                    lambda p: p.state != 'cancelled'
                )) == nb_picking
            )
        else:
            return(
                len(sale.picking_ids) == nb_picking
            )

    @api.multi
    def _compute_sf_state(self):

        for sale in self:
            # By default, we define Sensefly state unavailable
            sf_state = 'unavailable_sf_state'

            # Draft sale order
            if sale.state == 'draft':
                if not sale.carrier_id:
                    sf_state = 'waiting_delivery_method'
                else:
                    sf_state = 'waiting_send_quotation_to_customer'

            # Sent sale order
            elif sale.state == 'sent':
                sf_state = 'waiting_customer_confirmation'

            # Confirmed sale order
            elif sale.state == 'sale':

                # Sale order without procurement
                if not sale.picking_ids:
                    if sale.down_payment_required:
                        if sale.down_payment_missing:
                            sf_state = 'waiting_down_payment_creation'
                        else:
                            sf_state = 'waiting_down_payment_validation'

                # Sale order with procurement
                elif len(sale.picking_ids) == 3:
                    warehouse = sale.warehouse_id
                    pick_picking = sale.picking_ids.filtered(
                        lambda p: (
                            p.picking_type_id == warehouse.pick_type_id and
                            p.state != 'cancel'
                        )
                    )
                    pack_picking = sale.picking_ids.filtered(
                        lambda p: (
                            p.picking_type_id == warehouse.pack_type_id and
                            p.state != 'cancel'
                        )
                    )
                    customer_picking = sale.picking_ids.filtered(
                        lambda p: (
                            p.picking_type_id == warehouse.out_type_id and
                            p.state != 'cancel'
                        )
                    )

                    # We check we have pickings for Pick -> Pack -> Ship
                    if pick_picking and pack_picking and customer_picking:

                        # Waiting pick operation
                        if pick_picking.state == 'confirmed':
                            sf_state = 'waiting_reservation'

                        # Packing in waiting
                        elif pick_picking.state == 'assigned':
                            sf_state = 'packing_in_waiting'

                        elif pick_picking.state == 'done':
                            # Freight labelling waiting
                            if pack_picking.state == 'assigned':
                                sf_state = 'waiting_freight_labelling'

                            elif pack_picking.state == 'done':
                                # Waiting ship operation
                                if customer_picking.state == 'assigned':
                                    if not customer_picking.date_shipped:
                                        # Delivery in waiting
                                        if sale.rma_id:
                                            sf_state = 'delivery_in_waiting'
                                        # Waiting send customer
                                        else:
                                            sf_state = 'waiting_send_customer'
                                    # Receipt in waiting
                                    else:
                                        sf_state = 'receipt_in_waiting'

                        # Check invoices status only if all pickings are done
                        if all([p.state == 'done' for p in sale.picking_ids]):

                            # Sale order not fully invoiced
                            if sale.invoice_status != 'invoiced':
                                sf_state = 'waiting_invoice_creation'

                            # Waiting customer payment
                            elif sale.invoice_status == 'invoiced':
                                sf_state = 'waiting_customer_payment'

                            # Invoice paid
                            paid_conditions = (
                                sale.invoice_status == 'invoiced' and
                                all([
                                    i.state == 'paid'
                                    for i in sale.invoice_ids
                                ])
                            )
                            if paid_conditions:
                                sf_state = 'paid'

            # Done sale order
            elif sale.state == 'done':
                sf_state = 'lock'

            # Cancel sale order
            elif sale.state == 'cancel':
                sf_state = 'cancel'

            # Update Sensefly state
            sale.sf_state = sf_state
