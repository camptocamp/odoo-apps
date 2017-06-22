# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestMySenseFlyInterface(TransactionCase):
    def test_interface_call_with_get_spare_parts(self):
        drone_type = self.env.ref('sf_drone_info.sf_drone_type01')
        partner = self.env.ref('sf_drone_info.sf_partner01')
        outcome = \
            self.env['sf.mysensefly.interface'].call(
                'get_spare_parts', [drone_type.id, partner.id])
        self.assertEqual(len(outcome), 1)
