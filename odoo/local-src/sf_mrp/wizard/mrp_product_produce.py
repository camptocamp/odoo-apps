# -*- coding: utf-8 -*-

from odoo import api, models


class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    @api.multi
    def do_produce(self):
        res = super(MrpProductProduce, self).do_produce()
        # Stock moves of consumed products to Done
        for prod_produce in self:
            moves_not_to_do = prod_produce.production_id.move_raw_ids.\
                filtered(lambda x: x.state == 'done')
            moves_to_do = prod_produce.production_id.move_raw_ids.filtered(
                lambda x: x.state not in ('done', 'cancel'))
            moves_to_do.action_done()
            moves_to_do = prod_produce.production_id.move_raw_ids.filtered(
                lambda x: x.state == 'done') - moves_not_to_do
            prod_produce.production_id._cal_price(moves_to_do)
        return res
