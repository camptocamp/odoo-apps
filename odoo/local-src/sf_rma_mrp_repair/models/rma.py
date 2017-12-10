# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class RMA(models.Model):
    _inherit = 'sf.rma'

    @api.multi
    def action_open(self):
        # Automatically open the repair when there is nothing to receive
        super(RMA, self).action_open()
        for rec in self:
            if not rec.to_receive:
                rec.repair_ids.action_repair_open()
