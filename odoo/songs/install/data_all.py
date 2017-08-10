# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.records import create_or_update
from ..common import load_csv


""" Data loaded in all modes
The data loaded here will be loaded in the 'demo' and
'full' modes.
"""


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
def main(ctx):
    """ Loading data """
    create_analytic_dimension(ctx)
    import_analytic_tag(ctx)
    import_analytic_account_project(ctx)
    import_partner_entity(ctx)
    import_product_category(ctx)
    import_account_tag_pl_name(ctx)
    import_account_tag_parrot_category(ctx)
