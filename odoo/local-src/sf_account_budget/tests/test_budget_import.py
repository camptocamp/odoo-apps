# -*- coding: utf-8 -*-

from odoo.tests.common import SavepointCase
from os import path
import base64
import os
import calendar
import pandas as pd


class TestBudgetImport(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestBudgetImport, cls).setUpClass()
        cls.company_id = cls.env['res.company']._company_default_get(
            'sf.account.budget_import').id

        # Account Type
        account_type_id = cls.env['account.account.type'].create(
            {'name': 'Expenses',
             'type': 'other'}).id

        # Accounts
        cls.env['account.account'].create(
            {'name': 'IT Small equipment',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 41220,
             'user_type_id': account_type_id
             }
        )
        cls.env['account.account'].create(
            {'name': 'Professional fees - Payroll Fees',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 42400,
             'user_type_id': account_type_id
             }
        )
        cls.env['account.account'].create(
            {'name': 'Accounting / Audit fees',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 66100,
             'user_type_id': account_type_id
             }
        )
        cls.env['account.account'].create(
            {'name': 'Bank costs',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 67100,
             'user_type_id': account_type_id
             }
        )
        cls.env['account.account'].create(
            {'name': 'Shipping costs',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 65110,
             'user_type_id': account_type_id
             }
        )
        cls.env['account.account'].create(
            {'name': 'Small equipment',
             'internal_type': 'other',
             'company_id': cls.company_id,
             'code': 41110,
             'user_type_id': account_type_id
             }
        )

        # Load Budget
        cls.name = 'budget_test.csv'
        test_file = path.join(
            os.path.dirname(
                path.realpath(__file__)), cls.name)
        with open(test_file, 'rb') as budget_file:
            cls.data = base64.b64encode(budget_file.read())

        # Analytic tag dimensions
        dimension_id = cls.env['account.analytic.dimension'].create(
            {'name': 'Team',
             'code': 'team'}
        ).id

        # Analytic tags
        cls.env['account.analytic.tag'].create(
            {'name': 'FIN',
             'analytic_dimension_id': dimension_id
             }
        )
        cls.env['account.analytic.tag'].create(
            {'name': 'IT',
             'analytic_dimension_id': dimension_id
             }
        )

        # Fiscal Year
        cls.env['date.range'].create(
            {'name': 2017,
             'company_id': cls.company_id,
             'date_start': '2017-01-01',
             'date_end': '2017-12-31',
             'type_id': cls.env.ref('account_fiscal_year.fiscalyear').id}
        )

        # Monthly Periods
        month_range_type = \
            cls.env.ref('sf_date_range.sf_date_range_type_month_sa')
        cls.env['account.config.settings'].create(
            {'budget_range_type_id': month_range_type.id})

        for month in range(1, 13):
            cls.env['date.range'].create(
                {'name': '%s/2017' % '%02d' % month,
                 'code': '%s2017' % '%02d' % month,
                 'company_id': cls.company_id,
                 'date_start': '2017-%s-01' % '%02d' % month,
                 'date_end': '2017-%s-%s' % (
                     '%02d' % month, calendar.monthrange(2017, month)[1]),
                 'type_id': month_range_type.id}
            )

    def test_store_and_load_budget_file(self):
        """Budget file is stored in tmp folder and loaded into a data frame."""
        # Store file in /tmp folder
        fpath = self.env['sf.account.budget.import']._store_data_file(
            self.name, self.data
        )

        # Load file into to a dataframe
        df = self.env['sf.account.budget.import']._read_budjet_from_csv(fpath)
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_import_create_budget(self):
        """We are able to import a budget file from scratch."""
        vals = {'name': self.name,
                'data': self.data,
                }

        self.env['sf.account.budget.import'].create(vals)

        self.assertEqual(
            self.env['sf.account.budget.line'].search_count([]), 72
        )

    def test_import_overwriting_budget_lines(self):
        """We are able re-import the same budget or with changes."""
        vals = {'name': self.name,
                'data': self.data,
                'company_id': self.company_id
                }
        # 1st importation
        self.env['sf.account.budget.import'].create(vals)
        # 2nd importation
        self.env['sf.account.budget.import'].create(vals)

        # 2nd importation overwrite the 1st one.
        self.assertEqual(
            self.env['sf.account.budget.line'].search_count([]), 72
        )
