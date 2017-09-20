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
from odoo import api
from odoo.tools.translate import _


class MRPTeam(models.Model):
    _name = 'mrp.team'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Manufacturing Teams'
    _order = 'name'

    _sql_constraints = [
        ('unique_team_code', 'UNIQUE(code)', _('You cannot have two teams '
                                               'with the same code')),
    ]

    def _default_company(self):
        """
        Return the default companny for the mrp.team
        :return:
        """
        return self.env['res.company']._company_default_get('mrp.team')

    name = fields.Char(
        string='Name',
        size=128,
        required=True,
        translate=True,
    )
    code = fields.Char(
        string='Code',
        size=24,
        required=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help="""If the active field is set to false,
it will allow you to hide the MRP team without removing it.""",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=_default_company,
        ondelete='cascade',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Team Leader',
        ondelete='set null',
    )
    member_ids = fields.One2many(
        comodel_name='res.users',
        inverse_name='mrp_team_id',
        string='Team members',
    )
    color = fields.Integer(
        string='Color Index',
        help="The color of the team",
    )

    @api.model
    def create(self, values):
        return super(MRPTeam, self.with_context(
            mail_create_nosubscribe=True)).create(values)
