# -*- encoding: utf-8 -*-

from odoo import api, fields, models


class AssetDepreciationConfirmationWizard(models.TransientModel):
    _inherit = "asset.depreciation.confirmation.wizard"

    @api.multi
    def asset_compute(self):
        asset_compute_context = dict(self.env.context or {})
        if self.aggregate_move_lines:
            asset_compute_context.update(
                {'aggregate_move_lines': self.aggregate_move_lines,
                 'reference': self.reference,
                 'journal_id': self.journal_id.id
                 }
            )
        return super(
            AssetDepreciationConfirmationWizard,
            self.with_context(asset_compute_context)
        ).asset_compute()

    reference = fields.Char(
        string='Reference',
        help="This is the reference that will be given to the journal item.")
    aggregate_move_lines = fields.Boolean(
        string='Aggregate',
        default=True,
        help="All computed depreciation entries will be aggregated in a "
             "single journal entry.")
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        help="This journal will be used in the aggregated journal entry"
    )
