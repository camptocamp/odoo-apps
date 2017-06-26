# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    @api.multi
    def default_budget_range_type(self):
        """Get the value from the last configuration record.
        Strange behavior because each time configuration change new config
        record id added!
        """
        return self.search([], limit=1, order='id desc').budget_range_type_id

    budget_range_type_id = fields.Many2one(
        'date.range.type', string='Budget period range type',
        default=default_budget_range_type)
