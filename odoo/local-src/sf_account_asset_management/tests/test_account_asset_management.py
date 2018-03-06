# -*- encoding: utf-8 -*-

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

        asset_compute_context = dict(self.env.context or {})
        asset_compute_context.update(
            {'aggregate_move_lines': True,
             'reference': 'Test assets computation with aggregation',
             'journal_id': self.journal.id
             }
        )

        # Depreciation lines
        dl = self.dl_model.search(
            [('asset_id', 'in', (asset01.id, asset02.id)),
             ('type', '=', 'depreciate')])

        move_id = dl.with_context(asset_compute_context).create_move()

        # we've got a single account move as expected
        self.assertIsInstance(move_id, int)
        move = self.env['account.move'].browse(move_id)

        self.assertEqual(move.ref,
                         asset_compute_context['reference'])
        self.assertEqual(move.journal_id.id,
                         asset_compute_context['journal_id'])

        # analytic account (Project) and analytic tag (Team)
        # assigned to move lines
        for line in move.line_ids.filtered(lambda l: l.asset_id):
            self.assertEqual(line.analytic_account_id, account_analytic)
            self.assertEqual(line.analytic_tag_ids.ids, [tag.id])
