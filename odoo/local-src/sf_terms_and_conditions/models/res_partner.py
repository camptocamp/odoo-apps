# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    apply_sale_terms_and_conditions = fields.Boolean(
        string='Apply terms and conditions', default=True,
        help='Check this box to print terms and conditions on sale orders '
             'from this partner'
    )

    apply_purchase_terms_and_conditions = fields.Boolean(
        string='Apply terms and conditions', default=True,
        help='Check this box to print terms and conditions on purchase orders '
             'from this partner'
    )
