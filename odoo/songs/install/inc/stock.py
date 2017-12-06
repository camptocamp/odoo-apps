# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem
from ...common import load_csv




@anthem.log
def stock_config_settings_inc(ctx):
    """ Setup stock.config.settings for senseFly Inc """
    model = ctx.env['stock.config.settings'].with_context({'tracking_disable': 1})
    model.create({
        # Landed Costs: No landed costs  # noqa
        'module_stock_landed_costs': False,
        # Inventory Valuation: Periodic inventory valuation (recommended)  # noqa
        'group_stock_inventory_valuation': False,
        # Minimum Stock Rules: Set lead times in calendar days (easy)  # noqa
        'module_stock_calendar': False,
        # Barcode scanner support  # noqa
        'module_stock_barcode': False,
        # Picking Waves: Manage picking in batch per worker  # noqa
        'module_stock_picking_wave': 1,
        # Company  # noqa
        'company_id': ctx.env.ref('__setup__.company_inc').id,
        # Packages: Do not manage packaging  # noqa
        'group_stock_tracking_lot': False,
        # Product Variants: No variants on products  # noqa
        'group_product_variant': False,
        # Warning: An informative or blocking warning can be set on a partner  # noqa
        'group_warning_stock': 1,
        # Temando integration  # noqa
        'module_delivery_temando': False,
        # Lots and Serial Numbers: Track lots or serial numbers  # noqa
        'group_stock_production_lot': 1,
        # Manage several warehouses  # noqa
        'group_stock_multi_warehouses': True,
        # Product Owners: All products in your warehouse belong to your company  # noqa
        'group_stock_tracking_owner': False,
        # Minimum days to trigger a propagation of date change in pushed/pull flows.  # noqa
        'propagation_minimum_delta': 0,
        # USPS integration  # noqa
        'module_delivery_usps': False,
        # Dropshipping: Allow suppliers to deliver directly to your customers  # noqa
        'module_stock_dropshipping': 1,
        # Quality  # noqa
        'module_quality': False,
        # Procurements: Reserve products manually or based on automatic scheduler  # noqa
        'module_procurement_jit': False,
        # Packaging Methods: Do not manage packaging  # noqa
        'group_stock_packaging': False,
        # Fedex integration  # noqa
        'module_delivery_fedex': True,
        # Decimal precision on weight  # noqa
        'decimal_precision': 3,
        # Units of Measure: Some products may be sold/purchased in different units of measure (advanced)  # noqa
        'group_uom': 1,
        # Warehouses and Locations usage level: Manage several Warehouses, each one composed by several stock locations  # noqa
        'warehouse_and_location_usage_level': 2,
        # UPS integration  # noqa
        'module_delivery_ups': True,
        # Expiration Dates: Do not use Expiration Date on serial numbers  # noqa
        'module_product_expiry': False,
        # Manage several stock locations  # noqa
        'group_stock_multi_locations': True,
        # Routes: Advanced routing of products using rules  # noqa
        'group_stock_adv_location': 1,
        # DHL integration  # noqa
        'module_delivery_dhl': False,

    }).execute()


@anthem.log
def main(ctx):
    stock_config_settings_inc(ctx)
