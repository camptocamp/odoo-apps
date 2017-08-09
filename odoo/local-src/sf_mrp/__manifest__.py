# -*- coding: utf-8 -*-
# Part of senseFly.

{
    'name': 'SenseFly Manufacturing',
    'version': '1.0',
    'author': 'Anar Baghirli',
    'category': 'SenseFly',
    'depends': ['mrp'],
    'description': """
This is a module for customization of senseFly manufacturing

Custom actions:
* mrp.workorder
    - done_as_planned: button which add timetracking line based on planned duration
    """,
    'data': ['views/sf_mrp_workorder.xml'],
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
