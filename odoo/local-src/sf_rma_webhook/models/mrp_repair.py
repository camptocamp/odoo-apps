# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class MRPRepair(models.Model):
    _inherit = "mrp.repair"

    @api.multi
    def action_repair_done(self):
        rma_ids = super(MRPRepair, self).action_repair_done()
        self.env['rma.callback'].call('odoo_rma_repaired', rma_ids)
        return rma_ids
