# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api


def get_selection_description(rec, field):
    """ Get translated selection description from its selected value """
    return dict(rec._fields[field]._description_selection(rec.env))[rec[field]]


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _compute_repairs(self):
        for pick in self:
            repair_name = pick.group_id.name
            repair_ids = self.env['mrp.repair'].search(
                [('name', '=', repair_name)])
            if repair_ids:
                pick.repair_ids = repair_ids.ids

    @api.one
    @api.depends('repair_ids')
    def _compute_repair_count(self):
        self.repair_count = len(self.repair_ids)
        if self.repair_count == 1:
            state = get_selection_description(self.repair_ids, 'state')
            self.repair_state = state

    @api.multi
    def action_view_repair(self):
        rma = self.repair_ids.mapped('rma_id')
        assert not len(rma) > 1, "Repairs must belong to the same RMA."

        action = rma.action_view_relation(
            'repair_ids',
            'mrp_repair.action_repair_order_tree',
            'mrp_repair.view_repair_order_form')
        values = rma._prepare_mrp_repair_data()
        values = {'default_' + k: v for k, v in values.iteritems()}
        action['context'] = values
        return action

    repair_ids = fields.One2many(
        comodel_name='mrp.repair',
        string="Repairs",
        compute="_compute_repairs")
    repair_count = fields.Integer(
        compute='_compute_repair_count',
        string="# Repairs")
    repair_state = fields.Char(
        compute="_compute_repair_count")

    @api.multi
    def do_new_transfer(self):
        for pick in self:
            # RMA reception? Open the repair
            if pick.rma_id and pick.picking_type_id.code == 'incoming':
                for repair in pick.rma_id.repair_ids:
                    repair.state = 'open'
        return super(StockPicking, self).do_new_transfer()
