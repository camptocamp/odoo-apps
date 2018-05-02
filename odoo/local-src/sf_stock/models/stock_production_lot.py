# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from random import randint
import uuid


def gen_key():
    return '{}-{}'.format(randint(1000, 9990), randint(1000, 9990))


class ProductionLot(models.Model):

    _inherit = 'stock.production.lot'

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        default['uuid'] = uuid.uuid4()
        return super(ProductionLot, self).copy(default)

    @api.multi
    def action_set_invitation_key(self):
        """Assign invitation key and call api"""
        self.set_invitation_key()
        InterfaceObj = self.env['sf.mysensefly.interface']
        for lot in self:
            category = lot.product_id.categ_id.parent_id.name or ''
            code = lot.product_id.categ_id.name or ''
            data = {
                "invitationKey": lot.invitation_key,
                "product": {
                    "model": {
                        "category": category.lower(),
                        "code": code.lower(),
                        "designation": lot.product_id.name
                    },
                    "serialNumber": lot.name,
                    "uuid": lot.product_id.uuid
                }
            }
            InterfaceObj.assign_invitation_key(data)

    @api.multi
    def set_invitation_key(self):
        """Assign a unique invitation key to the lot with format: xxxx-xxxx"""
        for lot in self:
            key = gen_key()
            while self.search([('invitation_key', '=', key)]):
                # generate a new key until is found
                key = gen_key()
            lot.invitation_key = gen_key()

    uuid = fields.Char(
        'UUID', index=True, default=lambda self: '%s' % uuid.uuid4(),
        required=True)
    invitation_key = fields.Char(
        string='Invitation key',
        help='The person or entity with this key, owns the product '
             'with this serial number')
    warranty_end_date = fields.Date('Warranty end date')
    first_outgoing_stock_move_id = fields.Many2one(
        'stock.move', string='First outgoing stock move')
    product_tracking = fields.Selection(related='product_id.tracking',
                                        readonly=True,
                                        string='Product tracking')

    notes = fields.Text(string='Comment')

    _sql_constraints = [
        ('unique_uuid', 'UNIQUE(uuid)', 'UUID must be unique!'),
        ('unique_invitation_key', 'UNIQUE(invitation_key)',
         'Invitation key must be unique!'),
    ]
