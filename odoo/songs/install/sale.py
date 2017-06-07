# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import anthem


@anthem.log
def settings(ctx):
    """ Configure sale settings """
    ctx.env['sale.config.settings'].create(
        {'auto_done_setting': False,
         'company_id': ctx.env.ref('base.main_company').id,
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
