# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Sale',
    'version': '1.0',
    'author': 'senseFly, Telmo Santos',
    'category': 'SenseFly',
    'depends': ['sale', 'sf_report', 'sf_product'],
    'license': 'AGPL-3',
    'data': [
        'report/sf_sale_report_templates.xml',
        'report/sf_sale_report.xml'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
