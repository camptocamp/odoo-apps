# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def setup_ldap(ctx):
    company = ctx.env.ref('base.main_company')
    values = {
        'company': company.id,
        'ldap_server': '10.41.10.18',
        'ldap_server_port': '389',
        'ldap_password': 'xxx',
        'ldap_filter': '(userPrincipalName=%s)',
        'ldap_base':
            'OU=SENSEFLY_Users,OU=SENSEFLY,OU=SUBSIDIARIES,'
            'DC=PARROT,DC=BIZ',
        'ldap_binddn':
            'CN=Open Erp,'
            'OU=SENSEFLY_Users,OU=SENSEFLY,OU=SUBSIDIARIES,'
            'DC=PARROT,DC=BIZ',
        'create_user': False,
    }
    xmlid = '__setup__.ldap_config'
    create_or_update(ctx, 'res.company.ldap', xmlid, values)


@anthem.log
def main(ctx):
    """ Configuring ldap """
    setup_ldap(ctx)
