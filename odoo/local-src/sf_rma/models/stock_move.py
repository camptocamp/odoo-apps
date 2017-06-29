# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def play_onchanges(self, values, onchange_fields):
        res = super(StockMove, self).play_onchanges(values, onchange_fields)
        if 'product_qty' in res:
            del res['product_qty']
        return res
