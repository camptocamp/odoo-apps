# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo.tests import common
from odoo import fields
from datetime import datetime
import re


class TestInvitationKey(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestInvitationKey, cls).setUpClass()

        # Warehouse
        cls.warehouse = cls.env.ref('stock.warehouse0')
        cls.warehouse.write({'delivery_steps': 'pick_pack_ship'})
        cls.warehouse.pack_type_id.generate_invitation_key = True

        # Product
        Product = cls.env['product.product'].with_context(
            tracking_disable=True
        )
        cls.product1 = Product.create({
            'name': 'ebee plus',
            'type': 'product',
            'uom_id': cls.env.ref('product.product_uom_unit').id,
            'invoice_policy': 'delivery',
            'tracking': 'serial'
        })

        # Serial number
        Lot = cls.env['stock.production.lot'].with_context(
            tracking_disable=True
        )
        cls.lot_id = Lot.create({
            'name': 'xx-yy-zz',
            'product_id': cls.product1.id,
        })

        # Inventory
        inventory_wizard = cls.env['stock.change.product.qty'].with_context(
            tracking_disable=True
        ).create({
            'product_id': cls.product1.id,
            'new_quantity': 1.0,
            'location_id': cls.warehouse.lot_stock_id.id,
        })
        inventory_wizard.change_product_qty()

        # Sale Order
        SaleOrder = cls.env['sale.order'].with_context(
            tracking_disable=True
        )
        SaleOrderLine = cls.env['sale.order.line'].with_context(
            tracking_disable=True
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

    def test_assign_invitation_key(self):
        self.sale.state = 'sale'
        self.sale.confirmation_date = fields.Datetime.now()
        self.sale.order_line._action_procurement_create()

        # Pick step
        pick = self.sale.picking_ids.filtered(
            lambda p: p.picking_type_id.name == 'Pick'
        )
        pick.action_assign()

        for operation in pick.pack_operation_ids:
            self.env['stock.pack.operation.lot'].create({
                'operation_id': operation.id,
                'qty': 1,
                'lot_id': self.lot_id.id,
                'lot_name': self.lot_id.name,
            })
            operation.save()

        pick.do_new_transfer()

        self.assertFalse(pick.picking_type_id.generate_invitation_key)
        self.assertFalse(self.lot_id.invitation_key)

        # Pack step
        pack = self.sale.picking_ids.filtered(
            lambda p: p.picking_type_id.name == 'Pack'
        )
        pack.picking_type_id.generate_invitation_key = True

        pack.action_assign()
        pack.do_new_transfer()

        p = re.compile('[0-9]{4}-[0-9]{4}')
        self.assertTrue(p.match(self.lot_id.invitation_key))
