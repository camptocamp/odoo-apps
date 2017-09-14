# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _
from odoo.exceptions import MissingError


class SfSalesForecast(models.Model):
    _name = "sf.sales.forecast"
    _description = "Dealers sales forecast"

    name = fields.Char(
        string='Forecast Number', required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code(
            'sf.sales.forecast'))
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    product_ids = fields.Many2many(
        'product.product', string='Products')
    fiscal_year_id = fields.Many2one(
        'date.range',
        string='Fiscal Year',
        domain=[('type_id.fiscal_year', '=', True)],
        required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id
    )
    user_id = fields.Many2one('res.users', string='Responsible')
    forecast_line_ids = fields.One2many(
        'sf.sales.forecast.line', 'forecast_id', string='Lines')

    _sql_constraints = [('uniq_forecast',
                         'unique(company_id, partner_id, fiscal_year_id)',
                         _("Forecast must be unique by company partner and "
                           "fiscal year!"))]

    @api.multi
    def generate_forecast_lines(self):
        # Period range type
        period_range_type = \
            self.env['sale.config.settings']\
                .default_sale_forecast_range_type_id()
        if not period_range_type:
            raise MissingError(_('Sale forecast range type!: Please configure'
                                 ' it in Sales Configuration.'))

        # Periods os this fiscal year
        period_ids = self.env['date.range'].search(
            [('date_start', '>=', self.fiscal_year_id.date_start),
             ('date_end', '<=', self.fiscal_year_id.date_end),
             ('type_id', '=', period_range_type.id)])

        if not period_ids:
            raise MissingError(_('No periods defined!: At least one period is'
                                 ' extected to be configured in this'
                                 ' fiscal year!'))

        # Check lines already generated per product
        for product in self.product_ids:
            # Already exists skip it!
            if product in self.forecast_line_ids.mapped('product_id'):
                continue
            # Create lines
            for period_id in period_ids:
                self.write(
                    {'forecast_line_ids': [
                        (0, 0, {
                            'product_id': product.id,
                            'period_id': period_id.id
                            }
                         )]})

        lines2delete = self.forecast_line_ids.filtered(
            lambda line: line.product_id not in self.product_ids
        )
        lines2delete.unlink()


class SalesForecastLine(models.Model):
    _name = "sf.sales.forecast.line"
    _description = "Sales forecast line"

    forecast_id = fields.Many2one(
        'sf.sales.forecast', string='Forecast', ondelete='cascade')
    fiscal_year_id = fields.Many2one(
        string='Fiscal Year', related='forecast_id.fiscal_year_id')
    partner_id = fields.Many2one(
        string='Partner', related='forecast_id.partner_id')
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    period_id = fields.Many2one(
        'date.range', string='Period', required=True)
    updated_forecast = fields.Integer(
        string='Updated Forecast', default=0, required=True)
