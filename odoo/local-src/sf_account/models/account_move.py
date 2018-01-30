# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('date')
    def _onchange_date(self):
        """On the form view, a change on the date will trigger onchange()
        on account.move but not on account.move.line even the date field
        is related to account.move.
        Then, trigger the _onchange_amount_currency manually.
        """
        self.line_ids.onchange_amount_currency()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange('amount_currency', 'currency_id')
    def onchange_amount_currency(self):
        company_currency = self.env.user.company_id.currency_id
        date = self.date or fields.Datetime.now()
        if self.currency_id and company_currency and self.amount_currency:
            if self.amount_currency > 0:
                self.credit = False
                self.debit = self.currency_id.with_context(date=date).\
                    compute(self.amount_currency, company_currency)
            elif self.amount_currency < 0:
                self.credit = -self.currency_id.with_context(date=date).\
                    compute(self.amount_currency, company_currency)
                self.debit = False


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def _fix_multiple_exchange_rates_diff(
            self, amls_to_fix, amount_diff, diff_in_currency, currency, move):
        move_lines, partial_reconciles = super(AccountPartialReconcile, self).\
            _fix_multiple_exchange_rates_diff(
            amls_to_fix, amount_diff, diff_in_currency, currency, move)

        for aml in amls_to_fix:
            if aml.invoice_id.number:
                move_lines.name = _('Currency exchange rate difference: %s')\
                                  % aml.invoice_id.number
        return move_lines, partial_reconciles
