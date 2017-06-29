# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class RMA(models.Model):
    _name = 'sf.rma'
    _description = "Return merchandise authorisation"

    name = fields.Char(required=True)

    date = fields.Datetime(
        'Claim Date', index=True, default=fields.Datetime.now)
    create_date = fields.Datetime("Creation Date", readonly=True)
    date_closed = fields.Datetime("Closed", readonly=True)

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

    company_id = fields.Many2one(
        'res.company', string="Company",
        default=lambda rec: rec.env.user.company_id.id)

    zendesk_ref = fields.Char("Ticket num (Zendesk)")
    zendesk_url = fields.Char(compute='_compute_zendesk_url')
    zendesk_url_set = fields.Boolean(compute='_compute_zendesk_url')

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

    repair_ids = fields.One2many('mrp.repair', 'rma_id', string="Repairs")
    sale_ids = fields.One2many('sale.order', 'rma_id', string="Sale orders")
    picking_ids = fields.One2many('stock.picking', 'rma_id', string="Pickings")
    history_rma_ids = fields.Many2many(
        'sf.rma',
        compute='_compute_history_rma',
        help="Other RMA for the same seral number")

    repair_count = fields.Integer(
        compute='_compute_repair_count', string="# Repairs")
    sale_count = fields.Integer(
        compute='_compute_sale_count', string="# Sale orders")
    picking_count = fields.Integer(
        compute='_compute_picking_count', string="# Pickings")
    history_rma_count = fields.Integer(
        compute='_compute_history_rma', string="# RMA")

    @api.one
    @api.depends('zendesk_ref')
    def _compute_zendesk_url(self):
        """ Compute URL from a base url and a ticket number """
        ICP = self.env['ir.config_parameter']
        base_url = ICP.get_param('zendesk.url')
        if base_url:
            self.zendesk_url_set = True
            if self.zendesk_ref:
                if '{ref}' not in base_url:
                    base_url += '{ref}'
                self.zendesk_url = base_url.format(ref=self.zendesk_ref)

    @api.one
    @api.depends('lot_id')
    def _compute_history_rma(self):
        """ Find all RMA for the same lot_id """
        if self.lot_id:
            domain = [('lot_id', '=', self.lot_id.id)]
            if not isinstance(self.id, models.NewId):
                # exclude current RMA from history
                domain.append(('id', '!=', self.id))
            self.history_rma_ids = self.search(domain).ids
            self.history_rma_count = len(self.history_rma_ids)

    @api.one
    @api.depends('repair_ids')
    def _compute_repair_count(self):
        self.repair_count = len(self.repair_ids)

    @api.one
    @api.depends('sale_ids')
    def _compute_sale_count(self):
        self.sale_count = len(self.sale_ids)

    @api.one
    @api.depends('picking_ids')
    def _compute_picking_count(self):
        self.picking_count = len(self.picking_ids)

    @api.multi
    def action_view_relation(self, field, action, form_view):
        action = self.env.ref(action).read()[0]
        if len(self[field]) > 1:
            action['domain'] = [('id', 'in', self[field].ids)]
        elif len(self[field]) == 1:
            action['views'] = [(self.env.ref(form_view).id, 'form')]
            action['res_id'] = self[field].ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_view_repair(self):
        return self.action_view_relation(
            'repair_ids',
            'mrp_repair.action_repair_order_tree',
            'mrp_repair.view_repair_order_form')

    @api.multi
    def action_view_sale(self):
        return self.action_view_relation(
            'sale_ids',
            'sf_rma.act_sf_rma_sale_order',
            'sale.view_order_form')

    @api.multi
    def action_view_picking(self):
        return self.action_view_relation(
            'picking_ids',
            'stock.action_picking_tree_all',
            'stock.view_picking_form')

    @api.multi
    def action_view_rma_history(self):
        return self.action_view_relation(
            'history_rma_ids',
            'sf_rma.sf_rma_action',
            'sf_rma.sf_rma_form_view')

    def _prepare_mrp_repair_data(self):
        self.ensure_one()
        mrp_repair_data = self.env['mrp.repair'].default_get(
            ['location_id'])
        mrp_repair_data.update({
            'rma_id': self.id,
            'partner_id': self.partner_id.id,
            'product_id': self.product_id.id,
            'lot_id': self.lot_id.id,
            'product_qty': 1,
            'company_id': self.company_id.id,
        })
        return mrp_repair_data

    def _prepare_so_data(self):
        self.ensure_one()
        return {
            'partner_id': self.partner_id.id,
            'rma_id': self.id,
            'company_id': self.company_id.id,
            'team_id': self.env.ref('sf_rma.crm_team_rma').id,
            'pricelist_id': self.env.ref('sf_rma.pricelist_rma').id
        }

    def _prepare_so_line_data(self, sale):
        self.ensure_one()
        return {
            'order_id': sale.id,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
            'company_id': self.company_id.id,
        }

    def _prepare_picking_data(self):
        self.ensure_one()
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', self.company_id.id)],
            limit=1
        )

        return {
            'partner_id': self.partner_id.id,
            'rma_id': self.id,
            'company_id': self.company_id.id,
            'picking_type_id': warehouse.in_type_id.id,
            'location_dest_id': warehouse.lot_rma_id.id,
        }

    def _prepare_reception_move_data(self, picking):
        self.ensure_one()

        return {
            'picking_id': picking.id,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
            'company_id': self.company_id.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
        }

    @api.multi
    def action_open(self):
        self.write({'state': 'open'})
        for rec in self:
            mrp_repair_data = self._prepare_mrp_repair_data()
            self.env['mrp.repair'].create_with_onchanges(
                mrp_repair_data, ['product_id', 'partner_id', 'location_id'])

            so_data = self._prepare_so_data()
            sale = self.env['sale.order'].create_with_onchanges(
                so_data, ['partner_id'])

            so_line_data = self._prepare_so_line_data(sale)
            self.env['sale.order.line'].create_with_onchanges(
                so_line_data, ['product_id'])

            picking_data = self._prepare_picking_data()
            picking = self.env['stock.picking'].create_with_onchanges(
                picking_data, ['partner_id'])

            move_data = self._prepare_reception_move_data(picking)
            picking = self.env['stock.move'].create_with_onchanges(
                move_data, ['product_id'])

    @api.multi
    def action_close(self):
        self.write({'state': 'closed'})

    @api.multi
    def action_reset(self):
        self.write({'state': 'draft'})
