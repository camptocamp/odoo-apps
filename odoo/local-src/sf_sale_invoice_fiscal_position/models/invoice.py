# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def compute_taxes(self):
        res = super(AccountInvoice, self).compute_taxes()
        for invoice in self:
            if invoice.fiscal_position_id:
                invoice.fiscal_position_change()
        return res
