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

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    @api.depends('mrp_team_id')
    def _compute_is_mrp_team_member(self):
        for user in self:
            user.is_mrp_team_member = bool(self.mrp_team_id)

    @api.multi
    def _get_available_member(self, operator, _):
        """
        If no value, return all users.
        :param operator:
        :param value:
        :return:
        """
        if operator == '=':
            member_ids = self.search([('mrp_team_id', '!=', False)])
        else:
            member_ids = self.search([('mrp_team_id', '=', False)])

        return [('id', 'in', [x.id for x in member_ids])]

    mrp_team_id = fields.Many2one(
        comodel_name='mrp.team',
        string='Manufacturing Team',
        help="""Manufacturing Team the user is member of.
Used to compute the members of a mrp team through the inverse one2many""",
        ondelete='set null',
    )
    is_mrp_team_member = fields.Boolean(
        string='Is member of the team ?',
        compute='_compute_is_mrp_team_member',
        search='_get_available_member',
    )
