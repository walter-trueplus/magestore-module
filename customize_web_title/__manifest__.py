# -*- coding: utf-8 -*-
{
    'name': "Customize web title ",

    'summary': """
        Replace default Odoo title in web page by user's custom title!
        """,

    'description': """
        This module for helping change default Odoo title in web page by user's customize title.
        To change web page title, go to Settings, in General Settings, change title for web page in field "Web title setting".
    """,

    'author': "Magestore",
    'website': "http://www.Magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/asset_inherit.xml',
        'views/setting_view_inherit.xml',
    ],
    'application': True,
    # only loaded in demonstration mode

}
