# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _default_uom(self):
        weight_uom_id = self.env.ref('product.product_uom_kgm',
                                     raise_if_not_found=False)
        if not weight_uom_id:
            uom_categ_id = self.env.ref('product.product_uom_categ_kgm').id
            weight_uom_id = self.env['product.uom'].search(
                [('category_id', '=', uom_categ_id), ('factor', '=', 1)],
                limit=1)
        return weight_uom_id

    volume = fields.Float(copy=False)
    weight = fields.Float(compute='_cal_weight',
                          digits=dp.get_precision('Stock Weight'), store=True)
    weight_uom_id = fields.Many2one('product.uom', string='Unit of Measure',
                                    required=True, readonly="1",
                                    help="Unit of measurement for Weight",
                                    default=_default_uom)

    @api.depends('order_line')
    def _cal_weight(self):
        for sale in self:
            sale.weight = sum(line.weight for line in sale.order_line if
                              line.state != 'cancel')
