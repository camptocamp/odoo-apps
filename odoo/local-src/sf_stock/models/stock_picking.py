# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api
from datetime import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_shipped = fields.Date('Date Shipped')
    show_button_shipped = fields.Boolean(
        related='picking_type_id.show_button_shipped', readonly=True
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default['date_shipped'] = False
        return super(StockPicking, self).copy(default)

    def action_shipped(self):
        self.write({'date_shipped': datetime.today()})


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    show_button_shipped = fields.Boolean('Show button shipped')
