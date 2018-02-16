# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RMASettings(models.TransientModel):

    _name = 'rma.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    rma_sale_line_route_id = fields.Many2one(
        'stock.location.route', string='Sale Line route',
        required=True,
        related='company_id.rma_sale_line_route_id',
        help="This route will be used in the sale order line.")

    rma_so_default_carrier_id = fields.Many2one(
        'delivery.carrier',
        string='Free Repair Default Carrier',
        related='company_id.rma_so_default_carrier_id',
        help="This delivery method is applied by default when the decision "
             "of a RMA is Offer or Commercial Gesture")

    rma_default_payment_term_from_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default payment term from',
        related='company_id.rma_default_payment_term_from_id',
        help="When the sale order is generated, "
             "the payment term we need to replace",
    )

    rma_default_payment_term_to_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Default payment term to',
        related='company_id.rma_default_payment_term_to_id',
        help="When the sale order is generated, "
             "the payment term we need to define",
    )

    rma_receive_picking_type_id = fields.Many2one(
        related='company_id.rma_receive_picking_type_id'
    )
