# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.sf_rma.tests.test_rma import TestRMA


class TestRmaMrpRepair(TestRMA):
    def test_rma_repair_with_decision_change(self):
        """
        Test repair on change rma decision
        """
        # Open RMA
        self.rma.to_receive = True
        self.rma.decision = 'to_invoice'
        self.rma.action_open()

        # Receive Drone
        self.rma.picking_ids.do_new_transfer()

        # Repair to analyse
        self.rma.repair_ids.action_repair_to_analyze()
        # Repair to quotation
        self.rma.repair_ids.action_repair_to_quotation()

        # Now we change the decision and start the repair order
        self.rma.decision = 'free'
        self.rma.repair_ids.action_repair_to_repair()

        self.assertEquals(self.rma.repair_ids.state, 'under_repair')
