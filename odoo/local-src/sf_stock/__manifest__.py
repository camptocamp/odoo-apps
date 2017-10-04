# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Stock',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': ['stock', 'sale_stock', 'sf_report'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_location.xml',
        'views/stock_production_lot.xml',
        'views/stock_picking.xml',
        'views/stock_inventory_category.xml',
        'views/stock_inventory.xml',
        'views/product_inventory_category.xml',
        'report/sf_report_deliveryslip.xml',
        'report/sf_report_delivery_note.xml',
        'report/sf_stock_report.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
