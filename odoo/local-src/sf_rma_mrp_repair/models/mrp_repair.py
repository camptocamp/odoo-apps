# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError


MRP_REPAIR_STATE_SELECTION = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('to_analyze', 'To analyze'),
        ('to_quotation', 'To quotation'),
        ('under_repair', 'To repair'),
        ('to_test', 'To test'),
        ('to_finalize', 'To finalize'),
        ('done', 'Repaired'),
        ('cancel', 'Cancelled')]


class MrpRepair(models.Model):

    _inherit = 'mrp.repair'

    @api.model
    def _default_stock_location(self):
        """
        Override _default_stock_location to pick the repair location
        in RMA configuration, if defined.
        """
        comp = self.env.user.company_id
        if comp.rma_repair_location_id:
            return comp.rma_repair_location_id.id
        else:
            return super(MrpRepair, self)

    def _get_drone_flight_time(self):
        for record in self:
            record.drone_flight_time = record.rma_id.drone_flight_time

    def _set_drone_flight_time(self):
        for record in self:
            record.rma_id.drone_flight_time = record.drone_flight_time

    def _get_drone_flight_num(self):
        for record in self:
            record.drone_flight_num = record.rma_id.drone_flight_num

    def _set_drone_flight_num(self):
        for record in self:
            record.rma_id.drone_flight_num = record.drone_flight_num

    def _get_drone_firmware_version(self):
        for record in self:
            record.drone_firmware_version = \
                record.rma_id.drone_firmware_version

    def _set_drone_firmware_version(self):
        for record in self:
            record.rma_id.drone_firmware_version = \
                record.drone_firmware_version

    location_id = fields.Many2one(
        'stock.location', 'Current Location',
        default=_default_stock_location,
        index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', True)]})
    # Drone info
    drone_flight_time = fields.Float(
        "Hours of flight",
        compute='_get_drone_flight_time',
        inverse='_set_drone_flight_time',
        help="Drone hours of flight")
    drone_flight_num = fields.Integer(
        "Number of flights",
        compute='_get_drone_flight_num',
        inverse='_set_drone_flight_num',
        help="Drone number of flights")
    drone_firmware_version = fields.Char(
        "Firmware number",
        compute='_get_drone_firmware_version',
        inverse='_set_drone_firmware_version',
        help="Drone firmware number")

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

    invoicable_rma = fields.Boolean(store=True, compute='_is_rma_invoicable')

    @api.depends('rma_id.decision')
    def _is_rma_invoicable(self):
        for repair in self:
            repair.invoicable_rma = repair.rma_id \
                                    and repair.rma_id.decision == 'to_invoice'

    stage_id = fields.Many2one('mrp.repair.stage',
                               group_expand='_read_group_stage_ids',
                               compute='_compute_stage_id', store=True)

    @api.depends('state')
    def _compute_stage_id(self):
        for repair in self:
            repair.stage_id = self.env['mrp.repair.stage'].search(
                [('name', '=', repair.state)]).id

    @api.multi
    def action_repair_open(self):
        if self.filtered(lambda repair: repair.state != 'draft'):
            raise UserError(_("Repair must be in Draft in order to Open"))
        return self.write({'state': 'open'})

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
        if self.filtered(lambda repair: not (repair.state == 'open'
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
        if self.filtered(lambda repair: not ((repair.state == 'open'
                                              and not repair.invoicable_rma)
                                             or (repair.state == 'to_quotation'
                                                 and repair.invoicable_rma))):
            raise UserError(_('Repair must be either To Analyze for '
                              'invoicable RMA or Open for non invoicable '
                              'RMA, in order to be repaired.'))
        return self.write({'state': 'under_repair'})

    @api.multi
    def action_repair_back_to_analyze(self):
        if self.filtered(lambda repair: not repair.invoicable_rma and
                         repair.state != 'under_repair'):
            raise UserError(_('Repair must be To repair and his RMA invoicable'
                              'in order to set it back to analyze.'))
        return self.write({'state': 'to_analyze'})

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
            repair.mapped('operations').write({'state': 'confirmed'})
            repair.write({'repaired': True})
            vals = {'state': 'done'}
            # Use context without default_ values to generate stock.move
            move_create_context = {key: val for key, val
                                   in self.env.context.iteritems()
                                   if 'default_' not in key}
            vals['move_id'] = repair.with_context(
                move_create_context).action_repair_done().get(repair.id)
            repair.write(vals)

            repair.mapped(
                'rma_id.sale_ids.order_line'
            ).filtered(
                lambda l: l.order_id.state == 'sale'
            )._action_procurement_create()
        return True

    @api.multi
    def action_view_rma(self):
        action = self.env.ref('sf_rma.sf_rma_action').read()[0]
        if self.rma_id:
            action['views'] = [(self.env.ref('sf_rma.sf_rma_form_view').id,
                                'form')]
            action['res_id'] = self.rma_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

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

    type = fields.Selection(
        selection_add=[('replace', 'Replace')], default='add')

    cause_id = fields.Many2one('mrp.repair.cause', string='Cause',
                               ondelete='restrict')

    @api.onchange('type', 'repair_id')
    def onchange_operation_type(self):
        """Override onchange_operation_type to pick the source location from
        RMA configuration.
        """
        super(MrpRepairLine, self).onchange_operation_type()
        if self.type == 'add':
            comp = self.env.user.company_id
            if comp.rma_repair_line_src_location_id:
                self.location_id = comp.rma_repair_line_src_location_id


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
