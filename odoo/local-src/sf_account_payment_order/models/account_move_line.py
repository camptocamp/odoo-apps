# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        self.ensure_one()
        # Payment reference (name) is the PO partner ref
        vals = super(AccountMoveLine, self)._prepare_payment_line_vals(
            payment_order)

        if self.invoice_id.partner_ref:
            vals['name'] = self.invoice_id.partner_ref
        return vals
