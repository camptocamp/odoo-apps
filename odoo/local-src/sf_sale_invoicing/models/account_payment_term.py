# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPaymentTerm(models.Model):

    _inherit = "account.payment.term"

    down_payment_required = fields.Boolean(string='Requires down payment',
                                           default=False)
