# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseConfigSettings(models.TransientModel):

    _inherit = 'purchase.config.settings'

    terms_and_conditions = fields.Html(
        related='company_id.purchase_terms_and_conditions')
