# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo.tests import common
from odoo import fields
from datetime import datetime


class TestCommercialInvoice(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestCommercialInvoice, cls).setUpClass()

        # Warehouse
        cls.warehouse = cls.env.ref('stock.warehouse0')
        cls.warehouse.write({'delivery_steps': 'pick_pack_ship'})

        # Product
        Product = cls.env['product.product'].with_context(
            {'tracking_disable': True}
        )
        cls.product1 = Product.create({
            'name': 'ebee plus',
            'type': 'product',
            'uom_id': cls.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'delivery',
            'tracking': 'serial'
        })

        cls.product2 = Product.create({
            'name': 'Fedex International',
            'type': 'service',
            'uom_id': cls.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'order',
        })

        # Serial number
        Lot = cls.env['stock.production.lot'].with_context(
            {'tracking_disable': True}
        )
        cls.lot_id = Lot.create({
            'name': 'xx-yy-zz',
            'product_id': cls.product1.id,
        })

        # Inventory
        inventory_wizard = cls.env['stock.change.product.qty'].with_context(
            {'tracking_disable': True}
        )
        inventory_wizard.create({
            'filter': 'lot',
            'product_id': cls.product1.id,
            'new_quantity': 1.0,
            'location_id': cls.warehouse.lot_stock_id.id,
        })
        inventory_wizard.change_product_qty()

        # Sale Order
        SaleOrder = cls.env['sale.order'].with_context(
            {'tracking_disable': True}
        )
        SaleOrderLine = cls.env['sale.order.line'].with_context(
            {'tracking_disable': True}
        )
        partner = cls.env.ref('base.res_partner_12')
        cls.sale = SaleOrder.create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'date_order': datetime.today(),
            'pricelist_id': cls.env.ref('product.list0').id,
            'warehouse_id': cls.warehouse.id,
            'ignore_exception': True
        })
        SaleOrderLine.create({
            'order_id': cls.sale.id,
            'product_id': cls.product1.id,
            'name': cls.product1.name,
            'product_uom_qty': 1.0,
            'product_uom': cls.product1.uom_id.id,
            'price_unit': 1000.0,
        })

        SaleOrderLine.create({
            'order_id': cls.sale.id,
            'product_id': cls.product2.id,
            'name': cls.product2.name,
            'product_uom_qty': 1.0,
            'product_uom': cls.product2.uom_id.id,
            'price_unit': 20.0,
        })

        cls.ci = cls.env['commercial.invoice']

    def test_commercial_invoice(self):
        self.sale.state = 'sale'
        self.sale.confirmation_date = fields.Datetime.now()
        self.sale.order_line._action_procurement_create()

        pick = self.sale.picking_ids.filtered(
            lambda p: p.picking_type_id.name == 'Pick'
        )
        pick.force_assign()

        for operation in pick.pack_operation_ids:
            self.env['stock.pack.operation.lot'].with_context(
                {'tracking_disable': True}
            ).create({
                'operation_id': operation.id,
                'qty': 1,
                'lot_id': self.lot_id.id,
                'lot_name': self.lot_id.name,
            })
            operation.save()

        pick.do_new_transfer()

        for order_line in self.sale:
            for stock_move in pick.move_lines:
                stock_move.sale_line_id = order_line.id
                stock_move.refresh()

        sale = self.ci.with_context(pick_id=pick.id).get_sale_order()
        self.assertEqual(self.sale, sale)

        lines = self.ci.get_commercial_invoice_lines(sale, pick)
        self.assertEqual(self.sale.order_line[0], lines[0]['order_line'])
        self.assertEqual(self.lot_id, lines[0]['serial_numbers'])
        self.assertIsNotNone(lines[0]['pack_operation'])
        self.assertEqual(self.sale.order_line[1], lines[1]['order_line'])

        self.assertEqual(
            self.ci.get_order_line_delivered_qty(
                self.sale.order_line[0], pick
            ), 1)
        self.assertEqual(
            self.ci.get_order_line_delivered_qty(
                self.sale.order_line[0], pick
            ), 1)
