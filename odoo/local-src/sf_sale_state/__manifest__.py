# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sensefly sale state',
    'version': '10.0.1.0.0',
    'author': 'Camptocamp',
    'license': 'AGPL-3',
    'category': 'Sale',
    'depends': [
        'delivery',
        'sale',
        'sf_sale_invoicing',
        'sf_stock',
    ],
    'website': 'http://www.camptocamp.com',
    'data': [
        # Views
        'views/sale_order.xml',
    ],
    'installable': True,
}
