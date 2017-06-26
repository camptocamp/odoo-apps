# -*- coding: utf-8 -*-
# Part of SenseFly.
{
    'name': "SenseFly Account Budget",
    'version': '2.0',
    'author': 'senseFly SA :: telmo.santos@sensefly.com',
    'website': 'http://www.sensefly.com',
    'category': 'SenseFly',
    'depends': [
        'account_accountant',
        'account',
        'account_fiscal_year',
        'sf_date_range',
        'analytic_tag_dimension',
        ],
    'data': [
        'data/sequence.xml',
        'views/budget_view.xml',
        'views/budget_import_view.xml',
        'views/res_config_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False
}
