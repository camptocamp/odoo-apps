# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.onchange('payment_method_id', 'journal_id')
    def _onchange_payment_method(self):
        super(AccountPayment, self)._onchange_payment_method()

        journal_currency = \
            self.journal_id.currency_id \
            or self.journal_id.company_id.currency_id

        for invoice in self.invoice_ids:
            if journal_currency != invoice.currency_id:
                self.amount = 0
                break
