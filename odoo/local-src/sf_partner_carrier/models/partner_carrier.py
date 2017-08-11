# -*- coding: utf-8 -*-
# Part of SenseFly.
from odoo import fields, models


class PartnerCarrierAccount(models.Model):
    _name = 'partner.carrier.account'
    _description = "Partner carrier account"

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True)
    account = fields.Char(required=True)
    carrier_id = fields.Many2one(
        'delivery.carrier',
        string='Carrier',
        required=True)


class Partner(models.Model):
    _inherit = 'res.partner'

    carrier_account_ids = fields.One2many(
        'partner.carrier.account',
        'partner_id',
        string='Carrier Accounts',
        help='This partner is the owner of the following accounts.'
    )
