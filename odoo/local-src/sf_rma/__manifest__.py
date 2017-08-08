# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "Sensefly RMA",
    "summary": "Return merchandise authorization",
    "version": "10.0.1.0.0",
    "category": "RMA",
    "website": "https://camptocamp.com",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "post_init_hook": 'post_init_hook',
    "depends": [
        "sale",
        "stock",
        "mrp_repair",
        "sf_stock",
        "web_domain_field"
    ],
    "data": [
        "security/rma_security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/rma.xml",
        "views/rma_cause.xml",
        "views/mrp_repair.xml",
        "data/crm_team.xml",
        "data/pricelist.xml",
        "data/ir_sequence.xml",
        "data/ir_config_parameter.xml",
    ],
}
