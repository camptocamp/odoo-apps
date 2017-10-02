# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class RMASettings(models.TransientModel):

    _inherit = 'rma.config.settings'

    @api.multi
    def default_web_hook_base_url(self):
        return self.search([], limit=1, order='id desc').web_hook_base_url

    web_hook_base_url = fields.Char(
        string='Base Url', required=True,
        help="Base url to be called when rma is confirmed or repaired.",
        default=default_web_hook_base_url
    )
