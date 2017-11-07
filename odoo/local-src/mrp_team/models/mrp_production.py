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


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    team_id = fields.Many2one(
        comodel_name='mrp.team',
        string='Manufacturing Team',
        required=False,
        help="""If set, manufacturing team used notably to select the 
        technician who will handle this order.""",
        ondelete='set null',
    )
    technician_id = fields.Many2one(
        comodel_name='res.users',
        string='Technician',
        required=False,
        ondelete='set null',
    )