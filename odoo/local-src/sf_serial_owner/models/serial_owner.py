# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SerialOwner(models.Model):
    _name = 'serial.owner'
    _inherit = 'mail.thread'

    _description = 'Serial number onwership'

    serial_number_id = fields.Many2one(
        comodel_name='stock.production.lot',
        string='Serial Number',
        required=True,
    )
    product_id = fields.Many2one(
        related='serial_number_id.product_id',
        string='Product',
    )
    product_name = fields.Char(
        related='serial_number_id.product_id.name',
        string='Product',
        readonly=True,
    )
    reseller_id = fields.Many2one(
        comodel_name='res.partner',
        string='Reseller',
        domain=lambda self: self._get_reseller_domain(),
        track_visibility='onchange',
    )
    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        domain=[('customer', '=', True)],
        track_visibility='onchange',
    )
    shipped_to_reseller_on = fields.Date(
        string='Shipped on',
        track_visibility='onchange',
    )
    registred_by_customer_on = fields.Date(
        string='Registred on',
        track_visibility='onchange',
    )

    @api.multi
    def _get_reseller_domain(self):
        entity = self.env.ref(
            'sf_partner_entity_type.entity_dealer',
            raise_if_not_found=False
            )
        if not entity:
            raise UserError(
                _("Entity type \"Dealer\" was removed. Please update"
                  " sf_partner_enityt_type module to restore it."))
        return [('entity_type_id', '=', entity.id),
                ('customer', '=', 'True')]
