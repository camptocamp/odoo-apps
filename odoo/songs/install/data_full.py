# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv

""" File for full (production) data

These songs will be called on integration and production server at the
installation.

"""


@anthem.log
def import_users(ctx):
    """ Importing users from csv """
    load_csv(ctx, 'data/install/users.csv', 'res.users')


@anthem.log
def import_crm_team(ctx):
    """ Importing sales team / channel from csv """
    load_csv(ctx, 'data/demo/crm_team.csv', 'crm.team')


@anthem.log
def import_product(ctx):
    load_csv(ctx, 'data/install/product.csv', 'product.template')


@anthem.log
def main(ctx):
    """ Loading full data """
    import_users(ctx)
    import_crm_team(ctx)
    import_product(ctx)
    return
