# -*- coding: utf-8 -*-
{
    'name': "Create user from excel list",

    'description': """
        + Reading users excel list.
        + Create users from excel list with roles.
        + Create employee from excel list.
    """,

    'author': "magestore.com",

    'website': "http://www.magestore.com",

    'depends': ['base', 'hr'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'application': True,
    'qweb': ['static/src/xml/button_import_users.xml'],
}