# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def settings(ctx):
    """ Configure inventory settings """
    ctx.env['stock.config.settings'].create({
        'group_stock_production_lot': 1,
        'module_product_expiry': 0,
        'group_stock_tracking_lot': 0,
        'group_stock_tracking_owner': 0,
        'module_stock_barcode': False,
        'module_stock_landed_cost': 0,
        'group_stock_inventory_valuation': 0,
        'module_delivery_dhl': False,
        'module_delivery_fedex': False,
        'module_delivery_temando': False,
        'module_delivery_ups': False,
        'module_delivery_usps': False,
        'module_procurement_jit': 0,
        'warehouse_and_location_usage_level': 2,
        'group_stock_adv_location': 0,
        'decimal_precision': 0,
        'module_stock_dropshipping': 0,
        'module_stock_picking_wave': 1,
        'module_stock_calendar': 0,
        'group_uom': 0,
        'group_product_variant': 0,
        'group_stock_packaging': 0,
        'module_quality': True,
    }).execute()


@anthem.log
def main(ctx):
    """ Configuring logistics """
    settings(ctx)
