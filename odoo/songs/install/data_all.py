# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import csv
from anthem.lyrics.records import create_or_update
from ..common import load_csv
from pkg_resources import Requirement, resource_stream


""" Data loaded in all modes
The data loaded here will be loaded in the 'demo' and
'full' modes.
"""


req = Requirement.parse('sensefly-odoo')


@anthem.log
def create_date_range(ctx):
    """ Create date.ranges (periods) for 2017 from csv """
    load_csv(ctx, 'data/install/date_range.csv',
             'date.range')


@anthem.log
def create_analytic_dimension(ctx):
    """ Creating Analytic Dimension tag  """
    create_or_update(ctx, 'account.analytic.dimension',
                     '__setup__.account_analytic_dimension_team',
                     {'name': 'Team', 'code': 'T'})


@anthem.log
def import_analytic_tag(ctx):
    """ Importing Analytic tag (team) from csv """
    load_csv(ctx, 'data/install/analytic_tag.csv',
             'account.analytic.tag')


@anthem.log
def import_analytic_account_project(ctx):
    """ Importing analytic account (project) from csv """
    load_csv(ctx, 'data/install/analytic_account_project.csv',
             'account.analytic.account')


@anthem.log
def import_partner_entity(ctx):
    """ Importing partner entity from csv """
    load_csv(ctx, 'data/install/partner_entity.csv',
             'res.partner.entity.type')


@anthem.log
def import_product_category(ctx):
    """ Importing product category from csv """
    load_csv(ctx, 'data/install/product_category.csv',
             'product.category')


@anthem.log
def import_unit_measure(ctx):
    """ Importing unit measure from csv """
    load_csv(ctx, 'data/install/unitmeasure.csv', 'product.uom')


@anthem.log
def import_account_tag_pl_name(ctx):
    """ Importing account tag (PL name)  from csv """
    load_csv(ctx, 'data/install/account_tag_pl.csv',
             'account.account.tag')


@anthem.log
def import_account_tag_parrot_category(ctx):
    """ Importing account tag (parrot category) from csv """
    load_csv(ctx, 'data/install/account_tag_parrot.csv',
             'account.account.tag')


@anthem.log
def import_account_fiscal_position(ctx):
    """ Importing account fiscal postition from csv """
    load_csv(ctx, 'data/install/fiscal_position.csv',
             'account.fiscal.position')
    load_csv(ctx, 'data/install/fiscal_position_tax.csv',
             'account.fiscal.position.tax')


@anthem.log
def delete_account(ctx):
    """ Delete standard chart of accounts from csv """
    # Read the CSV
    content = resource_stream(req, 'data/install/account_delete.csv')

    # Create list of dictionnaries
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(content, skipinitialspace=True)
        ]

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'], raise_if_not_found=False)
        if rec:
            rec.unlink()


@anthem.log
def import_account_account(ctx):
    """ Importing chart of accounts from csv """
    load_csv(ctx, 'data/install/account.csv',
             'account.account')


def import_email_template(ctx):
    """ Importing email template from csv """
    load_csv(ctx, 'data/install/email_template.csv', 'mail.template')


@anthem.log
def update_picking_type(ctx):
    """ Update stock picking type names """
    for record in ctx.env['stock.picking.type'].search(
            [('name', '=', 'Pick')]):
        record.name = 'Reserve & Pack'
    for record in ctx.env['stock.picking.type'].search(
            [('name', '=', 'Pack')]):
            record.name = 'Freight Labeling'


@anthem.log
def update_procurement_rule(ctx):
    """ Update procurement rule names """
    for record in ctx.env['procurement.rule'].search(
            [('name', '=', 'WH: Output -> Customers')]):
        record.name = 'WH: Pickup -> Customers'
    for record in ctx.env['procurement.rule'].search(
            [('name', '=', 'WH: Packing Zone -> Output')]):
        record.name = 'WH: Packs Zone -> Pickup'


@anthem.log
def update_stock_location(ctx):
    """ Update stock location names """
    create_or_update(ctx, 'stock.location',
                     'stock.location_pack_zone',
                     {'name': 'Packs'})
    create_or_update(ctx, 'stock.location',
                     'stock.stock_location_output',
                     {'name': 'Pickup'})


@anthem.log
def main(ctx):
    """ Loading data """
    create_analytic_dimension(ctx)
    import_analytic_tag(ctx)
    import_analytic_account_project(ctx)
    import_partner_entity(ctx)
    import_product_category(ctx)
    import_unit_measure(ctx)
    import_account_tag_pl_name(ctx)
    import_account_tag_parrot_category(ctx)
    import_account_fiscal_position(ctx)
    delete_account(ctx)
    import_account_account(ctx)
    create_date_range(ctx)
    import_email_template(ctx)
    update_picking_type(ctx)
    update_procurement_rule(ctx)
    update_stock_location(ctx)
