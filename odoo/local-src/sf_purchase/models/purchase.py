# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class Purchase(models.Model):
    _inherit = "purchase.order"

    second_vendor_id = fields.Many2one(
        'res.partner',
        string='Secondary Vendor',
        help='An indirect supplier.')
