# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    linked_partner_id = fields.Many2one(
        'res.partner',
        string='Linked partner',
        help='The bank account of this partner can also be used to pay a PO.'
    )
    linked_partner_bank_ids = fields.One2many(
        related='linked_partner_id.bank_ids',
        string='Banks')
