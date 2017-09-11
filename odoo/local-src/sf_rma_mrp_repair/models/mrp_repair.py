# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError


MRP_REPAIR_STATE_SELECTION = [
        ('draft', 'Open'),
        ('to_analyze', 'To analyze'),
        ('to_quotation', 'To quotation'),
        ('under_repair', 'To repair'),
        ('to_test', 'To test'),
        ('to_finalize', 'To finalize'),
        ('done', 'Repaired'),
        ('cancel', 'Cancelled')]


class MrpRepair(models.Model):

    _inherit = 'mrp.repair'

    state = fields.Selection(
        MRP_REPAIR_STATE_SELECTION, required=True, default='draft',
        help="* The \'Open\' status is used when a user is encoding a new and "
             "unconfirmed repair order.\n"
             "* The \'To analyze\' status is used when RMA has to be "
             "invoiced.\n"
             "* The \'To quotation\' status is used after when RMA has to be "
             "invoiced, after being analyzed.\n"
             "* The \'To repair\' status is used to start to repairing.\n"
             "* The \'To test\' status is used after repairing.\n"
             "* The \'To finalize\' status is used after testing.\n"
             "* The \'Done\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair "
             "order."
    )

    invoicable_rma = fields.Boolean(store=True, compute='_is_invoicable')

    def _is_invoicable(self):
        for repair in self:
            repair.invoicable_rma = repair.rma_id.decision == 'to_offer'

    stage_id = fields.Many2one('mrp.repair.stage',
                               group_expand='_read_group_stage_ids',
                               compute='_compute_stage_id', store=True)

    @api.depends('state')
    def _compute_stage_id(self):
        for repair in self:
            repair.stage_id = self.env['mrp.repair.stage'].search(
                [('name', '=', repair.state)]).id

    @api.multi
    def action_repair_done(self):
        """ Custom redefinition of action_repair_done with no call to super
        because we don't want to create a stock move should the operation be
        of type replace.
        Otherwise it creates stock move for operation and stock move for final
        product of repair order.
        @return: Move ids of final products

        """
        # ***************************** Odoo code *****************************
        if self.filtered(lambda repair: not repair.repaired):
            raise UserError(_(
                "Repair must be repaired in order to make the product moves."))
        res = {}
        Move = self.env['stock.move']
        for repair in self:
            moves = self.env['stock.move']
            for operation in repair.operations:
                # ************************ Custom code ************************
                if operation.type == 'replace':
                    continue
                # ************************* Odoo code *************************
                move = Move.create({
                    'name': operation.name,
                    'product_id': operation.product_id.id,
                    'restrict_lot_id': operation.lot_id.id,
                    'product_uom_qty': operation.product_uom_qty,
                    'product_uom': operation.product_uom.id,
                    'partner_id': repair.address_id.id,
                    'location_id': operation.location_id.id,
                    'location_dest_id': operation.location_dest_id.id,
                })
                moves |= move
                operation.write({'move_id': move.id, 'state': 'done'})
            move = Move.create({
                'name': repair.name,
                'product_id': repair.product_id.id,
                'product_uom': repair.product_uom.id or
                repair.product_id.uom_id.id,
                'product_uom_qty': repair.product_qty,
                'partner_id': repair.address_id.id,
                'location_id': repair.location_id.id,
                'location_dest_id': repair.location_dest_id.id,
                'restrict_lot_id': repair.lot_id.id,
            })
            moves |= move
            moves.action_done()
            res[repair.id] = move.id
        return res

    @api.multi
    def action_repair_to_analyze(self):
        if self.filtered(lambda repair: not (repair.state == 'draft'
                                             and repair.invoicable_rma)):
            raise UserError(_('Repair must be Open and his RMA invoicable '
                              'in order to be analyzed.'))
        return self.write({'state': 'to_analyze'})

    @api.multi
    def action_repair_to_quotation(self):
        if self.filtered(lambda repair: not (repair.state == 'to_analyze'
                                             and repair.invoicable_rma)):
            raise UserError(_('Repair must be To analyze and his RMA '
                              'invoicable in order to be quoted.'))
        return self.write({'state': 'to_quotation'})

    @api.multi
    def action_repair_to_repair(self):
        if self.filtered(lambda repair: not ((repair.state == 'draft'
                                              and not repair.invoicable_rma)
                                             or (repair.state == 'to_quotation'
                                                 and repair.invoicable_rma))):
            raise UserError(_('Repair must be either To Analyze for '
                              'invoicable RMA or Open for non invoicable '
                              'RMA, in order to be repaired.'))
        self.mapped('operations').write({'state': 'confirmed'})
        return self.write({'state': 'under_repair'})

    @api.multi
    def action_repair_to_test(self):
        if self.filtered(lambda repair: repair.state != 'under_repair'):
            raise UserError(_('Repair must be to repair in order to be '
                              'tested.'))
        return self.write({'state': 'to_test'})

    @api.multi
    def action_repair_to_finalize(self):
        if self.filtered(lambda repair: repair.state != 'to_test'):
            raise UserError(_('Repairs must be to test in order to be '
                              'finalized.'))
        return self.write({'state': 'to_finalize'})

    @api.multi
    def action_repair_back_to_repair(self):
        if self.filtered(lambda repair: repair.state not in (
                'to_test', 'to_finalize')):
            raise UserError(_('Repair must be either to test or to finalize '
                              'in order to be set back to repair.'))
        return self.write({'state': 'under_repair'})

    @api.multi
    def action_repair_end(self):
        if self.filtered(lambda repair: repair.state != 'to_finalize'):
            raise UserError(_("Repair must be to finalize in order to end "
                              "reparation."))
        for repair in self:
            repair.write({'repaired': True})
            vals = {'state': 'done'}
            vals['move_id'] = repair.action_repair_done().get(repair.id)
            repair.write(vals)
        return True

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order,
                                   access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)


class MrpRepairLine(models.Model):

    _inherit = 'mrp.repair.line'

    type = fields.Selection(selection_add=[('replace', 'Replace')])

    cause_id = fields.Many2one('mrp.repair.cause', string='Cause',
                               ondelete='restrict')


class MrpRepairCause(models.Model):

    _name = 'mrp.repair.cause'
    _description = 'Cause of Mrp Repair Operation'

    name = fields.Char('Name', required=True, translate=True)

    active = fields.Boolean(default=True)


class MrpRepairStage(models.Model):
    """ This model is used to display MRP repairs on a kanban view using
    a group by state. As state is a selection field, it needs a sequence for
    the columns to appear in a logical order according to sensefly workflow."""

    _name = 'mrp.repair.stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, readonly=True, translate=False)

    sequence = fields.Integer('Sequence', default=1, readonly=True,
                              help="Used to order stages. Lower is better.")

    fold = fields.Boolean('Folded in Pipeline',
                          help='This stage is folded in the kanban view when '
                               'there are no records in that stage to '
                               'display.')

    @api.multi
    def name_get(self):
        """ Custom redefinition of name get to display translated state
        values in the kanban view"""
        selection = dict(
            self.env['mrp.repair']._fields['state']._description_selection(
                self.env))
        res = []
        for stage in self:
            res.append((stage.id, selection[stage.name]))
        return res
