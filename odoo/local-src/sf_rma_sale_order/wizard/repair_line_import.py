# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrderRepairLinesImportWizard(models.TransientModel):

    _name = 'sale.order.repair.lines.import'

    repair_line_ids = fields.Many2many('mrp.repair.line',
                                       string='Repair lines')

    sale_order_id = fields.Many2one('sale.order', string='Sale order',
                                    readonly=True)

    rma_id = fields.Many2one('sf.rma', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderRepairLinesImportWizard, self).default_get(fields)
        sale_id = res.get('sale_order_id') or self.env.context.get('active_id')
        sale = self.env['sale.order'].browse(sale_id)
        rma = sale.rma_id
        if rma:
            res.update({'rma_id': rma.id})
            repair_lines = rma.repair_ids.mapped('operations')
            if repair_lines:
                res.update({'repair_line_ids': repair_lines.ids})
        else:
            raise ValidationError(_('Importation of repair order lines is '
                                    'only allowed on sale orders originating '
                                    'from RMA.'))
        return res

    @api.multi
    def import_lines(self):
        rma_service = self.env.user.company_id.rma_service_product_id
        if not rma_service:
            raise UserError(_('A RMA repair service product has to be defined '
                              'in the RMA Settings.'))
        values = []
        for line in self.repair_line_ids:
            values.append(
                (0, 0, {
                    'name': line.name,
                    'product_id': rma_service.id,
                    'price_unit': line.product_id.list_price,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                }))

        self.sale_order_id.write({
            'order_line': values
        })
        return
