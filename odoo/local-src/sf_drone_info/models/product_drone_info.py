# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models
from odoo.exceptions import MissingError
from odoo.tools.translate import _

RESELLER_TYPE_SELECTION = [
    ('itrn', 'Internal'),
    ('srv', 'Service'),
    ('srvextd', 'Service Extended')
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    drone_type_ids = fields.Many2many('drone.type', 'rel_product_drone_type',
                                      'product_template_id', 'drone_type_id',
                                      string='Drone')
    product_reseller_type = fields.Selection(RESELLER_TYPE_SELECTION,
                                             string='Reseller Type')


class DroneType(models.Model):
    _name = "drone.type"
    _description = "Drone Type"

    name = fields.Char(required=True)
    product_ids = fields.Many2many('product.template',
                                   'rel_product_drone_type',
                                   'drone_type_id', 'product_template_id',
                                   string='Product')

    def get_spare_parts(self, partner_id):
        """Retrieve spare parts of a drone type"""
        res = []

        if not self.env['res.partner'].search([('id', '=', partner_id)]):
            raise MissingError(_('Missing record!') + ':' +
                               _('Partner does not exists.'))

        pricelist_id = \
            self.env['res.partner'].browse(
                partner_id).property_product_pricelist

        for drone_type in self:
            spare_part_ids = drone_type.product_ids.filtered(
                lambda p: p.product_reseller_type == 'itrn'
                or not p.product_reseller_type)

            spare_parts = [{'id': sp.id,
                            'name_template': sp.name,
                            'default_code': sp.default_code,
                            'price':
                                pricelist_id.price_get(
                                    sp.product_variant_id.id, 1, partner_id)
                                [pricelist_id.id],
                            'currency': pricelist_id.currency_id.name
                            } for sp in spare_part_ids]

            res += spare_parts

        return res
