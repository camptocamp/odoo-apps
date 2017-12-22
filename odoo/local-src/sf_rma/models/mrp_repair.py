# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models, api


class MRPRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.depends('state')
    def _compute_user_id(self):
        for repair in self:
            repair.user_id = self.env.uid

    rma_id = fields.Many2one('sf.rma', string="RMA")
    rma_state = fields.Selection(related='rma_id.state', readonly=True)

    user_id = fields.Many2one('res.users', string="Technician",
                              compute='_compute_user_id', store=True,
                              track_visibility='onchange')
    planned_date = fields.Date()
    other_notes = fields.Text(string="Other")
    invoice_notes = fields.Text(string="Invoice")
    note_resolution = fields.Text(string="Resolution")
    action_todo = fields.Text(string="Action to do")
    image_arrival = fields.Binary(attachment=True)
    image_departure = fields.Binary(attachment=True)
    # TODO time spent fields TBD
