# -*- coding: utf-8 -*-
# Copyright  Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# -- This file has been generated --

import anthem


@anthem.log
def account_config_settings_sa(ctx):
    """ Setup account.config.settings for senseFly SA """
    model = ctx.env['account.config.settings'].with_context(
        {'tracking_disable': 1})
    model.create({
        # Lock Date  # noqa
        'fiscalyear_lock_date': False,
        # Bank Accounts Prefix *  # noqa
        'bank_account_code_prefix': '102',
        # Cash Accounts Prefix *  # noqa
        'cash_account_code_prefix': '100',
        # Assets management  # noqa
        'module_account_asset': True,
        # Initiating Party Identifier  # noqa
        'initiating_party_identifier': False,
        # Default company currency  # noqa
        'currency_id': ctx.env.ref('base.CHF').id,
        # Multiple identifiers  # noqa
        'group_pain_multiple_identifier': False,
        # Full accounting features: journals, legal statements, chart of
        # accounts, etc.  # noqa
        'module_account_accountant': True,
        # Automatic Currency Rates Download  # noqa
        'auto_currency_up': True,
        # Fiscalyear last day  # noqa
        'fiscalyear_last_day': 31,
        # Number of days between two follow-ups *  # noqa
        'days_between_two_followups': 14,
        # Budget period range type  # noqa
        'budget_range_type_id': ctx.env.ref(
            'sf_date_range.sf_date_range_type_month_sa').id,
        # This company has its own chart of accounts  # noqa
        'expects_chart_of_accounts': True,
        # Plaid Connector  # noqa
        'module_account_plaid': False,
        # Complete set of taxes  # noqa
        'complete_tax_set': False,
        # Minimum days between two follow-ups *  # noqa
        'min_days_between_followup': 6,
        # Template transfer account id  # noqa
        'template_transfer_account_id': False,
        # Import in .csv format  # noqa
        'module_account_bank_statement_import_csv': False,
        # Budget management  # noqa
        'module_account_budget': False,
        # Company  # noqa
        'company_id': ctx.env.ref('base.main_company').id,
        # Analytic accounting for sales  # noqa
        'group_analytic_account_for_sales': False,
        # Warning: An informative or blocking warning can be set on a partner
        # noqa
        'group_warning_account': 1,
        # Template  # noqa
        'chart_template_id': False,
        # Allow multi currencies  # noqa
        'group_multi_currency': True,
        # Allow pro-forma invoices  # noqa
        'group_proforma_invoices': False,
        # Revenue Recognition  # noqa
        'module_account_deferred_revenue': False,
        # Company has a chart of accounts  # noqa
        'has_chart_of_accounts': False,
        # Has default company  # noqa
        'has_default_company': False,
        # Lock Date for Non-Advisers  # noqa
        'period_lock_date': False,
        # Purchase tax (%)  # noqa
        'purchase_tax_rate': 0.0,
        # Interval Unit: Manually  # noqa
        'currency_interval_unit': 'manually',
        # Import in .ofx format  # noqa
        'module_account_bank_statement_import_ofx': False,
        # Allow check printing and deposits  # noqa
        'module_l10n_us_check_printing': False,
        # Default Purchase Tax  # noqa
        'default_purchase_tax_id': False,
        # Service Provider: European Central Bank  # noqa
        'currency_provider': 'ecb',
        # Analytic accounting  # noqa
        'group_analytic_accounting': True,
        # Use Anglo-Saxon Accounting *  # noqa
        'use_anglo_saxon': False,
        # Sales tax (%)  # noqa
        'sale_tax_rate': 0.0,
        # Use batch deposit  # noqa
        'module_account_batch_deposit': False,
        # Import .qif files  # noqa
        'module_account_bank_statement_import_qif': False,
        # Bank Interface - Sync your bank feeds automatically  # noqa
        'module_account_yodlee': False,
        # Allow Tax Cash Basis  # noqa
        'module_account_tax_cash_basis': False,
        # # of Digits *  # noqa
        'code_digits': 5,
        # Initiating Party Issuer  # noqa
        'initiating_party_issuer': False,
        # Default Sale Tax  # noqa
        'default_sale_tax_id': False,
        # Overdue Payments Message *  # noqa
        'overdue_msg': """Dear Sir/Madam,

Our records indicate that some payments on your account are still due.
Please find details below.
If the amount has already been paid, please disregard this notice.
Otherwise, please forward us the total amount stated below.
If you have any queries regarding your account, Please contact us.

Thank you in advance for your cooperation.
Best Regards,""",
        # Default sale tax  # noqa
        'sale_tax_id': False,
        # Rate Difference Journal  # noqa
        'currency_exchange_journal_id': False,
        # Use SEPA payments  # noqa
        'module_account_sepa': False,
        # Get dynamic accounting reports  # noqa
        'module_account_reports': True,
        # Next Execution Date  # noqa
        'currency_next_execution_date': False,
        # Analytic accounting for purchases  # noqa
        'group_analytic_account_for_purchases': True,
        # Bank accounts footer preview  # noqa
        'company_footer': False,
        # Fiscalyear last month: December  # noqa
        'fiscalyear_last_month': 12,
        # Tax calculation rounding method *: Round per Line  # noqa
        'tax_calculation_rounding_method': 'round_per_line',
        # Enable payment followup management  # noqa
        'module_account_reports_followup': True,
        # Default purchase tax  # noqa
        'purchase_tax_id': False,
        # Inter-Banks Transfer Account  # noqa
        'transfer_account_id': ctx.env.ref('l10n_ch.1_transfer_account_id').id,

    }).execute()


@anthem.log
def main(ctx):
    account_config_settings_sa(ctx)
