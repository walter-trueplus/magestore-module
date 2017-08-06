# -*- coding: utf-8 -*-
{
    'name': "Create users from excel list",

    'description': """
        + Reading users excel list.
        + Create users from excel list with roles.
        + Create employee from excel list.
    """,

    'author': "magestore.com",

    'website': "http://www.magestore.com",

    'depends': ['base', 'base_import', 'hr', 'project', 'sale', 'sales_team', 'hr_timesheet', 'account'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
}