# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    analytic_tag_ids = fields.Many2many('account.analytic.tag',
                                        string='Analytic Tags')

    @api.multi
    def _compute_entries(self, date_end, check_triggers=False):
        # Overriding this method to aggregate depreciation journal items in
        # a single journal entry

        result = []
        depreciation_obj = self.env['account.asset.line']
        if check_triggers:
            recompute_obj = self.env['account.asset.recompute.trigger']
            recomputes = recompute_obj.sudo().search(
                [('state', '=', 'open')])
        if check_triggers and recomputes:
            trigger_companies = recomputes.mapped('company_id')
            for asset in self:
                if asset.company_id.id in trigger_companies.ids:
                    asset.compute_depreciation_board()
        depreciations = depreciation_obj.search([
            ('asset_id', 'in', self.ids),
            ('type', '=', 'depreciate'),
            ('init_entry', '=', False),
            ('line_date', '<=', date_end),
            ('move_check', '=', False)], order='line_date')

        if self.env.context.get('aggregate_move_lines'):
            # 1 move for all depreciations
            result = depreciations.create_move()
        else:
            # 1 move per depreciation
            for depreciation in depreciations:
                result += depreciation.with_context(
                    depreciation_date=depreciation.line_date).create_move()

        if check_triggers and recomputes:
            companies = recomputes.mapped('company_id')
            triggers = recomputes.filtered(
                lambda r: r.company_id.id in companies.ids)
            if triggers:
                recompute_vals = {
                    'date_completed': fields.Datetime.now(),
                    'state': 'done',
                }
                triggers.sudo().write(recompute_vals)
        return result
