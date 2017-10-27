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

    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()

        # Replace default email template
        ir_model_data = self.env['ir.model.data']

        try:
            template_id = ir_model_data.get_object_reference(
                'sf_sale', 'sf_email_template_edi_sale')[1]
        except ValueError:
            template_id = False

        res['context'].update(
            {
                'default_use_template': bool(template_id),
                'default_template_id': template_id
             })
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_to_invoice_qty(self):
        """
        Change computation of the quantity to invoice.

        If the quantity delivered is used, we set it to the ordered quantity
        only if the total quantity is delivered.

        Otherwise, when the invoice policy is order, no change to the quantity
        to invoice, it is calculated from the ordered quantity.

        """
        on_deliver_lines = self.filtered(
            lambda rec: (rec.product_id.invoice_policy != 'order' and
                         rec.order_id.state in ['sale', 'done']))

        for line in on_deliver_lines:
            if line.product_uom_qty == line.qty_delivered:
                line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
            else:
                line.qty_to_invoice = 0

        other_lines = self - on_deliver_lines
        super(SaleOrderLine, other_lines)._get_to_invoice_qty()
