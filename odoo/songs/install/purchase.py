# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import anthem


@anthem.log
def settings(ctx):
    """ Configure Purchases settings """
    # Purchases settings for main company (senseFly SA CH)
    ctx.env['purchase.config.settings'].create({
        'company_currency_id': ctx.env.ref('base.CHF').id,
        'company_id': ctx.env.ref('base.main_company').id,
        'group_costing_method': 1,
        'group_manage_vendor_price': False,
        'group_product_variant': False,
        'group_uom': 1,
        'group_warning_purchase': False,
        'module_purchase_requisition': False,
        'module_stock_dropshipping': 1,
        'po_double_validation': u'one_step',
        'po_double_validation_amount': 5000.0,
        'po_lead': 0.0,
        'po_lock': u'edit'}).execute()
    # Purchases settings for second company (senseFly Inc USA)
    ctx.env['purchase.config.settings'].create({
        'company_currency_id': ctx.env.ref('base.USD').id,
        'company_id': ctx.env.ref('__setup__.company_inc').id,
        'group_costing_method': False,
        'group_manage_vendor_price': False,
        'group_product_variant': False,
        'group_uom': False,
        'group_warning_purchase': False,
        'module_purchase_requisition': False,
        'module_stock_dropshipping': False,
        'po_double_validation': u'one_step',
        'po_double_validation_amount': 5000.0,
        'po_lead': 0.0,
        'po_lock': u'edit'}).execute()
