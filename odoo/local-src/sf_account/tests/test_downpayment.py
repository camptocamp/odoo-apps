# -*- coding: utf-8 -*-

from odoo.addons.account.tests.account_test_classes import AccountingTestCase

import time


class TestDownpaymentInvoice(AccountingTestCase):
    def setUp(self):
        super(AccountingTestCase, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']

        # setup down payment product
        vals = self.env['sale.advance.payment.inv']._prepare_deposit_product()
        self.downpay_product = self.env['product.product'].create(vals)
        self.env['ir.values'].sudo().set_default('sale.config.settings',
                                                 'deposit_product_id_setting',
                                                 self.downpay_product.id)

        # Create down payment invoice
        self.invoice = self.invoice_model.create({
            'partner_id': self.env.ref('base.res_partner_2').id,
            'reference_type': 'none',
            'currency_id': self.env.ref("base.CHF").id,
            'account_id': self.env.ref(
                'account.data_account_type_receivable').id,
            'type': 'out_invoice',
            'date_invoice': time.strftime('%Y') + '-12-31',
        })

        self.invoice_line_model.create({
            'product_id': self.downpay_product.id,
            'quantity': 1,
            'price_unit': 100,
            'invoice_id': self.invoice.id,
            'name': 'Down payment of 100.0%',
            'account_id': self.env.ref(
                'account.data_account_type_revenue').id
        })

    def test_downpay_invoice(self):
        self.invoice.invoice_validate()

        # Is a downpayment invoice
        self.assertTrue(self.invoice.is_down_pay_inv)

        # Using down payment sequence like Ayyyymmdd
        self.assertTrue(self.invoice.number.startswith('A'))
