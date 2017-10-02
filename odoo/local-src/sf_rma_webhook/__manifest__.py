# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'RMA Web Hook',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': ['sf_rma', 'sf_rma_sale_order'],
    'data': [
        'security/ir.model.access.csv',
        'views/rma_config_settings.xml',
        'data/base_url_data.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
