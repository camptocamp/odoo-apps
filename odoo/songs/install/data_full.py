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
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/install/users.csv', model)


@anthem.log
def import_users_groups(ctx):
    """ Importing groups to users from csv """
    load_csv(ctx, 'data/install/users_group.csv', 'res.users')


@anthem.log
def import_country_state(ctx):
    """ Importing country states from csv """
    load_csv(ctx, 'data/install/country_state.csv', 'res.country.state')


@anthem.log
def import_countries(ctx):
    """ Importing countries from csv """
    load_csv(ctx, 'data/install/country.csv', 'res.country')


@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    load_csv(ctx, 'data/install/customers.csv', 'res.partner')


@anthem.log
def import_suppliers(ctx):
    """ Importing suppliers from csv """
    load_csv(ctx, 'data/install/suppliers.csv', 'res.partner')


@anthem.log
def import_crm_team(ctx):
    """ Importing sales team / channel from csv """
    load_csv(ctx, 'data/install/crm_team.csv', 'crm.team')


@anthem.log
def import_location(ctx):
    """ Importing stock location from csv """
    load_csv(ctx, 'data/install/stock_location.csv', 'stock.location')


@anthem.log
def import_drone_type(ctx):
    """ Importing drone type from csv """
    load_csv(ctx, 'data/install/drone_type.csv', 'drone.type')


@anthem.log
def import_product(ctx):
    """ Importing products type from csv """
    load_csv(ctx, 'data/install/product.csv', 'product.template')


@anthem.log
def import_workcenter(ctx):
    """ Importing workcenters from csv """
    load_csv(ctx, 'data/install/workcenter.csv', 'mrp.workcenter')


@anthem.log
def import_rma_cause(ctx):
    """ Importing RMA causes from csv """
    load_csv(ctx, 'data/install/rma_cause.csv', 'sf.rma.cause')


@anthem.log
def import_bank(ctx):
    """ Importing bank from csv """
    load_csv(ctx, 'data/install/bank.csv', 'res.bank')


@anthem.log
def main(ctx):
    """ Loading full data """
    import_users(ctx)
    import_users_groups(ctx)
    import_country_state(ctx)
    import_countries(ctx)
    import_customers(ctx)
    import_suppliers(ctx)
    import_crm_team(ctx)
    import_location(ctx)
    import_drone_type(ctx)
    import_product(ctx)
    import_workcenter(ctx)
    import_rma_cause(ctx)
    import_bank(ctx)
    return
