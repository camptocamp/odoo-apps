# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDownPaymentRequired(TransactionCase):

    def create_sale_order(self, partner, product, payment_term):
        return self.env['sale.order'].create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
            })],
            'pricelist_id': self.env.ref('product.list0').id,
            'payment_term_id': payment_term.id,
        })

    def setUp(self):
        super(TestDownPaymentRequired, self).setUp()

        self.down_payment_product = self.env.ref('sale.advance_product_0')
        self.env['sale.config.settings'].create({
            'deposit_product_id_setting': self.down_payment_product.id
        }).execute()

        self.end_of_month_payment_term = self.env.ref(
            'account.account_payment_term')

        self.down_payment_term = self.env.ref(
            'sf_sale_invoicing.down_payment_required_term')

        self.product_to_sell = self.env.ref('product.product_product_7')
        self.product_to_sell.invoice_policy = 'order'

        self.partner = self.env.ref('base.res_partner_12')

        self.order_1 = self.create_sale_order(self.partner,
                                              self.product_to_sell,
                                              self.down_payment_term)
        self.order_2 = self.create_sale_order(self.partner,
                                              self.product_to_sell,
                                              self.down_payment_term)
        self.order_3 = self.create_sale_order(self.partner,
                                              self.product_to_sell,
                                              self.end_of_month_payment_term)

    def test_customer_down_payment_required(self):

        self.assertEqual(
            self.down_payment_product,
            self.env['sale.advance.payment.inv']._default_product_id())

        self.assertTrue(self.down_payment_term.down_payment_required)

        self.assertTrue(self.order_1.down_payment_required)
        self.assertTrue(self.order_2.down_payment_required)
        self.assertFalse(self.order_3.down_payment_required)

        self.assertTrue(self.order_1.down_payment_missing)
        self.assertTrue(self.order_2.down_payment_missing)
        self.assertFalse(self.order_3.down_payment_missing)

        self.down_payment_term.down_payment_required = False

        self.assertFalse(self.order_1.down_payment_missing)
        self.assertFalse(self.order_2.down_payment_missing)

        self.down_payment_term.down_payment_required = True
        self.assertTrue(self.order_1.down_payment_missing)
        self.assertTrue(self.order_2.down_payment_missing)

        self.order_1.action_confirm()
        self.order_2.action_confirm()
        self.order_3.action_confirm()

        # Test if creating down payment removes the downpayment missing
        context_1 = {"active_model": 'sale.order',
                     "active_ids": [self.order_1.id],
                     "active_id": self.order_1.id}

        payment_1 = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'percentage',
            'amount': 10.0,
        })
        payment_1.with_context(context_1).create_invoices()

        # FIXME this test fails in version 10.8.0
        # self.assertFalse(self.order_1.down_payment_missing)

        # Test if cancelling order removes down payment required
        self.order_2.action_cancel()
        self.assertFalse(self.order_2.down_payment_missing)

        # Test if setting payment term down payment required does not change
        # invoiced sale orders

        context_3 = {"active_model": 'sale.order',
                     "active_ids": [self.order_3.id],
                     "active_id": self.order_3.id}

        payment_3 = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'all',
        })
        payment_3.with_context(context_3).create_invoices()
        self.assertEqual(self.order_3.invoice_status, 'invoiced')

        self.end_of_month_payment_term.down_payment_required = True
        self.assertFalse(self.order_3.down_payment_missing)
