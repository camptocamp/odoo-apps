# -*- coding: utf-8 -*-
# Part of sensefly.

import odoo.tests.common as test_common

from datetime import datetime


class TestSale(test_common.TransactionCase):
    def setUp(self):
        super(TestSale, self).setUp()

        # Warehouse
        self.warehouse = self.env.ref('stock.warehouse0')

        # Product
        Product = self.env['product.product']
        self.product = Product.create({
            'name': 'eWasp',
            'type': 'product',
            'uom_id': self.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'delivery',
            'tracking': 'serial'
        })

        # Serial number
        Lot = self.env['stock.production.lot']
        self.lot_id = Lot.create({
            'name': 'xx-yy-zz',
            'product_id': self.product.id,
        })

        # Inventory
        inventory_wizard = self.env['stock.change.product.qty'].create({
            'filter': 'lot',
            'lot_id': self.lot_id.id,
            'product_id': self.product.id,
            'new_quantity': 1.0,
            'location_id': self.warehouse.lot_stock_id.id,
        })
        inventory_wizard.change_product_qty()

        # Sale Order
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        partner = self.env.ref('base.res_partner_12')
        self.sale = SaleOrder.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'date_order': datetime.today(),
            'pricelist_id': self.env.ref('product.list0').id,
            'warehouse_id': self.warehouse.id,
            'ignore_exception': True
        })
        SaleOrderLine.create({
            'order_id': self.sale.id,
            'product_id': self.product.id,
            'name': self.product.name,
            'lot_id': self.lot_id.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 1000.0,
        })

    def test_sale_confirm_with_3steps(self):
        # With warehouse 'Pick + Pack + Ship' configuration
        # 3 stock pickings are created on SO confirmation
        self.warehouse.write({'delivery_steps': 'pick_pack_ship'})
        self.sale.action_confirm()
        self.assertEqual(len(self.sale.picking_ids), 3)

    def test_sale_cancel_and_reconfirm_with_3steps(self):
        # With warehouse 'Pick + Pack + Ship' configuration
        # We are able to cancel order and reconfirm it
        self.warehouse.write({'delivery_steps': 'pick_pack_ship'})
        self.sale.action_confirm()
        self.sale.action_cancel()
        self.assertEqual(len(self.sale.picking_ids), 3)
        self.sale.action_draft()
        self.sale.action_confirm()
        self.assertEqual(len(self.sale.picking_ids), 3)

    def test_sale_confirm_with_2steps(self):
        # With warehouse 'Pick + Ship' configuration
        # 2 stock pickings are created on SO confirmation
        self.warehouse.write({'delivery_steps': 'pick_ship'})
        self.sale.action_confirm()
        self.assertEqual(len(self.sale.picking_ids), 2)

    def test_sale_confirm_with_1steps(self):
        # With warehouse 'Ship directly from stock' configuration
        # 1 stock pickings are created on SO confirmation
        self.warehouse.write({'delivery_steps': 'ship_only'})
        self.sale.action_confirm()
        self.assertEqual(len(self.sale.picking_ids), 1)

    def test_sale_confirm_with_3steps_and_pay_before_delivery(self):
        # With warehouse 'Pick + Pack + Ship' configuration
        # and payment term that requires down payment
        payment_term = self.env.ref('account.account_payment_term_immediate')
        payment_term.down_payment_required = True
        self.sale.payment_term_id = payment_term.id
        self.sale.action_confirm()

        # When payment term requires down payment.
        # There's no stock picking(s) after order confirm
        self.assertEqual(len(self.sale.picking_ids), 0)
