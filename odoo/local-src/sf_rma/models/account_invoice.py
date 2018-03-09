# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def write(self, vals):
        result = super(AccountInvoice, self).write(vals)
        if vals.get('state') == 'paid':
            self.mapped('order_ids')._compute_down_payment_missing()
        return result
