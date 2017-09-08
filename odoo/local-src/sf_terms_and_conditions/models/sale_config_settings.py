# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleConfigSettings(models.TransientModel):

    _inherit = 'sale.config.settings'

    terms_and_conditions = fields.Html(
        related='company_id.sale_terms_and_conditions')
