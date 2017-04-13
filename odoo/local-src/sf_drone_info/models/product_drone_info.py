# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models

RESELLER_TYPE_SELECTION = [
    ('itrn', 'Internal'),
    ('srv', 'Service'),
    ('srvextd', 'Service Extended')
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    drone_type_ids = fields.Many2many('drone.type', string='Drone')
    product_reseller_type = fields.Selection(RESELLER_TYPE_SELECTION,
                                             string='Reseller Type')


class DroneType(models.Model):
    _name = "drone.type"
    _description = "Drone Type"

    name = fields.Char(required=True)
