# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestRMA(TransactionCase):

    def setUp(self):
        super(TestRMA, self).setUp()
        self.drone = self.env['product.product'].create({
            'name': 'eBee',
        })
        self.lot = self.env['stock.production.lot'].create({
            'name': 'eBee123',
            'product_id': self.drone.id,
        })
        self.rma = self.env['sf.rma'].create({
            'partner_id': self.env.ref('base.res_partner_12').id,
            'product_id': self.drone.id,
            'zendesk_ref': '99999',
        })

    def test_rma_sequence(self):
        self.assertEquals(self.rma.name[:3], 'RMA')

    def test_rma_validation(self):
        """Create a RMA and validate it

        Check all relation have been corectly created

        Receive product

        """
        self.rma.to_receive = True

        self.assertEquals(self.rma.state, 'draft')
        self.assertEquals(self.rma.repair_count, 0)
        self.assertEquals(self.rma.picking_count, 0)
        self.assertEquals(self.rma.sale_count, 0)

        self.rma.action_open()

        self.assertEquals(self.rma.state, 'open')
        self.assertEquals(self.rma.repair_count, 1)
        self.assertEquals(self.rma.picking_count, 1)
        self.assertEquals(self.rma.sale_count, 1)

        self.assertEquals(self.rma.repair_ids.product_id,
                          self.rma.product_id)
        self.assertEquals(self.rma.repair_ids.partner_id,
                          self.rma.partner_id)
        self.assertEquals(self.rma.repair_ids.lot_id,
                          self.rma.lot_id)

        self.assertEquals(self.rma.picking_ids.partner_id,
                          self.rma.partner_id)
        self.assertEquals(self.rma.picking_ids.move_lines.product_id,
                          self.rma.product_id)

        self.assertEquals(self.rma.sale_ids.partner_id,
                          self.rma.partner_id)
        self.assertEquals(self.rma.sale_ids.pricelist_id,
                          self.env.ref('sf_rma.pricelist_rma'))
        self.assertEquals(self.rma.sale_ids.team_id,
                          self.env.ref('sf_rma.crm_team_rma'))
        self.assertEquals(self.rma.sale_ids.order_line.product_id,
                          self.rma.product_id)

    def test_rma_validation_no_picking(self):
        """Create a RMA and validate it

        Check all relation have been corectly created

        Don't receive product

        """
        self.rma.to_receive = False

        self.assertEquals(self.rma.state, 'draft')
        self.assertEquals(self.rma.repair_count, 0)
        self.assertEquals(self.rma.picking_count, 0)
        self.assertEquals(self.rma.sale_count, 0)

        self.rma.action_open()

        self.assertEquals(self.rma.state, 'open')
        self.assertEquals(self.rma.repair_count, 1)
        self.assertEquals(self.rma.picking_count, 0)
        self.assertEquals(self.rma.sale_count, 1)

        self.assertEquals(self.rma.repair_ids.product_id,
                          self.rma.product_id)
        self.assertEquals(self.rma.repair_ids.partner_id,
                          self.rma.partner_id)
        self.assertEquals(self.rma.repair_ids.lot_id,
                          self.rma.lot_id)

        self.assertEquals(self.rma.sale_ids.partner_id,
                          self.rma.partner_id)
        self.assertEquals(self.rma.sale_ids.pricelist_id,
                          self.env.ref('sf_rma.pricelist_rma'))
        self.assertEquals(self.rma.sale_ids.team_id,
                          self.env.ref('sf_rma.crm_team_rma'))
        self.assertEquals(self.rma.sale_ids.order_line.product_id,
                          self.rma.product_id)

    def test_rma_cancel_reset(self):
        """Create a RMA and cancel it and reset it

        """
        self.assertEquals(self.rma.state, 'draft')
        self.rma.action_close()
        self.assertEquals(self.rma.state, 'closed')
        self.rma.action_reset()
        self.assertEquals(self.rma.state, 'draft')
