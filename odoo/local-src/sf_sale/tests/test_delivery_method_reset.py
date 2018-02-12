# -*- coding: utf-8 -*-
# Part of sensefly.


from datetime import datetime

import odoo.tests.common as test_common


class TestSale(test_common.TransactionCase):

    def setUp(self):
        super(TestSale, self).setUp()
        Product = self.env['product.product']
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        partner = self.env.ref('base.res_partner_12')
        self.product = Product.create({
            'name': 'eWasp',
            'type': 'product',
            'uom_id': self.env.ref('product.product_uom_unit').id,
        })
        self.service = Product.create({
            'name': 'service aws',
            'type': 'service',
        })

        self.sale = SaleOrder.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'date_order': datetime.today(),
            'pricelist_id': self.env.ref('product.list0').id,
            'carrier_id': self.env.ref('delivery.free_delivery_carrier').id,
            'ignore_exception': True
        })

        SaleOrderLine.create({
            'order_id': self.sale.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 2,
            'product_uom': self.product.uom_id.id,
            'price_unit': 123,
        })

        SaleOrderLine.create({
            'order_id': self.sale.id,
            'product_id': self.service.id,
            'name': self.service.name,
            'product_uom_qty': 1,
            'price_unit': 100,
        })

    def test_create_sale_line_reset_delivery_method(self):
        # Add service line
        self.sale.order_line = [(0, 0, {
            'product_id': self.service.id,
            'name': self.service.name,
            'product_uom_qty': 1,
            'price_unit': 20,

        })]
        self.assertIsNotNone(self.sale.carrier_id)

        # Add physical product line
        self.sale.order_line = [(0, 0, {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'price_unit': 30,

        })]
        self.assertFalse(self.sale.carrier_id)

    def test_update_sale_line_reset_delivery_method(self):
        # Update service line
        service_line = self.sale.order_line.filtered(
            lambda l: l.product_id.type == 'service'
        )
        self.sale.write(
            {'order_line': [(1, service_line.id, {'product_uom_qty': 21})]}
        )
        self.assertIsNotNone(self.sale.carrier_id)

        # Update physical product line
        product_line = self.sale.order_line.filtered(
            lambda l: l.product_id.type == 'product'
        )
        self.sale.write(
            {'order_line': [(1, product_line.id, {'product_uom_qty': 21})]}
        )
        self.assertFalse(self.sale.carrier_id)

    def test_delete_sale_line_reset_delivery_method(self):
        # Delete service line
        service_line = self.sale.order_line.filtered(
            lambda l: l.product_id.type == 'service'
        )
        self.sale.write(
            {'order_line': [[2, service_line.id, False]]}
        )
        self.assertIsNotNone(self.sale.carrier_id)

        # Update physical product line
        product_line = self.sale.order_line.filtered(
            lambda l: l.product_id.type == 'product'
        )
        self.sale.write(
            {'order_line': [(2, product_line.id, False)]}
        )
        self.assertFalse(self.sale.carrier_id)
