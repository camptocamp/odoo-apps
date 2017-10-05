# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class Incoterms(models.Model):
    _inherit = "stock.incoterms"

    confirm_customer_received = fields.Boolean(
        string="Confirm Customer Received",
        help="Shows customer reception confirmation "
             "checkbox on delivery order."
    )
