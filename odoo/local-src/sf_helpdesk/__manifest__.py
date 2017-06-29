# -*- coding: utf-8 -*-
# Copyright 2017 Telmo Santos (senseFly SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sensefly helpdesk',
    'version': '1.0',
    'summary': 'Helpdesk, Ticket Support',
    'author': "senseFly, Telmo Santos",
    'website': 'https://www.sensefly.com/',
    'license': 'AGPL-3',
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
