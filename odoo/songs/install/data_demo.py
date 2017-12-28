# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem
from . import rma
import csv
from ..common import load_csv, req, get_content


""" File for demo data

These songs will be called when the mode is 'demo', we should import only
excerpt of data, while the full data is only imported in the 'full' mode.

"""


@anthem.log
def import_users(ctx):
    """ Importing users from csv """
    model = ctx.env['res.users'].with_context({
        'no_reset_password': True,
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/users.csv', model)


@anthem.log
def import_users_groups(ctx):
    """ Importing groups to users from csv """
    load_csv(ctx, 'data/demo/users_group.csv', 'res.users')


@anthem.log
def import_country_state(ctx):
    """ Importing country states from csv """
    load_csv(ctx, 'data/demo/country_state.csv', 'res.country.state')


@anthem.log
def import_countries(ctx):
    """ Importing countries from csv """
    load_csv(ctx, 'data/demo/country.csv', 'res.country')


@anthem.log
def import_crm_team(ctx):
    """ Importing sales team / channel from csv """
    model = ctx.env['crm.team'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/crm_team.csv', model)


@anthem.log
def import_location(ctx):
    """ Importing stock location from csv """
    load_csv(ctx, 'data/demo/stock_location.csv', 'stock.location')


@anthem.log
def import_customers(ctx):
    """ Importing customers from csv """
    model = ctx.env['res.partner'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/customers.csv', model)


@anthem.log
def import_customers_properties_account(ctx):
    """ Importing customers properties account from csv """
    model = ctx.env['ir.property'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/customers_proper_a.csv', model)

    # Change XMLID to database id
    # Read the CSV
    content = get_content(req, 'data/demo/customers_proper_a.csv')

    # Create list of dictionnaries
    records = list(csv.DictReader(content, skipinitialspace=True))

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'])
        if rec:
                # Customers / source
                cust_tmp = ctx.env.ref(rec.res_id,
                                       raise_if_not_found=False)
                if not cust_tmp:
                    continue
                rec.res_id = cust_tmp._name + "," + str(cust_tmp.id)
                # Account / destination
                account_tmp = ctx.env.ref(rec.value_reference,
                                          raise_if_not_found=False)
                if account_tmp:
                    rec.value_reference = account_tmp._name + "," + str(
                        account_tmp.id)
                else:
                    ctx.log_line(str(rec.res_id) + ":" + rec.value_reference)
                    rec.unlink()


@anthem.log
def import_customers_properties_payterm(ctx):
    """ Importing customers properties payment terms from csv """
    model = ctx.env['ir.property'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/customers_proper_p.csv', model)

    # Change XMLID to database id
    # Read the CSV
    content = get_content(req, 'data/demo/customers_proper_p.csv')

    # Create list of dictionnaries
    records = list(csv.DictReader(content, skipinitialspace=True))

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'])
        if rec:
            # Customer / source
            cust_tmp = ctx.env.ref(rec.res_id,
                                   raise_if_not_found=False)
            if not cust_tmp:
                continue
            rec.res_id = cust_tmp._name + "," + str(cust_tmp.id)
            # Payment term / destination
            payterm_tmp = ctx.env.ref(rec.value_reference,
                                      raise_if_not_found=False)
            if payterm_tmp:
                rec.value_reference = payterm_tmp._name + "," + str(
                    payterm_tmp.id)
            else:
                ctx.log_line(str(rec.res_id) + ":" + rec.value_reference)
                rec.unlink()


@anthem.log
def import_suppliers(ctx):
    """ Importing suppliers from csv """
    model = ctx.env['res.partner'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/suppliers.csv', model)


@anthem.log
def import_drone_type(ctx):
    """ Importing drone type from csv """
    load_csv(ctx, 'data/demo/drone_type.csv', 'drone.type')


@anthem.log
def import_product(ctx):
    """ Importing products from csv """
    model = ctx.env['product.template'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/product.csv', model)


@anthem.log
def import_product_account(ctx):
    """ Importing products accounts from csv """
    model = ctx.env['ir.property'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/product_account.csv', model)

    # Change XMLID to database id
    # Read the CSV
    content = get_content(req, "data/demo/product_account.csv")

    # Create list of dictionnaries
    records = list(csv.DictReader(content, skipinitialspace=True))

    # Delete data
    for record in records:
        rec = ctx.env.ref(record['id'])
        if rec:
            # Product / source
            prod_tmp = ctx.env.ref(rec.res_id,
                                   raise_if_not_found=False)
            if not prod_tmp:
                continue
            rec.res_id = prod_tmp._name + "," + str(prod_tmp.id)
            # Account / destination
            account_tmp = ctx.env.ref(rec.value_reference,
                                      raise_if_not_found=False)
            if account_tmp:
                rec.value_reference = account_tmp._name + "," + str(
                    account_tmp.id)
            else:
                ctx.log_line(str(rec.id) + "" + rec.value_reference)
                rec.unlink()


@anthem.log
def import_serial_number(ctx):
    """ Importing serial number from csv """
    model = ctx.env['stock.production.lot'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/serial.csv', model)


@anthem.log
def import_workcenter(ctx):
    """ Importing workcenters from csv """
    load_csv(ctx, 'data/demo/workcenter.csv', 'mrp.workcenter')


@anthem.log
def import_routing(ctx):
    """ Importing Routing from csv """
    load_csv(ctx, 'data/demo/routing.csv', 'mrp.routing')
    load_csv(ctx, 'data/demo/routing_line.csv', 'mrp.routing.workcenter')


@anthem.log
def import_rma_cause(ctx):
    """ Importing RMA causes from csv """
    load_csv(ctx, 'data/demo/rma_cause.csv', 'sf.rma.cause')


@anthem.log
def import_bank(ctx):
    """ Importing bank from csv """
    model = ctx.env['res.bank'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/bank.csv', model)


@anthem.log
def import_bank_account(ctx):
    """ Importing bank account partners from csv """
    model = ctx.env['res.partner.bank'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/bank_account.csv', model)


@anthem.log
def import_sales_order(ctx):
    """ Importing sales order from csv """
    model = ctx.env['sale.order'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/sale_order_head.csv', model)
    model_item = ctx.env['sale.order.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/sale_order_line.csv', model_item)


@anthem.log
def import_purchase_order(ctx):
    """ Importing purchases order from csv """
    model = ctx.env['purchase.order'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/purchase_order_head.csv', model)
    model_item = ctx.env['purchase.order.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/purchase_order_line.csv', model_item)


@anthem.log
def import_waves(ctx):
    """ Importing waves from csv """
    model = ctx.env['stock.picking.wave'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/wave.csv', model)


@anthem.log
def import_pricelist(ctx):
    """ Importing pricelists from csv """
    model = ctx.env['product.pricelist'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/pricelist.csv', model)
    model_item = ctx.env['product.pricelist.item'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/pricelist_item.csv', model_item)


@anthem.log
def import_invoices_supplier(ctx):
    """ Importing invoices supplier from csv """
    model = ctx.env['account.invoice'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/invoice_supp_head.csv', model)
    model_item = ctx.env['account.invoice.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/invoice_supp_line.csv', model_item)


@anthem.log
def import_invoices_customer(ctx):
    """ Importing customers invoice from csv """
    load_csv(ctx, 'data/demo/invoice_cust_head.csv', 'account.invoice')
    load_csv(ctx, 'data/demo/invoice_cust_line.csv', 'account.invoice.line')


@anthem.log
def import_rma(ctx):
    """ Importing rma"""
    rma.settings(ctx)

    mrp_repair_seq = ctx.env.ref('mrp_repair.seq_mrp_repair')
    mrp_repair_seq.prefix = 'FAKE'

    rma.process_rma_draft(
        ctx,
        'data/demo/rma_draft.csv',
        'data/demo/rma_draft_repair.csv'
    )

    rma.process_rma_received(
        ctx,
        'data/demo/rma_received.csv',
        'data/demo/rma_received_repair.csv'
    )

    rma.process_rma_under_repair(
        ctx,
        'data/demo/rma_under_repair.csv',
        'data/demo/rma_under_repair_repair.csv'
    )

    rma.process_rma_2binvoiced(
        ctx,
        'data/demo/rma_2binvoiced.csv',
        'data/demo/rma_2binvoiced_repair.csv'
    )

    rma.process_rma_done_undelivered(
        ctx,
        'data/demo/rma_done_not_delivered.csv',
        'data/demo/rma_done_not_delivered_repair.csv'
    )

    rma.process_rma_done_delivered(
        ctx,
        'data/demo/rma_done_delivered.csv',
        'data/demo/rma_done_delivered_repair.csv'
    )

    mrp_repair_seq.prefix = 'RMA'


@anthem.log
def import_stock_inventory(ctx):
    """ Importing stock inventory from csv """
    model = ctx.env['stock.inventory'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/stock_inventory.csv', model)

    model_line = ctx.env['stock.inventory.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/stock_inventory_line.csv', model_line)

    inventories = ctx.env['stock.inventory'].search([])
    for inventory in inventories:
        inventory.action_done()


@anthem.log
def import_stock_warehouse_orderpoint(ctx):
    """ Importing stock warehouse reordering rules from csv """
    model = ctx.env['stock.warehouse.orderpoint'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/stock_warehouse_orderpoint.csv', model)


@anthem.log
def import_assets(ctx):
    """ Importing assets from csv """
    model = ctx.env['account.asset.asset'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/account_asset_asset.csv', model)
    model_line = ctx.env['account.asset.depreciation.line'].with_context({
        'tracking_disable': True,
    })
    load_csv(ctx, 'data/demo/account_asset_depre_line.csv', model_line)


@anthem.log
def main(ctx):
    """ Loading demo data """
    import_users(ctx)
    import_users_groups(ctx)
    import_country_state(ctx)
    import_countries(ctx)
    import_customers(ctx)
    import_suppliers(ctx)
    import_customers_properties_account(ctx)
    import_customers_properties_payterm(ctx)
    import_crm_team(ctx)
    import_waves(ctx)
    import_location(ctx)
    import_customers(ctx)
    import_drone_type(ctx)
    import_product(ctx)
    import_product_account(ctx)
    import_pricelist(ctx)
    import_serial_number(ctx)
    import_workcenter(ctx)
    import_routing(ctx)
    import_rma_cause(ctx)
    import_bank(ctx)
    import_bank_account(ctx)
    import_sales_order(ctx)
    import_purchase_order(ctx)
    import_invoices_supplier(ctx)
    import_invoices_customer(ctx)
    import_assets(ctx)
    import_rma(ctx)
    import_stock_inventory(ctx)
    import_stock_warehouse_orderpoint(ctx)
