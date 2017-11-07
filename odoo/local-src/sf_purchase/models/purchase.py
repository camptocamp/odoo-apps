# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api


class Purchase(models.Model):
    _inherit = "purchase.order"

    second_vendor_id = fields.Many2one(
        'res.partner',
        string='Secondary Vendor',
        help='An indirect supplier.')
    confirmation_date = fields.Datetime(
        string='Confirmation Date',
        readonly=True, index=True,
        help="Date on which the purchase order is confirmed.")
    print_draft = fields.Boolean(
        string='Print Draft',
        help='Print draft stamp on the top of the request for quotation '
             'document.')

    @api.multi
    def button_confirm(self):
        res = super(Purchase, self).button_confirm()
        self.write({
            'confirmation_date': fields.Datetime.now(),
            'print_draft': False
        })

        return res

    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env['report'].get_action(
            self, 'sf_purchase.sf_report_purchasequotation')
