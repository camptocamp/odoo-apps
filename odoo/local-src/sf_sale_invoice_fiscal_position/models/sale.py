# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.

        Override standard method to assign Invoice fiscal position
        and refresh tax amounts

        :param grouped: if True, invoices are grouped by SO id. If False,
        invoices are grouped by (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        invoice_ids = super(SaleOrder, self).action_invoice_create(
            grouped=grouped, final=final)

        # Fiscal position from delivery order partner
        picking_partner = \
            self.picking_ids.filtered(
                lambda p:
                p.state != 'cancel' and
                p.picking_type_id.code == 'outgoing').mapped('partner_id')

        if picking_partner and len(picking_partner) == 1:
            for invoice in self.env['account.invoice'].browse(invoice_ids):
                invoice.write(
                    {'fiscal_position_id': picking_partner.
                        property_account_position_id.id})
                invoice.fiscal_position_change()
        elif picking_partner and len(picking_partner) > 1:
            raise UserError(_('It is not possible to have more than one '
                              'delivery order partner per sale order!'))

        return invoice_ids
