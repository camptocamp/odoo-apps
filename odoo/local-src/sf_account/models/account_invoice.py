# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import json
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _compute_sale_orders(self):
        for invoice in self:
            invoice.order_ids = invoice.invoice_line_ids.mapped(
                'sale_line_ids').mapped('order_id')

    @api.depends('invoice_line_ids.product_id')
    def _is_downpayment_invoice(self):
        downpay_prod_id = \
            self.env['sale.advance.payment.inv']._default_product_id()
        for inv in self:
            inv.is_down_pay_inv = inv.type == 'out_invoice' and \
                                  any(line.product_id == downpay_prod_id
                                      and line.quantity > 0
                                      for line in inv.invoice_line_ids)

    @api.multi
    def invoice_validate(self):
        """Assign downpayment invoice sequence"""
        res = super(AccountInvoice, self).invoice_validate()
        for inv in self:
            if inv.is_down_pay_inv:
                inv.number = self.env['ir.sequence'].next_by_code(
                    'downpay.invoice'
                )
        return res

    @api.multi
    def action_invoice_sent(self):
        """Override action_invoice_sent to modify the default template"""
        res = super(AccountInvoice, self).action_invoice_sent()
        template = \
            self.env.ref('sf_account.sf_email_template_edi_invoice', False)
        res['context']['default_template_id'] = \
            template and template.id or False
        return res

    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
            Note: override standard method replacing the report.
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(
            self, 'sf_account.sf_report_invoice')

    @api.one
    def get_payment_info(self):
        # Just load JSON payment info
        json_data = self.payments_widget
        try:
            payment_info = json.loads(json_data)
        except Exception, e:
            log_msg = "Error loading payment info. %s." % (e.message,)
            _logger.exception(log_msg)
            raise ValidationError('Error loading payment info. %s' % e.message)

        if payment_info:
            return payment_info.get('content', False)
        return False

    order_ids = fields.Many2many(
        'sale.order', string='Orders', compute='_compute_sale_orders')
    partner_ref = fields.Char(
        string='Partner Reference',
        help='Invoice number of the partner'
    )
    linked_partner_bank_id = fields.Many2one(
        related='partner_id.bank_ids.linked_partner_id', readonly=True)
    is_down_pay_inv = fields.Boolean(
        string='Downpayment Invoice',
        compute='_is_downpayment_invoice',
        help='This is a down payment invoice'
    )
