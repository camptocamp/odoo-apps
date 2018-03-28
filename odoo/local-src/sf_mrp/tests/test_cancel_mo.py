# -*- coding: utf-8 -*-
from odoo.tests import common
from odoo.exceptions import UserError


@common.at_install(False)
@common.post_install(True)
class TestCancelMO(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestCancelMO, cls).setUpClass()
        cls.source_location_id = cls.env.ref('stock.stock_location_14').id
        cls.env.user.write(
            {'groups_id': [(4, cls.env.ref('sf_mrp.group_mrp_cancel_mo').id)]})

        unit = cls.env.ref("product.product_uom_unit").id
        cls.custom_laptop = cls.env.ref("product.product_product_27")
        cls.custom_laptop.tracking = 'lot'

        # Create new product charger and keybord
        cls.product_charger = cls.env['product.product'].create({
            'name': 'Charger',
            'type': 'product',
            'tracking': 'lot',
            'uom_id': unit,
            'uom_po_id': unit})
        cls.product_keybord = cls.env['product.product'].create({
            'name': 'Usb Keybord',
            'type': 'product',
            'tracking': 'lot',
            'uom_id': unit,
            'uom_po_id': unit})

        # Create bill of material for customized laptop.
        bom_custom_laptop = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.custom_laptop.product_tmpl_id.id,
            'product_qty': 10,
            'product_uom_id': unit,
            'bom_line_ids': [(0, 0, {
                'product_id': cls.product_charger.id,
                'product_qty': 20,
                'product_uom_id': unit
            }), (0, 0, {
                'product_id': cls.product_keybord.id,
                'product_qty': 20,
                'product_uom_id': unit
            })]
        })

        # Create production order for customize laptop.
        cls.mo_custom_laptop = cls.env['mrp.production'].create({
            'product_id': cls.custom_laptop.id,
            'product_qty': 10,
            'product_uom_id': unit,
            'bom_id': bom_custom_laptop.id})

        # Assign component to production order.
        cls.mo_custom_laptop.action_assign()

        # Create lots
        lot_charger = cls.env['stock.production.lot'].create(
            {'product_id': cls.product_charger.id})
        lot_keybord = cls.env['stock.production.lot'].create(
            {'product_id': cls.product_keybord.id})

        # Inventory Init
        cls.inventory = cls.env['stock.inventory'].create({
            'name': 'Inventory Product Table',
            'filter': 'partial',
            'line_ids': [(0, 0, {
                'product_id': cls.product_charger.id,
                'product_uom_id': cls.product_charger.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_charger.id,
                'location_id': cls.source_location_id
            }), (0, 0, {
                'product_id': cls.product_keybord.id,
                'product_uom_id': cls.product_keybord.uom_id.id,
                'product_qty': 20,
                'prod_lot_id': lot_keybord.id,
                'location_id': cls.source_location_id
            })]
        })
        cls.inventory.action_done()

        # Assign products
        cls.mo_custom_laptop.action_assign()

        # Start production of 6 laptops
        context = {"active_ids": [cls.mo_custom_laptop.id],
                   "active_id": cls.mo_custom_laptop.id}
        product_consume = cls.env['mrp.product.produce'].with_context(
            context).create({'product_qty': 6.00})
        cls.laptop_lot_001 = cls.env['stock.production.lot'].create(
            {'product_id': cls.custom_laptop.id})
        product_consume.lot_id = cls.laptop_lot_001.id
        product_consume.consume_line_ids.write({'quantity_done': 12})
        product_consume.do_produce()
        cls.mo_custom_laptop.post_inventory()

    def _create_move(self, product, src_location, dst_location, **values):
        Move = self.env['stock.move']
        # simulate create + onchange
        move = Move.new(
            {'product_id': product.id, 'location_id': src_location.id,
             'location_dest_id': dst_location.id})
        move.onchange_product_id()
        move_values = move._convert_to_write(move._cache)
        move_values.update(**values)
        return Move.create(move_values)

    def test_cancel_mo_user_group(self):
        self.env.user.write(
            {'groups_id': [(3, self.env.ref('sf_mrp.group_mrp_cancel_mo').id)]}
        )
        with self.assertRaises(UserError):
            self.mo_custom_laptop.button_cancel_mo()

    def test_cancel_mo(self):
        raw_product_loc = self.env['product.product'].with_context(
            location=self.mo_custom_laptop.location_src_id.id)
        finished_product_loc = self.env['product.product'].with_context(
            location=self.mo_custom_laptop.location_dest_id.id)

        laptop_qty = finished_product_loc.browse(
            self.custom_laptop.id).qty_available
        keyboard_qty = raw_product_loc.browse(
            self.product_keybord.id).qty_available
        charger_qty = raw_product_loc.browse(
            self.product_keybord.id).qty_available
        # Initial stock of laptops: 85, produced qty: 6
        self.assertEqual(laptop_qty, 91)
        self.assertEqual(keyboard_qty, 8)
        self.assertEqual(charger_qty, 8)

        self.mo_custom_laptop.button_cancel_mo()

        laptop_qty = finished_product_loc.browse(
            self.custom_laptop.id).qty_available
        keyboard_qty = raw_product_loc.browse(
            self.product_keybord.id).qty_available
        charger_qty = raw_product_loc.browse(
            self.product_keybord.id).qty_available
        self.assertEqual(laptop_qty, 85)
        self.assertEqual(keyboard_qty, 20)
        self.assertEqual(charger_qty, 20)

    # TODO: Fix test
    # def test_cancel_mo_finished_product_moved(self):
    #     # Move some finished products to another location
    #     out_move = self._create_move(
    #         self.custom_laptop,
    #         self.mo_custom_laptop.location_dest_id,
    #         self.env.ref('stock.stock_location_customers'),
    #         product_uom_qty=2
    #     )
    #     out_move.action_assign()
    #     out_move.action_done()
    #     with self.assertRaises(UserError):
    #         self.mo_custom_laptop.button_cancel_mo()
    #
    #     # Return the previous products in stock
    #     in_move = self._create_move(
    #         self.custom_laptop,
    #         self.env.ref('stock.stock_location_customers'),
    #         self.mo_custom_laptop.location_dest_id,
    #         product_uom_qty=2
    #     )
    #     in_move.action_assign()
    #     in_move.action_done()
    #     self.mo_custom_laptop.button_cancel_mo()
