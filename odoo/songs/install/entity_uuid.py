# -*- coding: utf-8 -*-
# Part of sensefly.

import anthem
import uuid

""" Post processing assign entity UUID

This song will assign a random UUID to partners, products and serial numbers

"""


@anthem.log
def assign_uuid(ctx):
    """Assign UUID to products, partners and serial numbers"""
    products = ctx.env['product.product'].search(
        ['|', ('active', '=', True), ('active', '=', False)]
    )
    for product in products:
        product.uuid = uuid.uuid4()

    partners = ctx.env['res.partner'].search(
        ['|', ('active', '=', True), ('active', '=', False)]
    )
    for partner in partners:
        partner.uuid = uuid.uuid4()

    lots = ctx.env['stock.production.lot'].search([])
    for lot in lots:
        lot.uuid = uuid.uuid4()
