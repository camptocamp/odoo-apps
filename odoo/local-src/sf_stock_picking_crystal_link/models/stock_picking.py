# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_crystal_report_link_url(self):
        Parameters = self.env['ir.config_parameter'].sudo()
        return Parameters.get_param('packing.list.crystal.report.url')

    @api.multi
    def _get_packing_list_url(self):
        # URL like http://crystalreports/ReCrystallizeServer/ViewReport.aspx?
        # reportName=C:\ReCrystallizeServer\Reports\Supply%%20Chain\
        # Packing_List.rpt&P1=%s
        url = self._get_crystal_report_link_url()
        if not url:
            _logger.info(
                "Parameter packing.list.crystal.report.url not set!")
            return None

        for picking in self:
            try:
                picking.packing_list_url = url % picking.id
            except BaseException:
                raise UserError(_(
                    "Parameter packing.list.crystal.report.url "
                    "is not properly set."))

    packing_list_url = fields.Char(
        string='Packing List',
        compute=_get_packing_list_url)
