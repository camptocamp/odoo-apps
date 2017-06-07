# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def settings(ctx):
    """ Configure Manufacturing settings """
    ctx.env['mrp.config.settings'].create(
        {'company_id': ctx.env.ref('base.main_company').id,
         'group_mrp_routings': 1,
         'group_product_variant': False,
         'manufacturing_lead': 0.0,
         'module_mrp_byproduct': False,
         'module_mrp_maintenance': False,
         'module_mrp_mps': 1,
         'module_mrp_plm': 1,
         'module_quality_mrp': False}).execute()
