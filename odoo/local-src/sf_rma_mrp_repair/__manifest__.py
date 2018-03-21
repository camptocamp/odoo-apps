# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sensefly RMA MRP Repair",
    "summary": "RMA MRP Repair related customizations",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "website": "https://www.camptocamp.com/",
    "author": "Camptocamp SA",
    "license": "AGPL-3",
    "depends": [
        "sf_rma",
        "mrp_repair",
        "sf_report"
    ],
    "data": [
        "data/mrp_repair_stage.xml",
        "security/ir.model.access.csv",
        "views/mrp_repair.xml",
        "views/rma_config_settings.xml",
        "views/stock_picking.xml",
        "report/sf_repair_report.xml"
    ],
    "application": False,
    "installable": True,
}
