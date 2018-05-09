# -*- coding: utf-8 -*-
# Part of SenseFly.

from odoo import models
from itertools import groupby


class CommercialInvoice(models.AbstractModel):
    _name = "commercial.invoice"
    description = "Commercial invoice report"

    def get_sale_order(self):
        order = None
        picking_id = self.env.context.get('pick_id')
        if picking_id:
            pick = self.env['stock.picking'].browse(picking_id)
            order = pick.procurement_group_sale_id
        return order

    def get_address_name_lines(self, sale):
        address = {}
        # Invoicing address
        partner_invoice = sale.partner_invoice_id
        company_name = partner_invoice.commercial_company_name
        l1 = partner_invoice.commercial_company_name or partner_invoice.name
        l2 = ''
        if company_name != partner_invoice.name:
            l2 = partner_invoice.name
        address['invoicing'] = {
            'line1': l1,
            'line2': l2
        }

        # Shipping address
        partner_shipping = sale.partner_shipping_id
        l1 = partner_shipping.commercial_company_name or partner_shipping.name
        l2 = ''
        if partner_shipping.commercial_company_name != partner_shipping.name:
            l2 = partner_shipping.name

        address['shipping'] = {
            'line1': l1,
            'line2': l2
        }
        return address

    def display_discount(self, sale):
        return any(order_line.discount for order_line in sale.order_line)

    def get_order_line_serial_numbers(self, order_line, picking):
        serial_numbers = self.env['stock.production.lot']
        for move in picking.move_lines:
            if (move.lot_ids and
                move.sale_line_id and
                    move.sale_line_id.id == order_line.id):
                serial_numbers |= move.lot_ids
        return serial_numbers

    def get_order_line_delivered_qty(self, order_line, picking):
        if order_line.product_id.type == 'service':
            return order_line.product_uom_qty
        else:
            return sum(
                move.product_uom_qty for move in picking.move_lines
                if move.sale_line_id and move.sale_line_id.id == order_line.id
                and move.state in ('assigned', 'done')
            )

    def get_order_line_delivered_qty_price(self, order_line, delivered_qty):
        if order_line.product_id.type == 'service':
            return order_line.product_uom_qty * order_line.price_unit
        else:
            return (delivered_qty *
                    order_line.price_subtotal /
                    order_line.product_uom_qty)

    def get_adv_pay_product(self):
        """Deposit product"""
        return self.env['sale.advance.payment.inv'].\
            _default_product_id()

    def get_commercial_invoice_lines(self, sale, picking):
        lines = []
        deposit_product = self.get_adv_pay_product()
        for order_line in sale.order_line:
            product_service = order_line.product_id.type == 'service'
            product_deposit = order_line.product_id == deposit_product
            if (product_service and
                    not product_deposit and not picking.backorder_id):
                lines.append(
                    {'order_line': order_line}
                )

            for pack_operation in picking.pack_operation_ids:
                if order_line.id in pack_operation.sale_line_ids.ids:
                    lines.append(
                        {'order_line': order_line,
                         'serial_numbers':
                             self.get_order_line_serial_numbers(
                                 order_line, picking),
                         'pack_operation': pack_operation}
                    )
        return lines

    def get_order_lines_layouted(self, sale, picking):
        ci_lines = self.get_commercial_invoice_lines(sale, picking)
        report_pages = [[]]
        for category, lines in groupby(
                ci_lines, lambda l: l['order_line'].layout_category_id):
            # If last added category induced a pagebreak, this one will be
            # on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Other',
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        return report_pages

    def get_total_amounts(self, sale, picking):
        amounts = {
            'subtotal': 0.0,
            'tax': 0.0,
            'total': 0.0
        }

        deposit_product = self.get_adv_pay_product()

        for move in picking.move_lines:
            if (move.sale_line_id.product_uom_qty and
                    move.state in ('assigned', 'done')):
                qty = move.product_uom_qty / move.sale_line_id.product_uom_qty
                amounts['subtotal'] += move.sale_line_id.price_subtotal * qty
                amounts['tax'] += move.sale_line_id.price_tax * qty
                amounts['total'] += move.sale_line_id.price_total * qty
        for order_line in sale.order_line:
            if (order_line.product_id.type == 'service' and
                    not order_line.product_id == deposit_product and
                    not picking.backorder_id):
                amounts['subtotal'] += order_line.price_subtotal
                amounts['tax'] += order_line.price_tax
                amounts['total'] += order_line.price_total
        return amounts
