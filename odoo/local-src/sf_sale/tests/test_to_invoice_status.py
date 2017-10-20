# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

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
        self.sale = SaleOrder.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'date_order': datetime.today(),
            'pricelist_id': self.env.ref('product.list0').id
        })
        SaleOrderLine.create({
            'order_id': self.sale.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 42,
            'product_uom': self.product.uom_id.id,
            'price_unit': 1337.0,
        })

    def test_to_invoice_status_order_policy(self):
        """ Testing To Invoice status for order invoice policy."""
        self.product.invoice_policy = 'order'

        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.action_confirm()

        self.assertEquals(self.sale.order_line.qty_to_invoice, 42.0)
        self.assertEquals(self.sale.invoice_status, 'to invoice')

    def test_to_invoice_status_delivery_policy(self):
        """ Testing To Invoice status for delivery invoice policy."""
        self.product.invoice_policy = 'delivery'

        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.action_confirm()

        self.assertFalse(self.sale.order_line.qty_to_invoice)
        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.order_line.qty_delivered = 20

        self.assertFalse(self.sale.order_line.qty_to_invoice)
        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.order_line.qty_delivered = 42

        self.assertEquals(self.sale.order_line.qty_to_invoice, 42.0)
        self.assertEquals(self.sale.invoice_status, 'to invoice')
