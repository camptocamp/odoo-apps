# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.onchange('payment_difference')
    def onchange_payment_difference(self):
        if self.payment_difference != 0:
            self.amount = 0
