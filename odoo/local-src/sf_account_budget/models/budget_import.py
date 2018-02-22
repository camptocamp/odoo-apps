# -*- coding: utf-8 -*-
# Part of sensefly.
from odoo import fields, models, api
from odoo.exceptions import MissingError
from odoo import _
import math
import base64
import os
import chardet
import pandas as pd

TEMPLATE_MAP = {'account_code': 0,
                'team': 2,
                'budget_type': 3,
                'fiscal_year': 4,
                'periods': {'01': 5,
                            '02': 6,
                            '03': 7,
                            '04': 8,
                            '05': 9,
                            '06': 10,
                            '07': 11,
                            '08': 12,
                            '09': 13,
                            '10': 14,
                            '11': 15,
                            '12': 16}
                }

BUDGET_TYPE_MAP = {'BU': 'period_budget',
                   'E1': 'e1',
                   'E2': 'e2',
                   'E3': 'e3',
                   'E4': 'e4',
                   'E5': 'e5',
                   'E6': 'e6',
                   'E7': 'e7',
                   'E8': 'e8',
                   'E9': 'e9',
                   'E10': 'e10',
                   'E11': 'e11',
                   'E12': 'e12',
                   }


class AccountBudgetImport(models.Model):
    _name = "sf.account.budget.import"
    _description = "Import Budget"

    name = fields.Char(required=True)
    data = fields.Binary('File', attachment=True)
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())

    @api.model
    def create(self, vals):
        fpath = self._store_data_file(vals['name'], vals['data'])
        df = self._read_budjet_from_csv(fpath)

        company_id = self.env['res.company']._company_default_get(
            'sf.account.budget_import').id

        for index, row in df.iterrows():
            # Account
            account_code = row[TEMPLATE_MAP['account_code']]
            account_id = self._get_account_id(account_code, company_id)
            if not account_id:
                raise MissingError(
                    _("Account not found!: Row %s, Account Code %s") %
                    (index, account_code))

            # Fiscal Year
            fiscal_year = row[TEMPLATE_MAP['fiscal_year']]
            fiscal_year_id = self._get_fiscal_year_id(fiscal_year, company_id)
            if not fiscal_year_id:
                raise MissingError(
                    _("Fiscal year not found!: Row %s, Fiscal Year %s") %
                    (index, fiscal_year,))

            # Team
            team = row[TEMPLATE_MAP['team']]
            tag_id = self._get_team_analytic_tag_id(team)
            if not tag_id:
                raise MissingError(
                    _("Team not found!: Row %s, Team %s") %
                    (index, team))

            # Account Budget
            account_budget = self._get_account_budget(
                company_id, account_id, fiscal_year_id)

            if not account_budget:
                account_budget_vals = {'account_id': account_id,
                                       'fiscal_year_id': fiscal_year_id,
                                       'company_id': company_id,
                                       'active': True}
                account_budget = self.env['sf.account.budget'].create(
                    account_budget_vals)

            # Period range type
            period_range_type = self.env['account.config.settings'].\
                default_budget_range_type()
            if not period_range_type:
                raise MissingError(
                    _("Default period range type not configured!"))

            # Account Budget Line
            for period in TEMPLATE_MAP['periods']:
                # We assume that period code follow the rule MMYYYY=082017
                period_code = period + str(fiscal_year)
                period_id = self._get_period_id(
                    period_code, company_id, period_range_type)

                if not period_id:
                    raise MissingError(
                        _("Accounting Period code not found!: "
                          "Period %s, range type %s") %
                        (period_code, period_range_type))

                budget_line = self._get_account_budget_line(
                    account_budget.id, tag_id, period_id)

                budget_type = row[TEMPLATE_MAP['budget_type']]
                if not budget_type \
                        or budget_type not in BUDGET_TYPE_MAP.keys():
                    raise MissingError(
                        _("Budget type not valid!: Row %s, Budget type %s") %
                        (index, budget_type))

                if not budget_line:
                    self.with_context(index=index).create_budget_line(
                        account_budget.id, budget_type, period_id, period,
                        tag_id, row)
                else:
                    self.with_context(index=index).write_budget_line(
                        budget_line, budget_type, period, row)

        return super(AccountBudgetImport, self).create(vals)

    @api.model
    def create_budget_line(self, account_budget_id, budget_type,
                           period_id, period, tag_id, row):
        vals = {'budget_id': account_budget_id,
                'tag_id': tag_id,
                'period_id': period_id,
                'active': True
                }
        budget_val = row[TEMPLATE_MAP['periods'][period]]
        if not isinstance(budget_val, (int, float)) or math.isnan(budget_val):
            raise MissingError(
                _("Budget value must be a number >= 0!: Row %s") %
                self.env.context.get('index', False))

        vals[BUDGET_TYPE_MAP[budget_type]] = budget_val

        res = self.env['sf.account.budget.line'].create(vals)
        return res

    def write_budget_line(self, budget_line, budget_type, period, row):
        budget_val = row[TEMPLATE_MAP['periods'][period]]
        if not isinstance(budget_val, (int, float)) or math.isnan(budget_val):
            raise MissingError(
                _("Budget value must be a number >= 0!: Row %s") %
                self.env.context.get('index', False))

        vals = {BUDGET_TYPE_MAP[budget_type]: budget_val}
        return budget_line.write(vals)

    @api.model
    def _get_account_id(self, account_code, company_id):
        accounts = self.env['account.account'].search(
            [('code', '=', account_code),
             ('company_id', '=', company_id)])
        if len(accounts) != 1:
            return None
        return accounts[0].id

    @api.model
    def _get_fiscal_year_id(self, year, company_id):
        fiscal_years = self.env['date.range'].search(
            [('name', '=', str(year)),
             ('type_id', '=', self.env.ref(
                 'account_fiscal_year.fiscalyear').id),
             ('company_id', '=', company_id)])
        if len(fiscal_years) != 1:
            return None
        return fiscal_years[0].id

    @api.model
    def _get_period_id(self, period_code, company_id, range_type):
        periods = self.env['date.range'].search(
            [('company_id', '=', company_id),
             ('code', '=', period_code),
             ('type_id', '=', range_type.id)])
        if len(periods) == 1:
            return periods[0].id
        return None

    @api.model
    def _get_team_analytic_tag_id(self, team_code):
        tags = None
        tag_dimensions = self.env['account.analytic.dimension'].search(
            [('code', '=', 'T')])
        if tag_dimensions and len(tag_dimensions) == 1:
            tags = self.env['account.analytic.tag'].search(
                [('code', '=', team_code),
                 ('analytic_dimension_id', '=', tag_dimensions.id)])
            if len(tags) == 1:
                return tags[0].id
        return tags

    @api.model
    def _get_account_budget(self, company_id, account_id, fiscal_year_id):
        account_budget = self.env['sf.account.budget'].search(
            [('company_id', '=', company_id),
             ('account_id', '=', account_id),
             ('fiscal_year_id', '=', fiscal_year_id)])
        if len(account_budget) != 1:
            return None
        return account_budget[0]

    @api.model
    def _get_account_budget_line(self, account_budget_id, tag_id, period_id):
        account_budget_lines = self.env['sf.account.budget.line'].search(
            [('budget_id', '=', account_budget_id),
             ('tag_id', '=', tag_id),
             ('period_id', '=', period_id)])

        if len(account_budget_lines) != 1:
            return None
        return account_budget_lines[0]

    @api.model
    def _store_data_file(self, file_name, data, path='/tmp/'):
        """Stores binary data in a csv file."""
        data = base64.decodestring(data)
        full_file_path = os.path.join(path, file_name)
        fp = open(full_file_path, 'wb')
        fp.write(data)
        fp.close()
        return full_file_path

    @api.model
    def _read_budjet_from_csv(self, file_path):
        """
        Read a csv file into a dataframe
        """
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())

        df = pd.read_csv(file_path, delimiter=';', encoding=result['encoding'])
        return df
