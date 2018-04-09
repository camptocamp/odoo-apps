# -*- coding: utf-8 -*-

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestAccountMove(AccountingTestCase):
    def setUp(self):
        super(TestAccountMove, self).setUp()

    def test_onchange_account_move_date(self):
        """Tests that onchange account move date,
        move lines have date updated."""

        journal = self.env['account.journal'].search([('type', '=', 'bank')],
                                                     limit=1)
        account_recv = self.env.ref(
            'account.data_account_type_receivable')
        account_type_rev = self.env.ref(
            'account.data_account_type_revenue')

        move = self.env['account.move'].create({
            'date': '2018-04-09',
            'journal_id': journal.id,
            'line_ids': [
                (0, 0, {
                    'name': "Debit line",
                    'account_id': account_recv.id,
                    'debit': 100.0,
                }),
                (0, 0, {
                    'name': "Credit line 1",
                    'account_id': account_recv.id,
                    'credit': 50.0,
                }),
                (0, 0, {
                    'name': "Credit line 1",
                    'account_id': account_type_rev.id,
                    'credit': 50.0,
                }),
            ]
        })

        move.date = '2018-04-10'
        move._onchange_date()
        self.assertTrue(
            all(line.date == '2018-04-10' for line in move.line_ids)
        )
