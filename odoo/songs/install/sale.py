# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import anthem


@anthem.log
def settings(ctx):
    """ Configure sale settings """
    # Sales settings for main company (senseFly SA CH)
    ctx.env['sale.config.settings'].create({
        'alias_domain': u'localhost',
        'alias_prefix': u'info',
        'auto_done_setting': False,
        'company_id': ctx.env.ref('base.main_company').id,
        'default_invoice_policy': u'delivery',
        'default_picking_policy': False,
        'deposit_product_id_setting': False,
        'generate_sales_team_alias': True,
        'group_discount_per_so_line': 1,
        'group_display_incoterm': 1,
        'group_mrp_properties': False,
        'group_pricelist_item': True,
        'group_product_pricelist': False,
        'group_product_variant': False,
        'group_route_so_lines': 1,
        'group_sale_delivery_address': 1,
        'group_sale_layout': 1,
        'group_sale_pricelist': True,
        'group_show_price_subtotal': False,
        'group_show_price_total': True,
        'group_uom': 1,
        'group_use_lead': False,
        'group_warning_sale': 1,
        'module_crm_voip': False,
        'module_delivery': 1,
        'module_sale_contract': False,
        'module_sale_margin': False,
        'module_sale_order_dates': 1,
        'module_website_quote': False,
        'module_website_sale_digital': False,
        'module_website_sign': False,
        'sale_note': False,
        'sale_pricelist_setting': u'formula',
        'sale_show_tax': u'total',
        'security_lead': 0.0}
    ).execute()
    # Sales settings for second company (senseFly Inc USA)
    ctx.env['sale.config.settings'].create({
        'auto_done_setting': False,
        'company_id': ctx.env.ref('__setup__.company_mte').id,
        'default_invoice_policy': u'order',
        'default_picking_policy': False,
        'deposit_product_id_setting': False,
        'group_discount_per_so_line': 1,
        'group_display_incoterm': False,
        'group_mrp_properties': False,
        'group_pricelist_item': True,
        'group_product_pricelist': False,
        'group_product_variant': False,
        'group_route_so_lines': False,
        'group_sale_delivery_address': False,
        'group_sale_layout': False,
        'group_sale_pricelist': True,
        'group_show_price_subtotal': True,
        'group_show_price_total': False,
        'group_uom': False,
        'group_warning_sale': 1,
        'module_delivery': False,
        'module_sale_contract': False,
        'module_sale_margin': False,
        'module_sale_order_dates': False,
        'module_website_quote': False,
        'module_website_sale_digital': False,
        'sale_note': False,
        'sale_pricelist_setting': u'formula',
        'sale_show_tax': u'subtotal',
        'security_lead': 0.0}).execute()
