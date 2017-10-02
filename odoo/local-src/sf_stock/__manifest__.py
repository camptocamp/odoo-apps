# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Stock',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': ['stock', 'sale_stock', 'sf_report'],
    'data': [
        'views/stock_location.xml',
        'views/stock_production_lot.xml',
        'views/stock_picking.xml',
        'views/stock_picking_type.xml',
        'report/sf_report_deliveryslip.xml',
        'report/sf_report_delivery_note.xml',
        'report/sf_stock_report.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
