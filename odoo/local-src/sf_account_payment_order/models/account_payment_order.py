# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'

    @api.multi
    @api.constrains('date_scheduled')
    def check_date_scheduled(self):
        """ override check_date_scheduled to add check on
            date_prefered != 'fixed' """
        today = fields.Date.context_today(self)
        for order in self:
            if order.date_scheduled and order.date_prefered != 'fixed':
                if order.date_scheduled < today:
                    raise ValidationError(_(
                        "On payment order %s, the Payment Execution Date "
                        "is in the past (%s).")
                        % (order.name, order.date_scheduled))

    @api.multi
    def _prepare_move(self, bank_lines=None):
        """ set date explicitly """
        vals = super(AccountPaymentOrder, self)._prepare_move(bank_lines=None)
        if self.date_prefered == 'fixed':
            vals['date'] = self.date_scheduled
        return vals
