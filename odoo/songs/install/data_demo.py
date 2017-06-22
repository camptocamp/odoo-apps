# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv

""" File for demo data

These songs will be called when the mode is 'demo', we should import only
excerpt of data, while the full data is only imported in the 'full' mode.

"""


@anthem.log
def import_users(ctx):
    """ Importing users from csv """
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/users.csv', model)


@anthem.log
def import_location(ctx):
    """ Importing customers from csv """
    load_csv(ctx, 'data/demo/stock_location.csv', 'stock.location')


@anthem.log
def import_customers(ctx):
    """ Importing stock location from csv """
    load_csv(ctx, 'data/demo/customers.csv', 'res.partner')


@anthem.log
def import_product(ctx):
    load_csv(ctx, 'data/demo/product.csv', 'product.template')


@anthem.log
def main(ctx):
    """ Loading demo data """
    import_users(ctx)
    import_location(ctx)
    import_customers(ctx)
    import_product(ctx)
