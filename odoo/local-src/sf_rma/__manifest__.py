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
    "depends": [
        "base",
    ],
    "data": [
        "security/rma_security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/rma.xml",
        "views/rma_cause.xml",
    ],
}
