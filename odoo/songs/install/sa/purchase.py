# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem


@anthem.log
def purchase_config_settings_sa(ctx):
    """ Setup purchase.config.settings for senseFly SA """
    model = ctx.env['purchase.config.settings'].with_context(
        {'tracking_disable': 1})
    model.create({
        # Units of Measure: Some products may be sold/puchased in different units of measure (advanced)  # noqa
        'group_uom': 1,
        # Warning: All the products and the customers can be used in purchase orders  # noqa
        'group_warning_purchase': False,
        # Dropshipping: Allow suppliers to deliver directly to your customers  # noqa
        'module_stock_dropshipping': 1,
        # Costing Methods: Use a 'Fixed', 'Real' or 'Average' price costing method  # noqa
        'group_costing_method': 1,
        # Calls for Tenders: Purchase propositions trigger draft purchase orders to a single supplier  # noqa
        'module_purchase_requisition': False,
        # Levels of Approvals *: Confirm purchase orders in one step  # noqa
        'po_double_validation': 'one_step',
        # Company  # noqa
        'company_id': ctx.env.ref('base.main_company').id,
        # Currency  # noqa
        'company_currency_id': ctx.env.ref('base.CHF').id,
        # Vendor Price: Manage vendor price on the product form  # noqa
        'group_manage_vendor_price': False,
        # Purchase Lead Time *  # noqa
        'po_lead': 1.0,
        # Product Variants: No variants on products  # noqa
        'group_product_variant': False,
        # Purchase Order Modification *: Allow to edit purchase orders  # noqa
        'po_lock': 'edit',
        # Double validation amount *  # noqa
        'po_double_validation_amount': 5000.0,

    }).execute()


@anthem.log
def main(ctx):
    purchase_config_settings_sa(ctx)
