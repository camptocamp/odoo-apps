# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Product',
    'version': '1.0',
    'author': 'Telmo Santos',
    'category': 'SenseFly',
    'depends': ['product',
                'base_user_role',
                'sf_stock'],
    'description': """
This is a module for customization of senseFly products

Custom fields:

- origin_id - The country where the product/component was made or assembled.
- validated - Only validated product can be sold or purchased.
    """,
    'data': [
        'security/product_security.xml',
        'views/product.xml'
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
