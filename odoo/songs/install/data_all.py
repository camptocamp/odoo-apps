# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from ..common import load_csv

""" Data loaded in all modes
The data loaded here will be loaded in the 'demo' and
'full' modes.
"""


@anthem.log
def import_analytic_account_project(ctx):
    """ Importing analytic account (project) from csv """
    load_csv(ctx, 'data/install/analytic_account_project.csv',
             'account.analytic.account')


@anthem.log
def main(ctx):
    """ Loading data """
    import_analytic_account_project(ctx)
