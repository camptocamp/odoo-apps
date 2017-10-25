# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'senseFly Emoji',
    'version': '1.0',
    'category': 'Extra',
    'summary': 'Customized emojis for senseFly',
    'description': """
This module removes/adds emojis for chat module
===============================================
 """,
    'website': 'https://www.sensefly.com',
    'depends': ['base', 'mail'],
    'data': [
        'data/sensefly_emojis.xml',
    ],
    'qweb': [],
    'demo': [],
    'css': [],
    'installable': True,
    'auto_install': False,
}
