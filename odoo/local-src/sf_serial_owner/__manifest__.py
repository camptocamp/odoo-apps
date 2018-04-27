# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "sf_serial_owner",
    "description": "Keep track of serial number link to customer and reseller",
    "version": "10.0.1.0.0",
    "category": "",
    "website": "https://camptocamp.com",
    "author": "Camptocamp",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock",
        "sf_rma",
        "sf_partner_entity_type",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/serial_owner.xml",
    ],
}
