# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os

from base64 import b64encode
from pkg_resources import resource_string, resource_stream

import anthem

from anthem.lyrics.records import create_or_update
from anthem.lyrics.loaders import load_csv_stream

from ..common import req


@anthem.log
def setup_companies(ctx):
    """ Setup companies """
    content = resource_stream(req, 'data/install/res.company.csv')
    load_csv_stream(ctx, 'res.company', content, delimiter=',')

    holding = ctx.env.ref('base.main_company')

    with ctx.log(u'Set main company logo'):
        logo_content = resource_string(
            req, 'data/images/company_main_logo.png')
        b64_logo = b64encode(logo_content)
        holding.logo = b64_logo


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR',):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })


@anthem.log
def admin_user_password(ctx):
    """ Changing admin password """
    # TODO default admin password for the test server, must be changed
    # To get an encrypted password:
    # $ docker-compose run --rm odoo python -c \
    # "from passlib.context import CryptContext; \
    #  print CryptContext(['pbkdf2_sha512']).encrypt('my_password')"
    if os.environ.get('RUNNING_ENV') == 'dev':
        ctx.log_line('Not changing password for dev RUNNING_ENV')
        return
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$tVYq5dwbI0Tofc85RwiBcA$a1tNyzZ0hxW9kXKIyEwN1'
        'j84z5gIIi1PQmvtFHuxQ4rNA2RaXSGLjXnEifl6ZQZ/wiBJK6fZkeaGgF3DW9A2Bg'
    )


@anthem.log
def change_config_parameters(ctx):
    """ fix config parameters for reports styles """
    url = "http://localhost:8069"
    SysParam = ctx.env['ir.config_parameter']
    SysParam.set_param('web.base.url', url)
    SysParam.set_param('web.base.url.freeze', 'True')


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_companies(ctx)
    setup_language(ctx)
    admin_user_password(ctx)
    change_config_parameters(ctx)
