# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import models, api

# Methods that exists in the source code of mySenseFly website.
# But we are not sure if they are going to be used in the future.
NOT_IMPLEMENTED = ['write_tax_id',
                   'get_rma_by_sn',
                   'create_reseller_invoice',
                   'action_cancel_reseller',
                   'onchange_partner_id']


class MySenseFlyInterface(models.Model):
    _name = "sf.mysensefly.interface"
    _description = "MySenseFly Interface"

    @api.model
    def call(self, method, args):
        """Generic method to be called by mysensefly website through xmlrpc."""
        if method == 'get_spare_parts':
            assert len(args) == 2, \
                "%s expects 2 parameters." % method
            assert isinstance(args[0], int) and isinstance(args[1], int), \
                "Parameters must be integers."

            drone_type = self.env['drone.type'].browse(args[0])
            return drone_type.get_spare_parts(args[1:])
        elif method in NOT_IMPLEMENTED:
            return "To be implemented!"
        else:
            return "Not implemented!"
