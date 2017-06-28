# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class MRPRepair(models.Model):
    _inherit = 'mrp.repair'

    rma_id = fields.Many2one('sf.rma', string="RMA")
