# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    number = fields.Char('Ticket Number', readonly=True, required=True,
                         default=lambda self: self.env['ir.sequence']
                         .next_by_code('helpdesk.ticket'))
    solution = fields.Text(string='Solution')
    partner_id = fields.Many2one('res.partner', string='Created by',
                                 default=lambda self:
                                 self.env.user.partner_id.id)
