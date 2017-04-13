# -*- coding: utf-8 -*-
# Part of SenseFly.
{
    'name': "SenseFly Drone Info",
    'version': '1.0',
    'depends': ['product'
                ],
    'author': "Telmo Santos",
    'category': 'SenseFly',
    'description': """
Extends product with the details of the drone adding the following information:
1. The type of drone
2. The type of reseller that will use this product.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/product_drone_info.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}
