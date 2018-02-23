# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        self.ensure_one()
        vals = super(AccountMoveLine, self)._prepare_payment_line_vals(
            payment_order)

        # Payment reference for supplier
        invoice = self.invoice_id
        if invoice.partner_ref and invoice.reference_type != 'bvr':
            vals['communication'] = invoice.partner_ref
        return vals
