# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem


@anthem.log
def settings(ctx):
    """ Configure Accounting settings"""
    # General settings for main company (senseFly SA CH)
    ctx.env['account.config.settings'].create(
        {'bank_account_code_prefix': u'102',
         'cash_account_code_prefix': u'100',
         'chart_template_id': False,
         'code_digits': 5,
         'company_footer': False,
         'company_id': ctx.env.ref('base.main_company').id,
         'complete_tax_set': False,
         'currency_exchange_journal_id': (4, u'Exchange Difference (CHF)'),
         'currency_id': ctx.env.ref('base.CHF').id,
         'currency_interval_unit': u'manually',
         'currency_next_execution_date': False,
         'currency_provider': u'ecb',
         'days_between_two_followups': 14,
         'default_purchase_tax_id': ctx.env.ref(
             'l10n_ch.1_vat_XO').id,
         'default_sale_tax_id': ctx.env.ref('l10n_ch.1_vat_O_exclude').id,
         'expects_chart_of_accounts': True,
         'fiscalyear_last_day': 31,
         'fiscalyear_last_month': 12,
         'fiscalyear_lock_date': False,
         'group_analytic_account_for_purchases': True,
         'group_analytic_account_for_sales': False,
         'group_analytic_accounting': True,
         'group_multi_currency': True,
         'group_proforma_invoices': False,
         'group_warning_account': 1,
         'has_chart_of_accounts': True,
         'has_default_company': False,
         'initiating_party_identifier': False,
         'initiating_party_issuer': False,
         'min_days_between_followup': 6,
         'module_account_accountant': True,
         'module_account_asset': True,
         'module_account_bank_statement_import_csv': False,
         'module_account_bank_statement_import_ofx': True,
         'module_account_bank_statement_import_qif': False,
         'module_account_batch_deposit': False,
         'module_account_budget': False,
         'module_account_deferred_revenue': False,
         'module_account_plaid': False,
         'module_account_reports': True,
         'module_account_reports_followup': True,
         'module_account_sepa': False,
         'module_account_tax_cash_basis': False,
         'module_account_yodlee': False,
         'module_l10n_us_check_printing': False,
         'overdue_msg': u'Dear Sir/Madam,\n\nOur records indicate that some payments on your account are still due. Please find details below.\nIf the amount has already been paid, please disregard this notice. Otherwise, please forward us the total amount stated below.\nIf you have any queries regarding your account, Please contact us.\n\nThank you in advance for your cooperation.\nBest Regards,',  # noqa
         'period_lock_date': False,
         'purchase_tax_id': False,
         'purchase_tax_rate': 15.0,
         'sale_tax_id': False,
         'sale_tax_rate': 15.0,
         'tax_calculation_rounding_method': u'round_per_line',
         'template_transfer_account_id': False,
         'transfer_account_id': ctx.env.ref(
             'l10n_ch.1_transfer_account_id').id,
         'use_anglo_saxon': False}
    ).execute()
    # General settings for second company (senseFly Inc USA)
    ctx.env['account.config.settings'].create(
        {'bank_account_code_prefix': u'102',
         'cash_account_code_prefix': u'100',
         'chart_template_id': False,
         'code_digits': 5,
         'company_footer': False,
         'company_id': ctx.env.ref('__setup__.company_mte').id,
         'complete_tax_set': False,
         'currency_exchange_journal_id': False,
         'currency_id': ctx.env.ref('base.USD').id,
         'currency_interval_unit': u'manually',
         'currency_next_execution_date': False,
         'currency_provider': u'ecb',
         'days_between_two_followups': 14,
         'default_purchase_tax_id': False,
         'default_sale_tax_id': False,
         'expects_chart_of_accounts': True,
         'fiscalyear_last_day': 31,
         'fiscalyear_last_month': 12,
         'fiscalyear_lock_date': False,
         'group_analytic_account_for_purchases': True,
         'group_analytic_account_for_sales': False,
         'group_analytic_accounting': True,
         'group_multi_currency': True,
         'group_proforma_invoices': False,
         'group_warning_account': 1,
         'has_chart_of_accounts': False,
         'has_default_company': False,
         'initiating_party_identifier': False,
         'initiating_party_issuer': False,
         'min_days_between_followup': 6,
         'module_account_accountant': True,
         'module_account_asset': True,
         'module_account_bank_statement_import_csv': False,
         'module_account_bank_statement_import_ofx': True,
         'module_account_bank_statement_import_qif': False,
         'module_account_batch_deposit': False,
         'module_account_budget': False,
         'module_account_deferred_revenue': False,
         'module_account_plaid': False,
         'module_account_reports': True,
         'module_account_reports_followup': True,
         'module_account_sepa': False,
         'module_account_tax_cash_basis': False,
         'module_account_yodlee': False,
         'module_l10n_us_check_printing': False,
         'overdue_msg': u'Dear Sir/Madam,\n\nOur records indicate that some payments on your account are still due. Please find details below.\nIf the amount has already been paid, please disregard this notice. Otherwise, please forward us the total amount stated below.\nIf you have any queries regarding your account, Please contact us.\n\nThank you in advance for your cooperation.\nBest Regards,',  # noqa
         'period_lock_date': False,
         'purchase_tax_id': False,
         'purchase_tax_rate': 15.0,
         'sale_tax_id': False,
         'sale_tax_rate': 15.0,
         'tax_calculation_rounding_method': u'round_per_line',
         'template_transfer_account_id': False,
         'transfer_account_id': False,
         'use_anglo_saxon': False}
    ).execute()


@anthem.log
def main(ctx):
    """ Configuring accounting """
    settings(ctx)
