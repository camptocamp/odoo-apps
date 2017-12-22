# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api
from datetime import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_shipped = fields.Date('Date Shipped')
    date_delivered = fields.Date('Date Delivered')
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

    procurement_group_sale_id = fields.Many2one(
        'sale.order',
        string='Procurement group sale',
        compute='compute_procurement_group_sale'
    )

    @api.one
    def compute_procurement_group_sale(self):
        for order in self.env['sale.order'].search(
                [('name', '=', self.group_id.name)], limit=1):
            self.procurement_group_sale_id = order

    @api.one
    @api.depends('move_lines.procurement_id.sale_line_id.order_id')
    def _compute_sale_id(self):
        for move in self.move_lines:
            if move.procurement_id.sale_line_id:
                self.sale_id = move.procurement_id.sale_line_id.order_id
                return

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default['date_shipped'] = False
        return super(StockPicking, self).copy(default)

    def action_shipped(self):
        self.write({'date_shipped': datetime.today()})

    @api.one
    def propagate_delivery_info(self):
        """Propagate delivery info to the next delivery stage"""
        if self.picking_type_id.propagate_delivery_info:
            next_picking = self.move_lines.move_dest_id.picking_id
            next_picking.carrier_id = self.carrier_id
            next_picking.carrier_tracking_ref = self.carrier_tracking_ref

    @api.multi
    def do_new_transfer(self):
        # 1. If there's no need of confirmation that the customer received
        #    the goods, the reception is confirmed by default
        # 2. Propagate delivery details to next stage
        for pick in self:
            pick.customer_received = not pick.confirm_customer_received
            pick.propagate_delivery_info()
            pick.date_delivered = fields.Date.today()
        return super(StockPicking, self).do_new_transfer()

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
    propagate_delivery_info = fields.Boolean('Propagate delivery info',
                                             help="When you validate the DO, "
                                                  "delivery information is "
                                                  "propagated to the "
                                                  "next stage."
                                             )
