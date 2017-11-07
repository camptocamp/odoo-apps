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

{
    'name': 'MRP Team',
    'summary': 'Manufacturing Teams',
    'version': '10.0.1.0.0',
    'depends': [
        'mrp',
    ],
    'author': "senseFly,Amaris",
    'license': 'AGPL-3',
    'description': """
This module introduces production teams.
============================================
Product teams can be associated to a manufacturing
order and the technician linked to the MO should be
part of this team.
""",
    'category': 'Manufacturing',
    'data': [
        # Views
        'views/mrp_team_view.xml',
        'views/mrp_production_view.xml',
        # Data
        # Security
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'application': False,
    'installable': True,
}
