# -*- coding: utf-8 -*-
{
    'name': "Create user from excel file",

    'summary': """
        Create new employee associated with user when created an user
        
        """,

    'description': """
    This module will provides some new actions when you create an User account :
    
    + Read users from excel file
    + Create users with roles
    + Create employee for each user created
    """,

    'author': "Magestore",
    'website': "https://www.magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/form_import_user.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/button_import_user.xml',
    ],
    'application':True,
}