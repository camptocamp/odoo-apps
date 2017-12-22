# -*- coding: utf-8 -*-
# Part of sensefly.

import anthem
from ..common import load_csv
from anthem.lyrics.records import add_xmlid
from odoo.exceptions import UserError

""" Post processing RMA

These songs will create the RMA erp business objects

"""

import logging
_logger = logging.getLogger(__name__)


@anthem.log
def settings(ctx):
    """ Configure rma settings """
    # RMA settings for main company (senseFly SA CH)
    ctx.env['rma.config.settings'].create(
        {'company_id': ctx.env.ref('base.main_company').id,
         'rma_service_service_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_consumable_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_stockable_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_additional_description': 'Original value:',
         'webhook_base_url': 'http://translator.sensefly.com',
         'rma_repair_location_id':
             ctx.env.ref('__setup__.stock_location_rma_sa').id,
         'rma_repair_line_src_location_id':
             ctx.env.ref('__setup__.stock_location_81').id,
         'rma_sale_line_route_id':
             ctx.env.ref('__setup__.stock_location_route_rma_sa').id
         }
    ).execute()

    # RMA settings for second company (senseFly Inc USA)
    ctx.env['rma.config.settings'].create(
        {'company_id': ctx.env.ref('__setup__.company_inc').id,
         'rma_service_service_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_consumable_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_stockable_product_id':
             ctx.env.ref('__setup__.product_template_521').id,
         'rma_service_additional_description': 'Original value:',
         'webhook_base_url': 'http://translator.sensefly.com',
         'rma_repair_location_id':
             ctx.env.ref('__setup__.stock_location_rma_inc').id,
         'rma_repair_line_src_location_id':
             ctx.env.ref('__setup__.stock_location_stock_inc').id,
         'rma_sale_line_route_id':
             ctx.env.ref('__setup__.stock_location_route_rma_inc').id
         }
    ).execute()


@anthem.log
def process_rma_draft(ctx, rma_data, repair_data):
    """Process waiting reception"""
    model = ctx.env['sf.rma'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, rma_data, model)
    rmas = ctx.env['sf.rma'].search([('state', '=', 'draft')])
    for rma in rmas:
        _logger.info("Processing " + rma.name)
        # Trigger action open
        rma.action_open()
        for repair in rma.repair_ids:
            repair.write({'name': rma.name})
            # Add repair order xml_id
            repair_xml_id = rma.get_xml_id()[rma.id].replace(
                'rma', 'mrp_repair')

            add_xmlid(ctx, repair, repair_xml_id)
    model_item = ctx.env['mrp.repair.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, repair_data, model_item)
    return rmas


@anthem.log
def process_rma_received(ctx, rma_data, repair_data):
    """Process received"""

    rmas = process_rma_draft(ctx, rma_data, repair_data)
    for rma in rmas:
        # Receive
        if rma.to_receive:
            for pick in rma.picking_ids:
                try:
                    pick.do_new_transfer()
                except UserError:
                    # Ignoring edge cases where SN was received twice
                    _logger.warning(
                        "%s Serial number already received." % rma.name
                    )
    return rmas


@anthem.log
def process_rma_under_repair(ctx, rma_data, repair_data):
    """Process under repair"""

    rmas = process_rma_received(ctx, rma_data, repair_data)
    for rma in rmas:
        # To under repair
        for repair in rma.repair_ids:
            if repair.invoicable_rma:
                # Repair to analyze
                repair.action_repair_to_analyze()
                # Repair to quotation
                repair.action_repair_to_quotation()

            repair.action_repair_to_repair()

        # Confirm Sale Order
        for sale in rma.sale_ids:
            # TODO Fixme
            # With lot id assigned, the route of the so line is not
            # used when we deliver the product.
            if sale.order_line:
                sale.order_line.lot_id = False

            rma.sale_ids.action_confirm()
    return rmas


@anthem.log
def process_rma_2binvoiced(ctx, rma_data, repair_data):
    """Process to be invoiced"""

    rmas = process_rma_received(ctx, rma_data, repair_data)
    for rma in rmas:
        rma.decision = 'to_invoice'

        for repair in rma.repair_ids:
            # Repair to analyze
            repair.action_repair_to_analyze()
            # Repair to quotation
            repair.action_repair_to_quotation()

        # Confirm Sale Order (payment term: before delivery)
        for sale in rma.sale_ids:
            if sale.order_line:
                sale.order_line.lot_id = False
            # Sensefly SA route
            if sale.company_id.id == ctx.env.ref('base.main_company').id:
                sale.order_line.route_id = ctx.env.ref(
                    '__setup__.stock_location_route_rma_sa').id

            sale.payment_term_id = ctx.env.ref(
                '__setup__.account_payment_term_11').id

            # Confirm Order
            sale.action_confirm()
    return rmas


@anthem.log
def process_rma_done_undelivered(ctx, rma_data, repair_data):
    """Process repaired not delivered"""
    rmas = process_rma_received(ctx, rma_data, repair_data)
    for rma in rmas:
        for repair in rma.repair_ids:
            repair.write({'state': 'done'})
        for sale in rma.sale_ids:
            if sale.order_line:
                sale.order_line.lot_id = False

            # Apply route for Sensefly SA
            if sale.company_id.id == ctx.env.ref('base.main_company').id:
                if sale.order_line:
                    sale.order_line.route_id = ctx.env.ref(
                        '__setup__.stock_location_route_rma_sa').id

            # Import repair lines
            wizard = ctx.env['sale.order.repair.lines.import'].with_context(
                active_id=sale.id
            ).create(
                {'rma_id': rma.id,
                 'sale_order_id': sale.id,
                 'repair_line_ids': [
                     (6, 0, rma.repair_ids.mapped('operations').ids)]
                 })
            wizard.import_lines()

            # Confirm Order
            sale.action_confirm()


@anthem.log
def process_rma_done_delivered(ctx, rma_data, repair_data):
    """Process repaired delivered"""
    rmas = process_rma_draft(ctx, rma_data, repair_data)
    for rma in rmas:
        for repair in rma.repair_ids:
            repair.state = 'done'
        rma.state = 'closed'
