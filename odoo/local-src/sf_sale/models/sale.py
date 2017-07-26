# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self,
                                             'sf_sale.sf_report_saleorder')
