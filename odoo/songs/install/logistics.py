# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def settings(ctx):
    """ Configure inventory settings """
    # Logistics settings for main company (senseFly SA CH)
    ctx.env['stock.config.settings'].create({
        'company_id': ctx.env.ref('base.main_company').id,
        'decimal_precision': 0,
        'group_product_variant': False,
        'group_stock_adv_location': 1,
        'group_stock_inventory_valuation': 1,
        'group_stock_multi_locations': True,
        'group_stock_multi_warehouses': False,
        'group_stock_packaging': False,
        'group_stock_production_lot': 1,
        'group_stock_tracking_lot': False,
        'group_stock_tracking_owner': False,
        'group_uom': 1,
        'group_warning_stock': 1,
        'module_delivery_dhl': True,
        'module_delivery_fedex': True,
        'module_delivery_temando': False,
        'module_delivery_ups': True,
        'module_delivery_usps': True,
        'module_procurement_jit': False,
        'module_product_expiry': False,
        'module_quality': False,
        'module_stock_barcode': True,
        'module_stock_calendar': False,
        'module_stock_dropshipping': 1,
        'module_stock_landed_costs': 1,
        'module_stock_picking_wave': 1,
        'propagation_minimum_delta': 0,
        'warehouse_and_location_usage_level': 1}).execute()
    # Logistics settings for second company (senseFly Inc USA)
    ctx.env['stock.config.settings'].create({
        'company_id': ctx.env.ref('__setup__.company_mte').id,
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
        'warehouse_and_location_usage_level': 1,
        'group_stock_adv_location': 0,
        'decimal_precision': 0,
        'module_stock_dropshipping': 1,
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
