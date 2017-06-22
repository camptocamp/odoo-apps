# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class RMA(models.Model):
    _name = 'sf.rma'
    _description = "Return merchandise authorisation"

    name = fields.Char(required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True,
        help="Partner concerned by the repair")
    product_id = fields.Many2one(
        'product.product',
        string="Product",
        required=True,
        help="Returned product")
    lot_id = fields.Many2one(
        'stock.production.lot',
        string="Lot/Serial Number",
        domain="[('product_id','=',product_id)]",
        help="The Lot/Serial of the returned product")
    warranty_limit = fields.Date("Warranty limit")

    zendesk_ref = fields.Char("Ticket num (Zendesk)")
    zendesk_url = fields.Char(compute='_compute_zendesk_url')

    user_id = fields.Many2one(
        'res.users',
        string="Responsible",
        default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', "Draft"),
        ('open', "Open"),
        ('closed', "Closed")],
        string="Status",
        required=True,
        default='draft')

    # Decisions
    exchanged = fields.Boolean(
        default=False)
    received = fields.Boolean(
        default=False)
    offered = fields.Boolean(
        default=False,
        help="Commercial gesture")
    offer_reason = fields.Char(help="Reason of the commercial gesture")
    repaired_by = fields.Selection([
        ('retailer', "Retailer"),
        ('sf', "senseFly")])

    notes = fields.Text()

    # Drone info
    drone_flight_time = fields.Float(
        "Hours of flight",
        help="Drone hours of flight")
    drone_flight_num = fields.Integer(
        "Number of flights",
        help="Drone number of flights")
    drone_firmware_version = fields.Char(
        "Firmware number",
        help="Drone firmware number")

    cause_ids = fields.Many2many(
        'sf.rma.cause',
        string="Causes",
        help="Cause(s) of the failure")
    invoicing_method = fields.Selection([
        ('before', "Before invoicing"),
        ('after', "After invoicing")])

    # TODO
    # smart buttons
    # repair_ids = fields
    # order_ids = fields.
    # picking_ids = fields.

    @api.one
    @api.depends('zendesk_ref')
    def _compute_zendesk_url(self):
        if self.zendesk_ref:
            self.zendesk_url = "url%s" % self.zendesk_ref
