# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'Sensefly sale invoicing',
    'version': '1.0',
    'author': 'Telmo Santos',
    'website': 'https://www.sensefly.com',
    'category': 'SenseFly',
    'depends': ['sale_stock', 'account_invoice_fiscal_position_update'],
    'data': [
        'views/sale.xml',
        'views/payment_term.xml'
    ],
    'demo': [
        'demo/payment_term.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
