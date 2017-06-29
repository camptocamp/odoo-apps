# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, models


class OnchangePlayer(models.AbstractModel):

    _inherit = 'base'

    def get_new_values(self, record, on_change_result, model=None):
        vals = on_change_result.get('value', {})
        new_values = {}
        for fieldname, value in vals.iteritems():
            if fieldname not in record:
                if model:
                    column = self.env[model]._fields[fieldname]
                    if column.type == 'many2one':
                        value = value[0]  # many2one are tuple (id, name)
                new_values[fieldname] = value
        return new_values

    @api.model
    def play_onchanges(self, values, onchange_fields):
        onchange_specs = self._onchange_spec()

        # we need all fields in the dict even the empty ones
        # otherwise 'onchange()' will not apply changes to them
        all_values = values.copy()
        for field in self._fields:
            if field not in all_values:
                all_values[field] = False

        # we work on a temporary record
        new_record = self.new(all_values)

        new_values = {}
        for field in onchange_fields:
            onchange_values = new_record.onchange(all_values,
                                                  field, onchange_specs)
            new_values.update(self.get_new_values(values, onchange_values,
                                                  model=self._name))
            all_values.update(new_values)

        res = {f: v for f, v in all_values.iteritems()
               if f in values or f in new_values}
        return res

    @api.model
    def create_with_onchanges(self, values, onchange_fields):
        """ play onchanges and call create with updated values """
        data = values.copy()
        data.update(self.play_onchanges(data, onchange_fields))
        return self.create(data)
