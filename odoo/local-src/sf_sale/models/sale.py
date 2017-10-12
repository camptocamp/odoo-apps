# -*- coding: utf-8 -*-
# Part of sensefly.
from lxml import etree
import json

from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(SaleOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            # Delivery method is editable
            # only for group_delivery_method_manager
            doc = etree.XML(res['arch'])
            if self.user_has_groups("sf_stock.group_delivery_method_manager"):
                node = doc.xpath("//field[@name='carrier_id']")[0]
                node.set("readonly", "0")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = [
                    ('state', 'not in', ('draft', 'sent'))]
                node.set("modifiers", json.dumps(modifiers))

            res['arch'] = etree.tostring(doc)
        return res

    @api.multi
    def write(self, vals):
        for sale_order in self:
            # Onchange order lines reset delivery method
            if sale_order.state in ('draft', 'sent') and 'order_line' in vals:
                self.carrier_id = False
        return super(SaleOrder, self).write(vals)

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self,
                                             'sf_sale.sf_report_saleorder')
