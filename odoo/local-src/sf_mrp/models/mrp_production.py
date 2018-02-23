# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def open_produce_product(self):
        """ override base mrp.production open_produce_product method """
        self.ensure_one()

        for move in self.move_raw_ids:
            if move.has_tracking in ['lot', 'serial'] and \
                    move.product_uom_qty != move.quantity_done:
                raise ValidationError('Not all lot material consumed!')

        action = self.env.ref('mrp.act_mrp_product_produce').read()[0]
        return action
