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

        def _get_rma_service_placeholder(product):

            comp = self.env.user.company_id
            rma_service_service = comp.rma_service_service_product_id
            if not rma_service_service:
                raise UserError(_('Repair Service for services has to be '
                                  'defined in the RMA Settings.'))
            rma_service_consu = comp.rma_service_consumable_product_id
            if not rma_service_consu:
                raise UserError(_('Repair Service for consumables has to be '
                                  'defined in the RMA Settings.'))
            rma_service_stock = comp.rma_service_stockable_product_id
            if not rma_service_stock:
                raise UserError(_('Repair Service for stockables has to be '
                                  'defined in the RMA Settings.'))

            if product.type == 'service':
                return rma_service_service
            elif product.type == 'consu':
                return rma_service_consu
            elif product.type == 'product':
                return rma_service_stock
            else:
                return

        additional_description = \
            self.env.user.company_id.rma_service_additional_description

        values = []

        for line in self.with_context(
                pricelist=self.sale_order_id.pricelist_id.id).repair_line_ids:

            line_dict = {
                'price_unit': line.product_id.price,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
            }

            name = [line.name]
            if additional_description:
                name.append(additional_description)
            line_dict['name'] = '\n'.join(name)

            line_dict['product_id'] = _get_rma_service_placeholder(
                line.product_id).id

            values.append(
                (0, 0, line_dict))

        self.sale_order_id.write({
            'order_line': values
        })
        return
