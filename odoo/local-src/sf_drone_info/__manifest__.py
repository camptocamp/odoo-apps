# -*- coding: utf-8 -*-
# Part of SenseFly.
{
    'name': "SenseFly Drone Info",
    'version': '1.0',
    'depends': ['product'
                ],
    'author': "Telmo Santos",
    'category': 'SenseFly',
    'data': [
        'security/ir.model.access.csv',
        'views/product_drone_info.xml'
    ],
    'demo': ['data/partner_demo.xml',
             'data/product_demo.xml'],
    'installable': True,
    'application': True,
    'auto_install': False
}
