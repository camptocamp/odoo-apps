# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def settings(ctx):
    """ Configure Manufacturing settings """
    # Manufacturing settings for main company (senseFly SA CH)
    ctx.env['mrp.config.settings'].create({
        'company_id': ctx.env.ref('base.main_company').id,
        'group_mrp_routings': 1,
        'group_product_variant': False,
        'manufacturing_lead': 0.0,
        'manufacturing_period': u'week',
        'module_mrp_byproduct': False,
        'module_mrp_maintenance': False,
        'module_mrp_mps': 1,
        'module_mrp_plm': 1,
        'module_quality_mrp': False}).execute()
    # Manufacturing settings for second company (senseFly Inc USA)
    ctx.env['mrp.config.settings'].create({
        'company_id': ctx.env.ref('__setup__.company_mte').id,
        'group_mrp_routings': 1,
        'group_product_variant': False,
        'manufacturing_lead': 0.0,
        'module_mrp_byproduct': False,
        'module_mrp_maintenance': False,
        'module_mrp_mps': 1,
        'module_mrp_plm': 1,
        'module_quality_mrp': False}).execute()
