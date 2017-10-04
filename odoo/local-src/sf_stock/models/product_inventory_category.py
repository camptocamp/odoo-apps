# -*- coding: utf-8 -*-
# Part of senseFly.

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = ['product.template']

    inventory_category_id = fields.Many2one('sf.inventory.category',
                                            string='Inventory Category')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Fix me! I had to force the filter here.
        # search_default_inventory_category_id in the action is not working
        if self._context.get('search_default_inventory_category_id'):
            args.append((('inventory_category_id', '=',
                          self._context['active_id'])))
        return super(ProductTemplate, self).search(args, offset=offset,
                                                   limit=limit, order=order,
                                                   count=count)
