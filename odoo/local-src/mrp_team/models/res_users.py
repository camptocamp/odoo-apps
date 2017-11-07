# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Quentin Theuret
#    Copyright 2017 SenseFly, Amaris
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models
from odoo import fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    @staticmethod
    def _get_available_member(self, operator, value):
        """
        If no value, return all users.
        :param operator: 
        :param value: 
        :return: 
        """
        if not value:
            return [('share', '=', False)]
        else:
            return [('mrp_team_ids', operator, value)]

    mrp_team_ids = fields.Many2many(
        comodel_name='mrp.team',
        column1='team_id',
        column2='user_id',
        relation='mrp_team_users',
        string='MRP Teams',
    )
    is_mrp_team_member = fields.Boolean(
        string='Is member of the team ?',
        compute=lambda *a: True,
        search=_get_available_member,
    )

