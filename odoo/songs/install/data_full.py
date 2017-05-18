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
def import_customers(ctx):
    """ Importing customers from csv """
    load_csv(ctx, 'data/install/customers.csv', 'res.partner')


@anthem.log
def import_suppliers(ctx):
    """ Importing customers from csv """
    load_csv(ctx, 'data/install/suppliers.csv', 'res.partner')


@anthem.log
def import_product(ctx):
    load_csv(ctx, 'data/install/product.csv', 'product.template')


@anthem.log
def main(ctx):
    """ Loading full data """
    import_customers(ctx)
    import_suppliers(ctx)
    import_product(ctx)
    return
