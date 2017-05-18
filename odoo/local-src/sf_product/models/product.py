# -*- coding: utf-8 -*-
# Part of sensefly.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    origin_id = fields.Many2one('res.country', string='Country of Origin')
