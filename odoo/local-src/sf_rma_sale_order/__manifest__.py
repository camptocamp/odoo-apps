# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sensefly RMA Sale Order",
    "summary": "RMA Sale order related customizations",
    "version": "10.0.1.0.0",
    "category": "Sale",
    "website": "https://www.camptocamp.com/",
    "author": "Camptocamp SA",
    "license": "AGPL-3",
    "depends": [
        "sf_rma",
        "sf_rma_mrp_repair",
    ],
    "data": [
        "data/product.xml",
        "wizard/repair_line_import.xml",
        "views/rma_config_settings.xml",
        "views/sale_order.xml",
    ],
    "application": False,
    "installable": True,
}
