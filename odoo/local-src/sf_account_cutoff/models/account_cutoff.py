# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountCutoff(models.Model):
    _inherit = 'account.cutoff'

    @api.multi
    def _prepare_provision_line(self, cutoff_line):
        line = super(AccountCutoff, self)._prepare_provision_line(cutoff_line)
        line['partner_id'] = cutoff_line.partner_id.id
        line['analytic_tag_ids'] = tuple([
            (6, 0, tuple(cutoff_line.analytic_tag_ids.ids))
        ])
        return line

    @api.multi
    def _prepare_prepaid_lines(self, aml, mapping):
        lines = super(AccountCutoff, self)._prepare_prepaid_lines(
            aml, mapping
        )
        lines['analytic_tag_ids'] = [(6, 0, aml.analytic_tag_ids.ids)]
        return lines

    def _get_merge_keys(self):
        key_list = super(AccountCutoff, self)._get_merge_keys()
        key_list.append('partner_id')
        key_list.append('analytic_tag_ids')
        return key_list


class AccountCutoffLine(models.Model):
    _inherit = 'account.cutoff.line'

    analytic_tag_ids = fields.Many2many('account.analytic.tag',
                                        string='Analytic Tags')
