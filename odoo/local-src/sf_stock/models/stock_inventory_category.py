# -*- coding: utf-8 -*-
# Part of senseFly.

from odoo import fields, models


class InventoryCategory(models.Model):
    _name = 'sf.inventory.category'
    _description = "Inventory Category"
    _order = "name"

    name = fields.Char('Inventory Category', required=True)
    active = fields.Boolean(default=True,
                            help="If the active field is set to false, "
                                 "it will allow you to hide "
                                 "the inventory category "
                                 "without removing it.")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self:
                                 self.env['res.company']._company_default_get(
                                     'sf.inventory.category'))
    product_template_ids = fields.One2many(
        comodel_name='product.template',
        inverse_name='inventory_category_id',
        string='Products')
    product_count = fields.Integer(
        '# Products', compute='_compute_product_count',
        help="The number of products under this category")

    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group(
            [('inventory_category_id', 'in', self.ids)],
            ['inventory_category_id'],
            ['inventory_category_id'])
        group_data = dict((data['inventory_category_id'][0],
                           data['inventory_category_id_count'])
                          for data in read_group_res)
        for categ in self:
            categ.product_count = group_data.get(categ.id, 0)
