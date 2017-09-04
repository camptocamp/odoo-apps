# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import api, models, _
from datetime import datetime
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.multi
    def button_done_as_planned(self):

        timeline = self.env['mrp.workcenter.productivity']
        loss = self.env['mrp.workcenter.productivity.loss'].search([(
            'loss_type', '=', 'performance')], limit=1)
        if not loss:
            raise UserError(_(
                "You need to define at least one productivity "
                "loss in the category 'Performance'. "
                "Create one from the Manufacturing app, "
                "menu: Configuration / Productivity Losses."))
        for workorder in self:

            if workorder.production_id.state != 'progress':
                workorder.production_id.write({
                    'state': 'progress',
                    'date_start': datetime.now() - relativedelta(
                        minutes=workorder.duration_expected),
                })
            timeline.create({
                'workorder_id': workorder.id,
                'workcenter_id': workorder.workcenter_id.id,
                'description': _('Time Tracking: ')+self.env.user.name,
                'loss_id': loss.id,
                'date_start': datetime.now() - relativedelta(
                    minutes=workorder.duration_expected),
                'date_end': datetime.now(),
                'user_id': self.env.user.id
            })
        return self.write({
                    'state': 'done',
                    'date_finished': datetime.now(),
        })
