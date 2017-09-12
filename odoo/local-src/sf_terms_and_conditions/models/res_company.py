# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):

    _inherit = 'res.company'

    purchase_terms_and_conditions = fields.Html(string='Terms and conditions',
                                                translate=True)

    sale_terms_and_conditions = fields.Html(string='Terms and conditions',
                                            translate=True)