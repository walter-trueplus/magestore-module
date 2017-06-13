# -*- coding: utf-8 -*-
{
    'name': "Login Case Sensivity",

    'summary': """
        Module for helping user login without case sensitivity""",

    'description': """
        Module for helping user login without case sensitivity.
        User can enable this feature by goto Settings. Unser Settings menu, click General Setting.
        In group 'Login Option', enable this feature by click 'Require Case Sensivity' checkbox field.
    """,

    'author': "Magestore",
    'website': "http://www.Magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','base_setup'],

    # always loaded
    'data': [
        'views/inherit_base_setting.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}