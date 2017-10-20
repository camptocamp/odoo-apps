# -*- coding: utf-8 -*-
# Copyright 2017 Telmo Santos (senseFly SA)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Sensefly helpdesk',
    'version': '1.0',
    'summary': 'Helpdesk, Ticket Support',
    'author': "senseFly, Telmo Santos",
    'website': 'https://www.sensefly.com/',
    'license': 'LGPL-3',
    'category': 'SenseFly',
    'images': [],
    'depends': ['helpdesk'],
    'data': [
        'data/sequence.xml',
        'views/helpdesk_ticket.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
