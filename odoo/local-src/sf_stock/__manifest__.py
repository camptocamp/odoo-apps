# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Stock',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': [
        'stock',
        'sale_stock',
        'sf_report',
        'delivery',
        'stock_disable_force_availability_button',
        'sf_country',
        'stock_picking_wave',
        'sale_order_lot_selection'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/module_data.xml',
        'security/stock_security.xml',
        'views/stock_location.xml',
        'views/stock_production_lot.xml',
        'views/stock_picking.xml',
        'views/stock_inventory_category.xml',
        'views/stock_inventory.xml',
        'views/product_inventory_category.xml',
        'views/stock_picking_type.xml',
        'views/stock_incoterms_views.xml',
        'wizard/wizard_stock_picking_availability.xml',
        'report/sf_report_deliveryslip.xml',
        'report/sf_report_delivery_note.xml',
        'report/sf_report_commercial_invoice.xml',
        'report/sf_stock_report.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
