# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Partner entity type",
    "summary": "To define entity on partners",
    "version": "10.0.1.0.0",
    "category": "CRM",
    "website": "https://camptocamp.com",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/entity_type.xml",
        "views/partner.xml",
        "data/entity_type.xml",
    ],
}
