# -*- coding: utf-8 -*-
# Part of sensefly.
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def write(self, vals):
        for sale_order in self:
            # Reset delivery method
            if sale_order.state in ('draft', 'sent') and 'order_line' in vals:
                self.carrier_id = False
        return super(SaleOrder, self).write(vals)

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self,
                                             'sf_sale.sf_report_saleorder')
