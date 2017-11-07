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
def import_users_groups(ctx):
    """ Importing groups to users from csv """
    load_csv(ctx, 'data/demo/users_group.csv', 'res.users')


@anthem.log
def import_country_state(ctx):
    """ Importing country states from csv """
    load_csv(ctx, 'data/demo/country_state.csv', 'res.country.state')


@anthem.log
def import_countries(ctx):
    """ Importing countries from csv """
    load_csv(ctx, 'data/demo/country.csv', 'res.country')


@anthem.log
def import_crm_team(ctx):
    """ Importing sales team / channel from csv """
    model = ctx.env['crm.team'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/crm_team.csv', model)


@anthem.log
def import_location(ctx):
    """ Importing stock location from csv """
    load_csv(ctx, 'data/demo/stock_location.csv', 'stock.location')


@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    model = ctx.env['res.partner'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/customers.csv', model)


@anthem.log
def import_suppliers(ctx):
    """ Importing suppliers from csv """
    model = ctx.env['res.partner'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/suppliers.csv', model)


@anthem.log
def import_drone_type(ctx):
    """ Importing drone type from csv """
    load_csv(ctx, 'data/demo/drone_type.csv', 'drone.type')


@anthem.log
def import_product(ctx):
    """ Importing products from csv """
    model = ctx.env['product.template'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/product.csv', model)


@anthem.log
def import_serial_number(ctx):
    """ Importing serial number from csv """
    load_csv(ctx, 'data/demo/serial.csv', 'stock.production.lot')


@anthem.log
def import_workcenter(ctx):
    """ Importing workcenters from csv """
    load_csv(ctx, 'data/demo/workcenter.csv', 'mrp.workcenter')


@anthem.log
def import_rma_cause(ctx):
    """ Importing RMA causes from csv """
    load_csv(ctx, 'data/demo/rma_cause.csv', 'sf.rma.cause')


@anthem.log
def import_bank(ctx):
    """ Importing bank from csv """
    load_csv(ctx, 'data/demo/bank.csv', 'res.bank')


@anthem.log
def import_bank_account(ctx):
    """ Importing bank account partners from csv """
    load_csv(ctx, 'data/demo/bank_account.csv', 'res.partner.bank')


@anthem.log
def import_sales_order(ctx):
    """ Importing sales order from csv """
    model = ctx.env['sale.order'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/sale_order_head.csv', model)
    load_csv(ctx, 'data/demo/sale_order_line.csv', 'sale.order.line')


@anthem.log
def import_waves(ctx):
    """ Importing waves from csv """
    load_csv(ctx, 'data/demo/wave.csv', 'stock.picking.wave')


@anthem.log
def main(ctx):
    """ Loading demo data """
    import_users(ctx)
    import_users_groups(ctx)
    import_country_state(ctx)
    import_countries(ctx)
    import_customers(ctx)
    import_suppliers(ctx)
    import_crm_team(ctx)
    import_waves(ctx)
    import_location(ctx)
    import_customers(ctx)
    import_drone_type(ctx)
    import_product(ctx)
    import_serial_number(ctx)
    import_workcenter(ctx)
    import_rma_cause(ctx)
    import_bank(ctx)
    import_bank_account(ctx)
    import_sales_order(ctx)
    return
