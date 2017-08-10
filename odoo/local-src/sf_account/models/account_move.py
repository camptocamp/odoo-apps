# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


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
