# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_new_transfer(self):
        for pick in self:
            # RMA reception? Open the repair
            if pick.rma_id and pick.picking_type_id.code == 'incoming':
                for repair in pick.rma_id.repair_ids:
                    repair.state = 'open'
        return super(StockPicking, self).do_new_transfer()
