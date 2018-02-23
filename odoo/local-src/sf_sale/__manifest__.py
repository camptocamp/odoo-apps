# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Sale',
    'version': '1.0',
    'author': 'senseFly, Telmo Santos',
    'category': 'SenseFly',
    'depends': [
        'sale',
        'sf_report',
        'sf_product',
        'sf_stock',
        'delivery',
        'sale_exception',
        'sale_order_lot_selection',
    ],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'report/sf_sale_report_templates.xml',
        'report/sf_sale_report.xml',
        'data/mail_template_data.xml',
        'data/sale_exception_data.xml',
        'views/sale_views.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
