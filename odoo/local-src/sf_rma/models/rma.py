# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import json
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def get_selection_description(rec, field):
    """ Get translated selection description from its selected value """
    return dict(rec._fields[field]._description_selection(rec.env))[rec[field]]


class RMA(models.Model):
    _name = 'sf.rma'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Return merchandise authorisation"

    name = fields.Char(required=True, default='/', readonly=True)

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
    original_order_products_domain = fields.Char(
        'product.product', compute="_compute_original_order_products_domain")
    original_order_id = fields.Many2one(
        'sale.order',
        string='Original sale order'
    )
    original_customer_id = fields.Many2one(
        'res.partner',
        string='Original customer',
        help='Customer who bought the product'
    )
    lot_id = fields.Many2one(
        'stock.production.lot',
        string="Lot/Serial Number",
        domain="[('first_outgoing_stock_move_id','!=',False)]",
        help="The Lot/Serial of the returned product")
    lot_first_order_id = fields.Many2one(
        'sale.order',
        related='lot_id.first_outgoing_stock_move_id.picking_id.sale_id'
    )
    warranty_limit = fields.Date("Warranty limit")

    company_id = fields.Many2one(
        'res.company', string="Company",
        default=lambda rec: rec.env.user.company_id.id)

    zendesk_ref = fields.Char("Ticket num (Zendesk)", required=True)
    zendesk_url = fields.Char(compute='_compute_zendesk_url')
    zendesk_url_set = fields.Boolean(compute='_compute_zendesk_url')

    user_id = fields.Many2one(
        'res.users',
        string="Responsible",
        default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', "Draft"),
        ('open', "Open"),
        ('closed', "Closed"),
        ('canceled', "Canceled")],
        string="Status",
        required=True,
        default='draft')

    # Decisions
    to_exchange = fields.Boolean(
        default=False)
    to_receive = fields.Boolean(
        default=False)
    decision = fields.Selection(
        [('free', 'Free'),
         ('to_invoice', 'To invoice'),
         ('to_offer', 'Commercial Gesture')]
    )
    offer_reason = fields.Char(string="Reason",
                               help="Reason of the commercial gesture")
    repair_by = fields.Selection([
        ('retailer', "Retailer"),
        ('sf', "senseFly")])

    # Notes
    problem_description = fields.Text()
    resolution_description = fields.Text()

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

    repair_ids = fields.One2many('mrp.repair', 'rma_id', string="Repairs")
    sale_ids = fields.One2many('sale.order', 'rma_id', string="Sale orders")
    picking_ids = fields.One2many('stock.picking', 'rma_id', string="Pickings")
    history_rma_ids = fields.Many2many(
        'sf.rma',
        string='RMA History',
        compute='_compute_history_rma',
        help="Other RMA for the same serial number")

    repair_count = fields.Integer(
        compute='_compute_repair_count', string="# Repairs")
    sale_count = fields.Integer(
        compute='_compute_sale_count', string="# Sale orders")
    picking_count = fields.Integer(
        compute='_compute_picking_count', string="# Pickings")
    history_rma_count = fields.Integer(
        compute='_compute_history_rma', string="# RMA")

    repair_state = fields.Char(compute="_compute_repair_count")
    sale_state = fields.Char(compute="_compute_sale_count")
    picking_state = fields.Char(compute="_compute_picking_count")

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
        if self.repair_count == 1:
            state = get_selection_description(self.repair_ids, 'state')
            self.repair_state = state

    @api.one
    @api.depends('sale_ids')
    def _compute_sale_count(self):
        self.sale_count = len(self.sale_ids)
        if self.sale_count == 1:
            state = get_selection_description(self.sale_ids, 'state')
            self.sale_state = state

    @api.one
    @api.depends('picking_ids')
    def _compute_picking_count(self):
        self.picking_count = len(self.picking_ids)
        if self.picking_count == 1:
            state = get_selection_description(self.picking_ids, 'state')
            self.picking_state = state

    @api.model
    def _get_sequence_number(self):
        return self.env['ir.sequence'].next_by_code('sf.rma') or '/'

    @api.model
    def create(self, values):
        values = values or {}
        if ('name' not in values or not values.get('name') or
                values.get('name') == '/'):
            values['name'] = self._get_sequence_number()
        return super(RMA, self).create(values)

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
        action = self.action_view_relation(
            'repair_ids',
            'mrp_repair.action_repair_order_tree',
            'mrp_repair.view_repair_order_form')
        values = self._prepare_mrp_repair_data()
        values = {'default_' + k: v for k, v in values.iteritems()}
        action['context'] = values
        return action

    @api.multi
    def action_view_sale(self):
        action = self.action_view_relation(
            'sale_ids',
            'sf_rma.act_sf_rma_sale_order',
            'sale.view_order_form')
        values = self._prepare_so_data()
        values = {'default_' + k: v for k, v in values.iteritems()}
        action['context'] = values
        return action

    @api.multi
    def action_view_picking(self):
        action = self.action_view_relation(
            'picking_ids',
            'stock.action_picking_tree_all',
            'stock.view_picking_form')
        values = self._prepare_picking_data()
        values = {'default_' + k: v for k, v in values.iteritems()}
        action['context'] = values
        return action

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
            'pricelist_id': self.env.ref('sf_rma.pricelist_rma').id,
            'origin': self.name,
            'type_id': self.env.ref('sf_rma.rma_sale_type').id
        }

    def _prepare_so_line_data(self, sale):
        self.ensure_one()
        values = {
            'order_id': sale.id,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
            'company_id': self.company_id.id,
        }
        if self.lot_id:
            values.update({'lot_id': self.lot_id.id})
        return values

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
            # New create context without default_user_id key to ensure
            # mrp.repair is not created with RMA user.
            create_mrp_repair_context = dict(self.env.context or {})
            create_mrp_repair_context['default_user_id'] = False

            mrp_repair_data = self._prepare_mrp_repair_data()
            self.env['mrp.repair'].with_context(
                create_mrp_repair_context).create_with_onchanges(
                mrp_repair_data, ['product_id', 'partner_id', 'location_id'])

            so_data = self._prepare_so_data()
            sale = self.env['sale.order'].create_with_onchanges(
                so_data, ['partner_id'])

            so_line_data = self._prepare_so_line_data(sale)
            self.env['sale.order.line'].create_with_onchanges(
                so_line_data, ['product_id'])

            if rec.to_receive:
                picking_data = self._prepare_picking_data()
                picking = self.env['stock.picking'].create_with_onchanges(
                    picking_data, ['partner_id'])

                move_data = self._prepare_reception_move_data(picking)
                self.env['stock.move'].create_with_onchanges(
                    move_data, ['product_id'])

                picking.action_confirm()

    @api.multi
    def action_close(self):
        self.write({'state': 'closed',
                    'date_closed': fields.Datetime.now()})

    @api.multi
    def action_reset(self):
        self.write({'state': 'draft',
                    'date_closed': False})

    @api.multi
    @api.depends('original_order_id')
    def _compute_original_order_products_domain(self):
        for rma in self:
            products = self._get_order_products(rma.original_order_id)
            if products:
                rma.original_order_products_domain = json.dumps(
                    [('id', 'in', products.ids)])

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        lot = self.lot_id
        if lot:
            sale_order = self.lot_first_order_id
            self.product_id = self.lot_id.product_id.id
            self.warranty_limit = self.lot_id.warranty_end_date
            self.original_order_id = sale_order.id
        else:
            self.product_id = False
            self.warranty_limit = False
            self.original_order_id = False

    @api.onchange('original_order_id')
    def onchange_original_order_id(self):
        order = self.original_order_id
        if order:
            lot = self.lot_id
            if lot:
                original_order = self.lot_first_order_id
                if order != original_order:
                    raise ValidationError(_('Original sale order has to be '
                                            'the first sale order where the '
                                            'lot was sold : %s')
                                          % original_order.name
                                          )
            original_partner_id = order.partner_id.id
            self.original_customer_id = original_partner_id
            self.partner_id = original_partner_id
        else:
            self.original_customer_id = False
            self.partner_id = False
            if not self.lot_id:
                self.product_id = False
                self.warranty_limit = False

    @api.onchange('original_customer_id')
    def onchange_original_customer_id(self):
        lot = self.lot_id
        if lot:
            sale_order = self.lot_first_order_id
        else:
            sale_order = self.original_order_id
        if sale_order.partner_id != self.original_customer_id:
            raise ValidationError(_('Original customer has to be the partner '
                                    'from the original sale order : %s.')
                                  % sale_order.partner_id.name)

    @api.onchange('product_id')
    def onchange_product_id(self):
        lot = self.lot_id
        if lot and lot.product_id != self.product_id:
            raise ValidationError(_('RMA Product has to be the same product '
                                    'from the lot/serial number : %s.')
                                  % lot.product_id)
        else:
            original_products = self._get_order_products(
                self.original_order_id)
            if original_products and self.product_id not in original_products:
                raise ValidationError(_('RMA Product has to be a product '
                                        'from original sale order.'))

    def _get_order_products(self, sale_order):
        order_lines = self.env['sale.order.line'].search(
            [('order_id', '=', sale_order.id)])
        if order_lines:
            return order_lines.mapped('product_id')

    _sql_constraints = [
        ('zendesk_ref_5_digits',
         "CHECK(CHAR_LENGTH(zendesk_ref) = 5 AND zendesk_ref ~ '^[0-9]+$')",
         'Ticket num (Zendesk) must be 5 digits'),
        ('zendesk_ref_unique', 'unique(zendesk_ref)',
         'This ticket num (Zendesk) is already used on another RMA.')
    ]
