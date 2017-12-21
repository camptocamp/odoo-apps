# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
import csv
from anthem.lyrics.records import add_xmlid, create_or_update
from ..common import load_csv
from pkg_resources import Requirement, resource_stream
from datetime import date
from odoo import fields


""" Data loaded in all modes
The data loaded here will be loaded in the 'demo' and
'full' modes.
"""


req = Requirement.parse('sensefly-odoo')


@anthem.log
def create_date_range(ctx):
    """ Create date.ranges (periods) for 2017 from csv """
    load_csv(ctx, 'data/install/date_range.csv',
             'date.range')


@anthem.log
def create_analytic_dimension(ctx):
    """ Creating Analytic Dimension tag  """
    create_or_update(ctx, 'account.analytic.dimension',
                     '__setup__.account_analytic_dimension_team',
                     {'name': 'Team', 'code': 'T'})


@anthem.log
def import_analytic_tag(ctx):
    """ Importing Analytic tag (team) from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/analytic_tag.csv',
             'account.analytic.tag')


@anthem.log
def import_analytic_account_project(ctx):
    """ Importing analytic account (project) from csv """
    model = ctx.env['account.analytic.account'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx,
             's3://prod-sf-odoo-data/install/analytic_account_project.csv',
             model)


@anthem.log
def import_partner_entity(ctx):
    """ Importing partner entity from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/partner_entity.csv',
             'res.partner.entity.type')


@anthem.log
def import_product_category(ctx):
    """ Importing product category from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/product_category.csv',
             'product.category')


@anthem.log
def import_inventory_category(ctx):
    """ Importing inventory category from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/inventory_category.csv',
             'sf.inventory.category')


@anthem.log
def import_unit_measure(ctx):
    """ Importing unit measure from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/unitmeasure.csv',
             'product.uom')


@anthem.log
def import_account_tag_pl_name(ctx):
    """ Importing account tag (PL name)  from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/account_tag_pl.csv',
             'account.account.tag')


@anthem.log
def import_account_tag_parrot_category(ctx):
    """ Importing account tag (parrot category) from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/account_tag_parrot.csv',
             'account.account.tag')


@anthem.log
def import_account_fiscal_position(ctx):
    """ Importing account fiscal postition from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/fiscal_position.csv',
             'account.fiscal.position')
    load_csv(ctx, 's3://prod-sf-odoo-data/install/fiscal_position_tax.csv',
             'account.fiscal.position.tax')


@anthem.log
def delete_account(ctx):
    """ Delete standard chart of accounts from csv """
    # Read the CSV
    content = resource_stream(req, 'data/install/account_delete.csv')

    # Create list of dictionnaries
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(content, skipinitialspace=True)
        ]

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'], raise_if_not_found=False)
        if rec:
            rec.unlink()


@anthem.log
def import_account_account(ctx):
    """ Importing chart of accounts from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/account.csv',
             'account.account')


@anthem.log
def add_xmlid_account_journal(ctx):
    """ Add xml ID to journals"""
    journals = ctx.env['account.journal'].search([])

    for journal in journals:
        add_xmlid(
            ctx, journal,
            'scenario.account_journal_' + journal.code,
            noupdate=True
        )


@anthem.log
def delete_account_journal(ctx):
    """ Delete standard journals from csv """
    # Read the CSV
    content = resource_stream(req, 'data/install/journal_delete.csv')

    # Create list of dictionnaries
    records = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(content, skipinitialspace=True)
        ]

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'], raise_if_not_found=False)
        if rec:
            rec.unlink()


@anthem.log
def import_account_journal(ctx):
    """ Importing journals from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/journal.csv',
             'account.journal')


