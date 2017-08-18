# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'Sales Forecast',
    'summary': 'Sensefly dealers sales forecast',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'Sales',
    'depends': ['sale', 'sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_forecast.xml',
        'views/forecast_import.xml',
        'views/res_config_view.xml',
        'data/sequence.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
