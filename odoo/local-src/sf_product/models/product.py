# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models, api, _
import uuid


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange('sale_ok', 'purchase_ok', 'validated')
    def onchange_sale_purchase_ok(self):
        if not self.validated and (self.sale_ok or self.purchase_ok):
            return {
                'warning': {
                    'title': _('Product not Validated!'),
                    'message':
                        _('Only validated products can be sold or purchased.')
                },
                'value': {
                    'sale_ok': False,
                    'purchase_ok': False},
                }

    def _compute_validator_user(self):
        for product in self:
            product.validator_user =\
                self.env.user.has_group('sf_product.group_product_validator')

    origin_id = fields.Many2one('res.country', string='Country of Origin')
    sale_ok = fields.Boolean(
        'Can be Sold', default=False,
        help="Specify if the product can be selected in a sales order line.")
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
    validated = fields.Boolean(
        help="This product can be sold/purchased when validated.",
    )

    validator_user = fields.Boolean(compute='_compute_validator_user')
    validation_state = fields.Selection([
        ('1sales', 'Sales'),
        ('2industrialisation', 'Industrialisation'),
        ('3shipping', 'Shipping'),
        ('4css', 'CSS'),
        ('5accounting', 'Accounting'),
    ])
    uuid = fields.Char(
        'UUID', index=True, default=lambda self: '%s' % uuid.uuid4(),
        required=True)

    _sql_constraints = [
        ('unique_uuid', 'UNIQUE(uuid)', 'UUID must be unique!'),
    ]


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _is_deposit_product(self):
        deposit_product_id = \
            self.env['sale.advance.payment.inv']._default_product_id()
        for product in self:
            product.is_deposit = product == deposit_product_id

    is_deposit = fields.Boolean(
        compute='_is_deposit_product',
        help="Is this product used for upfront payments?",
    )
