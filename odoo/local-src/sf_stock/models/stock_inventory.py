# -*- coding: utf-8 -*-
# Part of senseFly.

from odoo import fields, models, api, _


class Inventory(models.Model):
    _inherit = ['stock.inventory']

    inventory_category_id = fields.Many2one(
        'sf.inventory.category',
        string='Inventory Category')

    @api.model
    def _selection_filter(self):
        res_filter = super(Inventory, self)._selection_filter()
        res_filter.append(('inventory_category', _('One inventory category')))
        return res_filter

    @api.onchange('filter')
    def onchange_filter(self):
        if self.filter != 'inventory_category':
            self.inventory_category_id = False
        else:
            super(Inventory, self).onchange_filter()

    @api.multi
    def _get_inventory_lines_values(self):
        # Overriding the standard method to include a new filter.
        # TS CLEAN ME: Probably sql usage could have been avoided

        # case 6: Filter on Inventory Category
        if self.inventory_category_id:
            locations = self.env['stock.location'].search(
                [('id', 'child_of', [self.location_id.id])])

            domain = ' location_id in %s'
            args = (tuple(locations.ids),)

            vals = []
            Product = self.env['product.product']
            # Empty recordset of products available in stock_quants
            quant_products = self.env['product.product']
            # Empty recordset of products to filter
            products_to_filter = self.env['product.product']

            inventory_categ_products = Product.search(
                [('inventory_category_id',
                  '=', self.inventory_category_id.id)])
            domain += ' AND product_id = ANY (%s)'
            args += (inventory_categ_products.ids,)
            products_to_filter |= inventory_categ_products

            self.env.cr.execute(
                """
                SELECT product_id, sum(qty) as product_qty, location_id,
                lot_id as prod_lot_id, package_id, owner_id as partner_id
                FROM stock_quant
                WHERE %s
                GROUP BY product_id, location_id, lot_id, package_id,
                partner_id """ % domain, args)

            for product_data in self.env.cr.dictfetchall():
                for void_field in [item[0] for item in product_data.items() if
                                   item[1] is None]:
                    product_data[void_field] = False
                product_data['theoretical_qty'] = product_data['product_qty']
                if product_data['product_id']:
                    product_data['product_uom_id'] = Product.browse(
                        product_data['product_id']).uom_id.id
                    quant_products |= Product.browse(
                        product_data['product_id'])
                vals.append(product_data)
            if self.exhausted:
                exhausted_vals = self._get_exhausted_inventory_line(
                    products_to_filter, quant_products)
                vals.extend(exhausted_vals)
            return vals
        else:
            return super(Inventory, self)._get_inventory_lines_values()
