# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    bfc_account = fields.Char(
        string='BFC Account',
        help='Parrot business financial consolidation account.')
    bfc_factor = fields.Selection(
        [(-1, '-1'), (1, '1')],
        string='BFC Factor', help="Informs how the value has to be reported.")
