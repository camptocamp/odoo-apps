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
    sale_incoterm_id = fields.Many2one(
        'stock.incoterms',
        string='Sale Incoterm',
        related='sale_id.incoterm'
    )
    confirm_customer_received = fields.Boolean(
        string='Confirm Customer Received',
        related='sale_incoterm_id.confirm_customer_received',

    )
    customer_received = fields.Boolean(
        string='Customer Received',
        help="Confirm that the customer received physically the goods."
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default['date_shipped'] = False
        return super(StockPicking, self).copy(default)

    def action_shipped(self):
        self.write({'date_shipped': datetime.today()})

    @api.multi
    def do_new_transfer(self):
        # If there's no need of confirmation that the customer received
        # the goods, the reception if confirmed by default
        for pick in self:
            pick.customer_received = not pick.confirm_customer_received
        return super(StockPicking, self).do_new_transfer()

    @api.one
    def _get_sale_order_id(self):
        if self.origin and self.picking_type_id.code == 'outgoing':
            self.sale_id = self.env['sale.order'].search(
                [('name', '=', self.origin)])

    @api.multi
    def do_prepare_partial(self):
        """ This function ensures that any Lot/Serial number for pack ops
            is automatically added to the next picking """
        res = super(StockPicking, self).do_prepare_partial()
        pack_lots = self.pack_operation_ids.mapped('pack_lot_ids').filtered(
            lambda p: p.plus_visible
        )
        if pack_lots:
            pack_lots.do_plus()
        return res


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    show_button_shipped = fields.Boolean('Show button shipped')
