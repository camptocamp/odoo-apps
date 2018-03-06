# -*- coding: utf-8 -*-

import time
from odoo import models, api


class AccountAssetLine(models.Model):
    _inherit = "account.asset.line"

    @api.multi
    def _setup_move_line_data(self, depreciation_date, account_id, type,
                              move_id):

        # No aggregation. Just call super()
        if not self.env.context.get('aggregate_move_lines'):
            return super(AccountAssetLine, self)._setup_move_line_data(
                depreciation_date, account_id, type, move_id)

        self.ensure_one()
        asset = self.asset_id
        amount = self.amount
        analytic_id = False
        analytic_tag_ids = []

        if type == 'depreciation':
            debit = amount < 0 and -amount or 0.0
            credit = amount > 0 and amount or 0.0
        elif type == 'expense':
            debit = amount > 0 and amount or 0.0
            credit = amount < 0 and -amount or 0.0
            analytic_id = asset.account_analytic_id.id
            analytic_tag_ids = asset.analytic_tag_ids.ids

        move_line_data = {
            'name': asset.name,
            'move_id': move_id,
            'account_id': account_id,
            'credit': credit,
            'debit': debit,
            'partner_id': asset.partner_id.id,
            'analytic_account_id': analytic_id,
            'analytic_tag_ids': [(6, 0, analytic_tag_ids)],
            'asset_id': asset.id if type == 'expense' else False,
        }
        return move_line_data

    @api.multi
    def create_move(self):
        # No aggregation. Just call super()
        if not self.env.context.get('aggregate_move_lines'):
            return super(AccountAssetLine, self).create_move()

        asset_obj = self.env['account.asset']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        asset_ids = []

        # Create single account move
        move = move_obj.create(
            {
                'ref': self.env.context['reference'],
                'date': time.strftime('%Y-%m-%d'),
                'journal_id': self.env.context['journal_id']
             }
        )

        for line in self:
            asset = line.asset_id
            if asset.method_time == 'year':
                depreciation_date = self.env.context.get(
                    'depreciation_date') or line.line_date
            else:
                depreciation_date = self.env.context.get(
                    'depreciation_date') or time.strftime('%Y-%m-%d')

            depr_acc_id = asset.profile_id.account_depreciation_id.id
            exp_acc_id = asset.profile_id.account_expense_depreciation_id.id
            move_line_obj = move_line_obj.with_context(allow_asset=True)

            move_line_obj.with_context(check_move_validity=False).create(
                line._setup_move_line_data(depreciation_date, depr_acc_id,
                                           'depreciation', move.id))

            move_line_obj.create(line._setup_move_line_data(
                depreciation_date, exp_acc_id, 'expense', move.id))

            line.with_context(allow_asset_line_update=True).write(
                {'move_id': move.id})

            asset_ids.append(asset.id)
        # we re-evaluate the assets to determine whether we can close them
        for asset in asset_obj.browse(asset_ids):
            if asset.company_id.currency_id.is_zero(asset.value_residual):
                asset.write({'state': 'close'})
        return move.id
