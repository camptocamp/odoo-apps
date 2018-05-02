# -*- coding: utf-8 -*-
# Part of sensefly.
from odoo import models, api
from urlparse import urljoin
import logging
import requests

_logger = logging.getLogger(__name__)

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

    def get_sensefly_api_parameters(self, endpoint):
        SysParam = self.env['ir.config_parameter']
        parameters = {
            'base_url': SysParam.get_param('api.sensefly.url'),
            'user': SysParam.get_param('api.sensefly.user'),
            'password': SysParam.get_param('api.sensefly.password'),
            'endpoint': SysParam.get_param(endpoint)
        }
        for key in parameters:
            if not parameters[key]:
                _logger.warning("Api parameter %s not configured." % key)
                return False
        return parameters

    def assign_invitation_key(self, data):
        parameters = self.get_sensefly_api_parameters(
            'api.sensefly.invitation_keys'
        )

        # This build a url like:
        # https://test.sensefly.io/v1/invitation-keys/1234-1234
        URL = urljoin(
            urljoin(parameters['base_url'], parameters['endpoint']),
            data['invitationKey'])

        auth = requests.auth.HTTPBasicAuth(
            parameters['user'], parameters['password']
        )
        try:
            response = requests.put(URL, json=data, auth=auth)
        except Exception, e:
            log_msg = "Invitation key can not be assigned: %s" % e.message
            _logger.exception(log_msg)
            return False

        if response.status_code in (200, 201, 204):
            log_msg = "Invitation key %s successfully updated" % \
                      data['invitationKey']
            _logger.info(log_msg)
            return True
        else:
            log_msg = "Invitation key %s api request update returned status " \
                      "code %s." % (data['invitationKey'],
                                    str(response.status_code))
            if response.status_code == 500:
                log_msg += "\n" + response.text
                log_msg += "\n" + str(data)
            _logger.warning(log_msg)
            return False
