# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import anthem


@anthem.log
def settings(ctx):
    """ Configure Manufacturing settings"""
    ctx.env['mrp.config.settings'].create(
        {'company_id': ctx.env.ref('base.main_company').id,
         'group_mrp_routings': 1,
         'group_product_variant': False,
         'manufacturing_lead': 0.0,
         'manufacturing_period': u'week',
         'module_mrp_byproduct': False,
         'module_mrp_maintenance': False,
         'module_mrp_mps': 1,
         'module_mrp_plm': 1,
         'module_quality_mrp': False}
    ).execute()


@anthem.log
def main(ctx):
    """ Configuring manufacturing """
    settings(ctx)
