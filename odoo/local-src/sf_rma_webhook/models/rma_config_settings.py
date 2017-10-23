# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RMASettings(models.TransientModel):

    _inherit = 'rma.config.settings'

    web_hook_base_url = fields.Char(
        string='Base Url', required=True,
        related='company_id.web_hook_base_url',
        help="Base url to be called when rma is confirmed or repaired.",
    )
