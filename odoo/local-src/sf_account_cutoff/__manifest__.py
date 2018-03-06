# -*- coding: utf-8 -*-
# Part of SenseFly.
{
    'name': 'SenseFly Account Cut-off',
    'version': '10.0.1.0.0',
    'website': 'http://www.sensefly.com',
    'category': 'SenseFly',
    'depends': [
        'account_cutoff_base',
        'account_cutoff_accrual_picking',
    ],
    'data': [
        'views/account_cutoff.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
