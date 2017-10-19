# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Purchase',
    'version': '1.0',
    'author': 'Telmo Santos',
    'website': 'https://www.sensefly.com',
    'category': 'SenseFly',
    'depends': ['purchase'],
    'data': [
        'report/sf_purchase_order_templates.xml',
        'report/sf_purchase_order_internal.xml',
        'report/sf_purchase_quotation_templates.xml',
        'report/sf_purchase_reports.xml',
        'views/purchase.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
