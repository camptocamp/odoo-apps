# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        picking_partner = self.picking_ids.filtered(
            lambda p:
            p.state != 'cancel' and
            p.picking_type_id.code == 'outgoing').mapped('partner_id')
        if picking_partner and len(picking_partner) == 1:
            res.update({
                'fiscal_position_id':
                    picking_partner.property_account_position_id.id
            })
        elif picking_partner and len(picking_partner) > 1:
            raise UserError(_('It is not possible to have more than one '
                              'delivery order partner per sale order!'))
        return res

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        return super(SaleOrder, self).action_invoice_create(grouped=True)
