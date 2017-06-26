# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    active = fields.Boolean(string='Active', default=True)
