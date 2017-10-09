# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


class Purchase(models.Model):
    _inherit = "purchase.order"

    second_vendor_id = fields.Many2one(
        'res.partner',
        string='Secondary Vendor',
        help='An indirect supplier.')
    print_draft = fields.Boolean(
        string='Print Draft',
        help='Print draft stamp on the top of the request for quotation '
             'document.')

    @api.multi
    def button_confirm(self):
        res = super(Purchase, self).button_confirm()
        self.print_draft = False
        return res

    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env['report'].get_action(
            self, 'sf_purchase.sf_report_purchasequotation')
