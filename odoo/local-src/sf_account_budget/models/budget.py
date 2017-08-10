# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class AccountBudget(models.Model):
    _name = "sf.account.budget"
    _description = "Budget and Estimation"

    name = fields.Char(
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code(
            'sf.account.budget'))
    account_id = fields.Many2one(
        'account.account', string='Account', required=True)
    fiscal_year_id = fields.Many2one(
        'date.range', string='Fiscal Year')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'sf.account.budget'))
    budget_line_ids = fields.One2many(
        'sf.account.budget.line', 'budget_id', string='Budget Lines'
    )
    active = fields.Boolean(default=True)


class AccountBudgetLine(models.Model):
    _name = "sf.account.budget.line"

    budget_id = fields.Many2one(
        'sf.account.budget', string='Account Budget', ondelete='cascade',
        required=True)
    tag_id = fields.Many2one(
        'account.analytic.tag', string='Team', required=True
    )
    fiscal_year_id = fields.Many2one(
        'date.range', related='budget_id.fiscal_year_id'
    )
    period_id = fields.Many2one(
        'date.range', string='Period', required=True
    )
    company_id = fields.Many2one(
        related='budget_id.company_id', readonly=True,
        string='Company')
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')
    period_budget = fields.Monetary(
        'Budget', currency_field='company_currency_id', default=0.0)
    e1 = fields.Monetary(
        'E1', currency_field='company_currency_id', default=0.0)
    e2 = fields.Monetary(
        'E2', currency_field='company_currency_id', default=0.0)
    e3 = fields.Monetary(
        'E3', currency_field='company_currency_id', default=0.0)
    e4 = fields.Monetary(
        'E4', currency_field='company_currency_id', default=0.0)
    e5 = fields.Monetary(
        'E5', currency_field='company_currency_id', default=0.0)
    e6 = fields.Monetary(
        'E6', currency_field='company_currency_id', default=0.0)
    e7 = fields.Monetary(
        'E7', currency_field='company_currency_id', default=0.0)
    e8 = fields.Monetary(
        'E8', currency_field='company_currency_id', default=0.0)
    e9 = fields.Monetary(
        'E9', currency_field='company_currency_id', default=0.0)
    e10 = fields.Monetary(
        'E10', currency_field='company_currency_id', default=0.0)
    e11 = fields.Monetary(
        'E11', currency_field='company_currency_id', default=0.0)
    e12 = fields.Monetary(
        'E12', currency_field='company_currency_id', default=0.0)
    active = fields.Boolean(default=True)
