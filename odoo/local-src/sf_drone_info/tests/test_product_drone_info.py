# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import MissingError


class TestProductDroneInfo(TransactionCase):
    def test_get_spare_parts_details(self):
        drone_type = self.env.ref('sf_drone_info.sf_drone_type01')
        partner = self.env.ref('sf_drone_info.sf_partner01')
        outcome = drone_type.get_spare_parts(partner.id)

        self.assertEqual(len(outcome), 1)
        self.assertEqual(outcome[0]['name_template'], 'eBee')
        self.assertEqual(outcome[0]['price'], 40.0)
        self.assertEqual(outcome[0]['currency'],
                         partner.property_product_pricelist.currency_id.name)

    def test_get_spare_parts_with_bad_partner_throw_exception(self):
        drone_type = self.env.ref('sf_drone_info.sf_drone_type01')
        with self.assertRaises(MissingError):
            drone_type.get_spare_parts(888888888888888)
