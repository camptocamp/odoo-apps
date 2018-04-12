# -*- encoding: utf-8 -*-

from odoo import fields
from odoo.addons.account_asset_management.tests.test_account_asset_management \
    import TestAssetManagement


class SenseflyTestAssetManagement(TestAssetManagement):
    def test_compute_assets_with_aggregation(self):
        asset01 = self.env.ref(
            "account_asset_management.account_asset_vehicle0")
        asset02 = self.env.ref(
            "account_asset_management.account_asset_ict0")

        account_analytic = self.env.ref('analytic.analytic_our_super_product')
        asset01.account_analytic_id = account_analytic.id
        asset02.account_analytic_id = account_analytic.id

        tag = self.env.ref('analytic.tag_contract')
        asset01.analytic_tag_ids = [(6, 0, [tag.id])]
        asset02.analytic_tag_ids = [(6, 0, [tag.id])]

        asset01.validate()
        asset02.validate()
        asset01.compute_depreciation_board()
        asset02.compute_depreciation_board()

        # Depreciation lines
        dl = self.dl_model.search(
            [('asset_id', 'in', (asset01.id, asset02.id)),
             ('type', '=', 'depreciate')])

        move_id = dl.with_context(
            aggregate_move_lines=True,
            reference='Test assets computation with aggregation',
            journal_id=self.journal.id,
            date_end='2018-04-10'
        ).create_move()

        # we've got a single account move as expected
        self.assertIsInstance(move_id, int)
        move = self.env['account.move'].browse(move_id)

        self.assertEqual(move.ref,
                         'Test assets computation with aggregation')
        self.assertEqual(move.journal_id.id,
                         self.journal.id)
        move_lines = move.line_ids.filtered(lambda l: l.asset_id)
        for line in move_lines:
            # analytic account (Project) and analytic tag (Team)
            # assigned to move lines
            self.assertEqual(line.analytic_account_id, account_analytic)
            self.assertEqual(line.analytic_tag_ids.ids, [tag.id])
            # All move lines have assigned the last day of the month chosen
            # in the assets compute wizard
            self.assertEqual(line.date, '2018-04-30')

    def test_asset_compute_entries(self):
        """As a result of the computation of the assets entries,
        with context aggregation of move lines, we get a list with a single
        account move id
        """
        asset = self.env.ref(
            "account_asset_management.account_asset_vehicle0")

        today = fields.Date.today()
        move_ids = asset.with_context(
            aggregate_move_lines=True,
            reference='Test assets computation with aggregation',
            journal_id=self.journal.id)._compute_entries(today)

        self.assertIsInstance(move_ids, list)
        self.assertEqual(len(move_ids), 1)
