# -*- coding: utf-8 -*-
{
    'name': "Login with Google and Facebook",

    'summary': """
        Showing Google and other auth methods on buttons""",

    'description': """
        Module for helping user can log in to Odoo by Google or Facebook Account.
    """,

    'author': "Magestore",
    'website': "http://www.Magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','auth_oauth'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/replace_login_template.xml',
        # 'views/inherit_login_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application':True,
}