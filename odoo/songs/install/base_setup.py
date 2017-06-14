# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import anthem


@anthem.log
def settings(ctx):
    """ Configure General Settings """
    for cp in ctx.env['res.company'].search([]):
        ctx.env['base.config.settings'].create(
            {'alias_domain': u'localhost',
             'auth_signup_reset_password': False,
             'auth_signup_template_user_id': ctx.env.ref(
                 'auth_signup.default_template_user').id,
             'auth_signup_uninvited': False,
             'company_id': cp.id,
             'company_share_partner': False,
             'company_share_product': False,
             'custom_footer': False,
             'fail_counter': 1,
             'fcm_api_key': False,
             'fcm_project_id': False,
             'font': False,
             'group_multi_company': True,
             'group_multi_currency': True,
             'group_product_variant': False,
             'ldaps': [],
             'module_auth_oauth': False,
             'module_base_import': True,
             'module_google_calendar': False,
             'module_google_drive': False,
             'module_inter_company_rules': False,
             'module_portal': True,
             'module_share': False,
             'paperformat_id': ctx.env.ref('report.paperformat_euro').id,
             'rml_footer': False,
             'rml_footer_readonly': False,
             'rml_paper_format': u'a4'}
        ).execute()
