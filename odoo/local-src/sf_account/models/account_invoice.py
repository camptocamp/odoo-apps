# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _compute_sale_orders(self):
        for invoice in self:
            self.order_ids = invoice.invoice_line_ids.mapped(
                'sale_line_ids').mapped('order_id')

    @api.multi
    def action_invoice_sent(self):
        """Override action_invoice_sent to modify the default template"""
        res = super(AccountInvoice, self).action_invoice_sent()
        template = \
            self.env.ref('sf_account.sf_email_template_edi_invoice', False)
        res['context']['default_template_id'] = \
            template and template.id or False
        return res

    order_ids = fields.Many2many(
        'sale.order', string='Orders', compute='_compute_sale_orders')