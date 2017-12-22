# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import odoo.tests.common as test_common


class TestToInvoiceStatus(test_common.TransactionCase):

    def setUp(self):
        super(TestToInvoiceStatus, self).setUp()
        Product = self.env['product.product']
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        partner = self.env.ref('base.res_partner_12')
        self.product = Product.create({
            'name': 'eWasp',
            'type': 'product',
            'uom_id': self.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'delivery',
        })
        self.product2 = Product.create({
            'name': 'eWasp 2017',
            'type': 'product',
            'uom_id': self.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'delivery',
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
        SaleOrderLine.create({
            'order_id': self.sale.id,
            'product_id': self.product2.id,
            'name': self.product.name,
            'product_uom_qty': 23,
            'product_uom': self.product.uom_id.id,
            'price_unit': 1337.0,
        })

    def test_to_invoice_status_to_invoice(self):
        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.action_confirm()

        self.sale.order_line[0].invoice_status = 'to invoice'
        self.sale.order_line[1].invoice_status = 'to invoice'
        self.sale._get_invoiced()
        self.assertEquals(self.sale.invoice_status, 'to invoice')

    def test_to_invoice_status_no(self):
        self.assertEquals(self.sale.invoice_status, 'no')

        self.sale.action_confirm()

        self.sale.order_line[0].invoice_status = 'to invoice'
        self.sale._get_invoiced()
        self.assertEquals(self.sale.invoice_status, 'no')

    def test_to_invoice_status_order_no(self):
        self.assertEquals(self.sale.invoice_status, 'no')
        self.product.invoice_policy = 'order'

        self.sale.action_confirm()

        self.sale.order_line[1].invoice_status = 'no'

        self.sale._get_invoiced()
        self.assertEquals(self.sale.invoice_status, 'no')

    def test_to_invoice_status_order_to_invoice(self):
        self.assertEquals(self.sale.invoice_status, 'no')
        self.product.invoice_policy = 'order'

        self.sale.action_confirm()

        self.sale.order_line[1].invoice_status = 'to invoice'

        self.sale._get_invoiced()
        self.assertEquals(self.sale.invoice_status, 'to invoice')