@anthem.log
def import_email_template(ctx):
    """ Importing email template from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/email_template.csv',
             'mail.template')


@anthem.log
def update_picking_type(ctx):
    """ Update stock picking type. Only for sensefly SA """
    for record in ctx.env['stock.picking.type'].search(
            [('name', 'in', ('Pick', 'Reserve & Pack')),
             ('warehouse_id', '=', ctx.env.ref('stock.warehouse0').id),
             ('active', '=', False)]):
        record.name = 'Reserve & Pack'
        record.active = True
        add_xmlid(
            ctx, record,
            '__setup__.stock_pick_type_reserve_pack',
            noupdate=True
        )
    for record in ctx.env['stock.picking.type'].search(
            [('name', 'in', ('Pack', 'Freight Labeling')),
             ('warehouse_id', '=', ctx.env.ref('stock.warehouse0').id),
             ('active', '=', False)]):
        record.name = 'Freight Labeling'
        record.active = True
        record.propagate_delivery_info = True
        add_xmlid(
            ctx, record,
            '__setup__.stock_pick_type_freight_labeling',
            noupdate=True
        )


@anthem.log
def update_procurement_rule(ctx):
    """ Update procurement rule names """
    for record in ctx.env['procurement.rule'].search(
            [('name', '=', 'WH: Stock -> Packing Zone')]):
        if record.warehouse_id.company_id.id == ctx.env.ref(
                'base.main_company').id:
            record.delay = 1
            add_xmlid(ctx, record,
                      '__setup__.procurement_rule_stock_packs_sa',
                      noupdate=False)

    for record in ctx.env['procurement.rule'].search(
            [('name', 'in', ('WH: Packing Zone -> Output',
                             'WH: Packs -> Pickup'))]):
        record.name = 'WH: Packs -> Pickup'
        if record.warehouse_id.company_id.id == ctx.env.ref(
                'base.main_company').id:
            add_xmlid(ctx, record,
                      '__setup__.procurement_rule_packs_pickup_sa',
                      noupdate=False)

    for record in ctx.env['procurement.rule'].search(
            [('name', 'in', ('WH: Output -> Customers',
                             'WH: Pickup -> Customers'))]):
        record.name = 'WH: Pickup -> Customers'
        if record.warehouse_id.company_id.id == ctx.env.ref(
                'base.main_company').id:
            add_xmlid(ctx, record,
                      '__setup__.procurement_rule_pickup_customers_sa',
                      noupdate=False)


@anthem.log
def update_stock_location(ctx):
    """ Update stock location names """
    create_or_update(ctx, 'stock.location',
                     'stock.location_pack_zone',
                     {'name': 'Packs'})
    create_or_update(ctx, 'stock.location',
                     'stock.stock_location_output',
                     {'name': 'Pickup'})


@anthem.log
def delete_payment_term(ctx):
    """ Delete payment terms standard """
    # Create list of dictionnaries
    records = [
        'account.account_payment_term_15days',
        'account.account_payment_term_net',
        'account.account_payment_term_immediate'
        ]

    # Delete data
    for record in records:
        rec = ctx.env.ref(record, raise_if_not_found=False)
        if rec:
            rec.unlink()


@anthem.log
def import_payment_term(ctx):
    """ Importing payment terms from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/payment_term.csv',
             'account.payment.term')
    load_csv(ctx, 's3://prod-sf-odoo-data/install/payment_term_line.csv',
             'account.payment.term.line')


@anthem.log
def delete_layout_category(ctx):
    """ Delete layout categories """
    record = ctx.env.ref('sale.sale_layout_cat_1', raise_if_not_found=False)
    if record:
        record.unlink()
    record = ctx.env.ref('sale.sale_layout_cat_2', raise_if_not_found=False)
    if record:
        record.unlink()


@anthem.log
def create_layout_category(ctx):
    """ Creating layout categories  """
    create_or_update(ctx, 'sale.layout_category',
                     '__setup__.layout_category_new_material',
                     {'name': 'List of new material',
                      'subtotal': True,
                      'sequence': 10})
    create_or_update(ctx, 'sale.layout_category',
                     '__setup__.layout_category_repair_labor',
                     {'name': 'Repair labour',
                      'subtotal': True,
                      'sequence': 20})


@anthem.log
def import_sequence(ctx):
    """ Importing Sequences from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/sequence.csv',
             'ir.sequence')


def import_account_asset_category(ctx):
    """ Importing account asset category from csv """
    load_csv(
        ctx,
        's3://prod-sf-odoo-data/install/account_asset_category.csv',
        'account.asset.category'
    )


@anthem.log
def desactive_incoterm(ctx):
    """ Desactive Incoterm from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/incoterm.csv',
             'stock.incoterms')


