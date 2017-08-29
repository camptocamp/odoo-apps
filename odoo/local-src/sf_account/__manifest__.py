# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Account',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': ['account'],
    'data': [
        'data/invoice_action_data.xml',
        'views/account_journal.xml',
        'views/account_account.xml',
        'views/account_invoice.xml',
        'report/sf_report_invoice.xml',
        'report/sf_account_report.xml'
        ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
