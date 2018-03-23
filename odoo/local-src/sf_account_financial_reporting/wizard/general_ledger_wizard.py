# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GeneralLedgerReportWizard(models.TransientModel):
    """General ledger report wizard."""
    _inherit = 'general.ledger.report.wizard'

    all_account_types = fields.Boolean(string='All')
    account_type_ids = fields.Many2many(
        comodel_name='account.account.type',
        string='Account Types')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries')],
                                   string='Target Moves',
                                   required=True,
                                   default='posted')

    @api.onchange('account_type_ids', 'all_account_types')
    def onchange_account_types(self):
        """Handle account types filter"""
        all_account_types = self.env['account.account.type'].search([])

        if self.all_account_types:
            self.account_type_ids = all_account_types

        if self.account_type_ids:
            domain = [('user_type_id', 'in', self.account_type_ids.ids)]
            self.account_ids = self.env['account.account'].search(domain)
        else:
            self.account_ids = None

    @api.onchange('partner_ids')
    def onchange_partner_ids(self):
        """Override this method. We do not want to change the filter"""
        pass
