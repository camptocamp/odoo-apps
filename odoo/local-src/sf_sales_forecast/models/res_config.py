# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    @api.multi
    def default_sale_forecast_range_type_id(self):
        return self.search(
            [], limit=1, order='id desc').sale_forecast_range_type_id

    sale_forecast_range_type_id = fields.Many2one(
        'date.range.type', string='Sale forecast range type',
        default=default_sale_forecast_range_type_id)
