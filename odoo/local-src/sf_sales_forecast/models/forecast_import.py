# -*- coding: utf-8 -*-
# Part of sensefly.
from odoo import fields, models, api
from odoo.exceptions import MissingError, UserError
from odoo import _
import calendar
import math
import base64
import os
import chardet
import pandas as pd


class SalesForecastImport(models.Model):
    _name = "sf.sales.forecast.import"
    _description = "Import Sales Forecast"

    name = fields.Char(required=True)
    data = fields.Binary('File', attachment=True)
    date = fields.Datetime('Date', default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        fpath = self._store_data_file(vals['name'], vals['data'])
        df = self._read_forecast_from_csv(fpath)
        data = df.transpose().to_dict()

        company_id = self.env['res.company']._company_default_get(
            'sf.sales.forecast.import').id

        loaded_rows = []
        for index, row in data.iteritems():
            # Partner / Dealer
            partner_name = row['Dealer']
            partner_id = self._get_partner_id(partner_name, company_id)

            # Product
            product_code = row['Product Ref']
            product_id = self._get_product_id(product_code)
            if not product_id:
                raise MissingError(
                    _("Product not found!: Row %s, Code %s") %
                    (index, product_code))

            # Check pair (Partner, Product) already loaded
            if (partner_id, product_id) in loaded_rows:
                raise UserError(
                    _("Duplicated line!: Row %s, (%s, %s)") %
                    (index, partner_name, product_code))

            # Fiscal year
            fiscal_year = row['Fiscal Year']
            fiscal_year_id = self._get_fiscal_year_id(fiscal_year, company_id)
            if not fiscal_year_id:
                raise MissingError(
                    _("Fiscal year not found!: Row %s, Fiscal Year %s") %
                    (index, fiscal_year,))

            # Sales Forecast
            sales_forecast = self._get_sales_forecast(
                company_id, partner_id, fiscal_year_id)

            if not sales_forecast:
                forecast_vals = {'partner_id': partner_id,
                                 'fiscal_year_id': fiscal_year_id,
                                 'product_ids': [(4, product_id)]
                                 }
                sales_forecast = self.env['sf.sales.forecast'].create(
                    forecast_vals)
            else:
                # Add product to this forecast
                if product_id not in sales_forecast.product_ids.ids:
                    sales_forecast.write({'product_ids': [(4, product_id)]})

            # Period range type
            period_range_type = self.env['sale.config.settings']. \
                default_sale_forecast_range_type_id()
            if not period_range_type:
                raise MissingError(
                    _("Default period range type not configured!"))

            # Forecast Lines
            for month_number in range(1, 13):
                # We assume that period code follow the pattern MMYYYY=082017
                period_code = str(month_number).zfill(2) + str(fiscal_year)
                period_id = self._get_period_id(
                    period_code, company_id, period_range_type)

                if not period_id:
                    raise MissingError(
                        _("Accounting Period code not found!: "
                          "Period %s, range type %s") %
                        (period_code, period_range_type))

                forecast_line = self._get_sales_forecast_line(
                    sales_forecast.id, product_id, period_id)

                # Validate forecast value
                forecast_val = row[calendar.month_abbr[month_number]]
                if not isinstance(forecast_val, (int, float)) or \
                        math.isnan(forecast_val):
                    raise MissingError(
                        _("Forecast value must be a number >= 0!: Row %s")
                        % index)

                # Create forecast line
                if not forecast_line:
                    sales_forecast.write(
                        {
                            'forecast_line_ids': [
                                (0, 0, {'product_id': product_id,
                                        'period_id': period_id,
                                        'updated_forecast': forecast_val}
                                 )]
                         }
                    )

                # Write forecast line value
                else:
                    forecast_line.write(
                        {'updated_forecast': forecast_val}
                    )

                loaded_rows += [(partner_id, product_id)]

        return super(SalesForecastImport, self).create(vals)

    @api.model
    def _store_data_file(self, file_name, data, path='/tmp/'):
        """Stores binary data in a csv file."""
        data = base64.decodestring(data)
        full_file_path = os.path.join(path, file_name)
        with open(full_file_path, 'wb') as fp:
            fp.write(data)
        return full_file_path

    @api.model
    def _read_forecast_from_csv(self, file_path):
        """
        Read forecast from csv file into a dataframe
        """
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())

        df = pd.read_csv(file_path, delimiter=';',
                         encoding=result['encoding'])
        return df

    @api.model
    def _get_partner_id(self, partner_name, company_id):
        partners = self.env['res.partner'].search(
            [('name', '=', partner_name),
             ('company_id', '=', company_id)])
        if not partners:
            raise MissingError(
                _("Partner not found!: Partner %s") % partner_name)
        elif len(partners) > 1:
            raise UserError(
                _("Found duplicated partners in the system!: "
                  "Found %s partners with name %s")
                % (len(partners), partner_name))
        else:
            return partners[0].id

    @api.model
    def _get_product_id(self, product_code):
        products = self.env['product.product'].search(
            [('default_code', '=', product_code)])
        if len(products) != 1:
            return None
        return products[0].id

    @api.model
    def _get_fiscal_year_id(self, year, company_id):
        fiscal_years = self.env['date.range'].search(
            [('code', '=', str(year)),
             ('type_id', '=', self.env.ref(
                 'account_fiscal_year.fiscalyear').id),
             ('company_id', '=', company_id)])
        if len(fiscal_years) != 1:
            return None
        return fiscal_years[0].id

    @api.model
    def _get_sales_forecast(self, company_id, partner_id, fiscal_year_id):
        sales_forecast = self.env['sf.sales.forecast'].search(
            [('company_id', '=', company_id),
             ('partner_id', '=', partner_id),
             ('fiscal_year_id', '=', fiscal_year_id)])
        if len(sales_forecast) != 1:
            return None
        return sales_forecast[0]

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
    def _get_sales_forecast_line(
            self, sales_forecast_id, product_id, period_id):
        forecast_lines = self.env['sf.sales.forecast.line'].search(
            [('forecast_id', '=', sales_forecast_id),
             ('product_id', '=', product_id),
             ('period_id', '=', period_id)]
        )
        if len(forecast_lines) != 1:
            return None
        return forecast_lines[0]