@anthem.log
def import_price_category(ctx):
    """ Importing price category from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/price_category.csv',
             'product.price.category')


@anthem.log
def create_rate_auto_download(ctx):
    """ Creating currency rate download configuration"""
    create_or_update(ctx, 'currency.rate.update.service',
                     '__setup__.rate_auto_download_sa',
                     {'service': 'CH_ADMIN',
                      'interval_type': 'months',
                      'interval_number': 1,
                      'next_run': fields.Date.to_string(
                          date.today().replace(day=1)
                      ),
                      'currency_to_update': [(6, 0,
                                              [ctx.env.ref('base.CHF').id,
                                               ctx.env.ref('base.USD').id,
                                               ctx.env.ref('base.EUR').id]
                                              )]})
    record = ctx.env.ref('__setup__.rate_auto_download_sa')
    record.refresh_currency()


@anthem.log
def create_rma_route(ctx):
    """Creating rma route"""

    # Add xml_id on stock location RMA
    location_rma_sa = ctx.env['stock.location'].search(
        [('name', '=', 'RMA'),
         ('company_id', '=', ctx.env.ref('base.main_company').id)])
    add_xmlid(
        ctx, location_rma_sa,
        '__setup__.stock_location_rma_sa',
        noupdate=True)
    location_rma_inc = ctx.env['stock.location'].search(
        [('name', '=', 'RMA'),
         ('company_id', '=', ctx.env.ref('__setup__.company_inc').id)])
    add_xmlid(
        ctx, location_rma_inc,
        '__setup__.stock_location_rma_inc',
        noupdate=True)

    # RMA procurement rules
    create_or_update(ctx, 'procurement.rule',
                     '__setup__.procurement_rule_rma_packs_sa',
                     {
                         'name': 'RMA -> Packs',
                         'action': 'move',
                         'location_id':
                             ctx.env.ref('stock.location_pack_zone').id,
                         'location_src_id': location_rma_sa.id,
                         'warehouse_id': ctx.env.ref('stock.warehouse0').id,
                         'procure_method': 'make_to_order',
                         'picking_type_id': ctx.env.ref(
                             '__setup__.stock_pick_type_reserve_pack').id
                     })

    create_or_update(ctx, 'procurement.rule',
                     '__setup__.procurement_rule_rma_packs_pickup_sa',
                     {
                         'name': 'WH: Packs -> Pickup',
                         'action': 'move',
                         'location_id':
                             ctx.env.ref('stock.stock_location_output').id,
                         'location_src_id':
                             ctx.env.ref('stock.location_pack_zone').id,
                         'warehouse_id': ctx.env.ref('stock.warehouse0').id,
                         'procure_method': 'make_to_order',
                         'picking_type_id': ctx.env.ref(
                             '__setup__.stock_pick_type_freight_labeling').id
                     })

    create_or_update(ctx, 'procurement.rule',
                     '__setup__.procurement_rule_rma_pickup_customers_sa',
                     {
                         'name': 'WH: Pickup -> Customers',
                         'action': 'move',
                         'location_id':
                             ctx.env.ref('stock.stock_location_customers').id,
                         'location_src_id':
                             ctx.env.ref('stock.stock_location_output').id,
                         'warehouse_id': ctx.env.ref('stock.warehouse0').id,
                         'procure_method': 'make_to_order',
                         'picking_type_id': ctx.env.ref(
                             'stock.picking_type_out').id
                     })

    # RMA route
    create_or_update(ctx, 'stock.location.route',
                     '__setup__.stock_location_route_rma_sa',
                     {'company_id': ctx.env.ref('base.main_company').id,
                      'name': 'senseFly SA: RMA Pick + Pack + Ship',
                      'warehouse_ids': [
                          (4, ctx.env.ref('stock.warehouse0').id)
                      ],
                      'sale_selectable': True,
                      'sequence': 20,
                      'pull_ids': [
                          (4, ctx.env.ref(
                              '__setup__.procurement_rule_rma_packs_sa')
                           .id),
                          (4, ctx.env.ref(
                              '__setup__.procurement_rule_rma_packs_pickup_sa')
                           .id),
                          (4, ctx.env.ref(
                              '__setup__.'
                              'procurement_rule_rma_pickup_customers_sa').id)
                      ]
                      })


@anthem.log
def import_delivery_methode(ctx):
    """ Importing delivery methode from csv """
    load_csv(ctx, 's3://prod-sf-odoo-data/install/delivery_methode.csv',
             'delivery.carrier')


@anthem.log
def main(ctx):
    """ Loading data """
    create_analytic_dimension(ctx)
    import_analytic_tag(ctx)
    import_analytic_account_project(ctx)
    import_partner_entity(ctx)
    import_product_category(ctx)
    import_inventory_category(ctx)
    import_unit_measure(ctx)
    import_account_tag_pl_name(ctx)
    import_account_tag_parrot_category(ctx)
    import_account_fiscal_position(ctx)
    delete_account(ctx)
    import_account_account(ctx)
    import_sequence(ctx)
    add_xmlid_account_journal(ctx)
    delete_account_journal(ctx)
    import_account_journal(ctx)
    create_date_range(ctx)
    import_email_template(ctx)
    update_picking_type(ctx)
    update_procurement_rule(ctx)
    update_stock_location(ctx)
    delete_payment_term(ctx)
    import_payment_term(ctx)
    delete_layout_category(ctx)
    create_layout_category(ctx)
    import_account_asset_category(ctx)
    desactive_incoterm(ctx)
    import_price_category(ctx)
    create_rate_auto_download(ctx)
    create_rma_route(ctx)
    import_delivery_methode(ctx)
