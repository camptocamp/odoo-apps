# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _
from odoo.exceptions import MissingError
from urlparse import urljoin
import requests
import logging

_logger = logging.getLogger(__name__)


class RmaCallBack(models.Model):
    _name = "rma.callback"

    @api.model
    def call(self, url_suffix, rma_ids):
        base_url = self.env.user.company_id.web_hook_base_url
        if not base_url:
            raise MissingError(_("Rma web hook base url not configured!"))

        for rma in self.env['mrp.repair'].browse(rma_ids):
            url = urljoin(base_url, url_suffix + '/' + rma.name)

            rma_call = self.search([('url', '=', url)], limit=1)

            if rma_call:
                # We do not make the call twice but we want to log it
                rma_call.count += 1
            else:
                response = None
                try:
                    response = requests.get(url)

                    self.env['rma.callback'].create(
                        {
                            'url': url,
                            'status_code': response.status_code,
                            'count': 1
                        }
                    )
                except Exception, e:
                    log_msg = "Called %s. %s." % (
                        url, e.message,)
                    _logger.exception(log_msg)

                if response:
                    log_msg = "Called %s. Status code %s." % (
                        url, response.status_code,)
                    _logger.info(log_msg)

    url = fields.Char(required=True)
    status_code = fields.Integer(required=True)
    count = fields.Integer(default=1)
