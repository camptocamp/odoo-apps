# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        """ override default 'date' value if 'date' is in vals """
        move = super(AccountMove, self).create(vals)
        if vals.get('date'):
            move.date = vals.get('date')
        return move

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
        for line in self:
            date = line.date or fields.Datetime.now()
            if line.currency_id and company_currency and line.amount_currency:
                if line.amount_currency > 0:
                    line.credit = False
                    line.debit = line.currency_id.with_context(date=date).\
                        compute(line.amount_currency, company_currency)
                elif line.amount_currency < 0:
                    line.credit = -line.currency_id.with_context(date=date).\
                        compute(line.amount_currency, company_currency)
                    line.debit = False


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def _fix_multiple_exchange_rates_diff(
            self, amls_to_fix, amount_diff, diff_in_currency, currency, move):
        move_lines = self.env['account.move.line']
        partial_reconciles = self.env['account.partial.reconcile']

        for aml_to_fix in amls_to_fix:
            move_line, partial_reconcile = super(AccountPartialReconcile,
                                                 self).\
                _fix_multiple_exchange_rates_diff(aml_to_fix,
                                                  amount_diff,
                                                  diff_in_currency,
                                                  currency,
                                                  move)

            if aml_to_fix.invoice_id.number:
                move_line.name = _('Currency exchange rate difference: %s')\
                                  % aml_to_fix.invoice_id.number
                move_lines |= move_line
                partial_reconciles |= partial_reconcile

        return move_lines, partial_reconciles
