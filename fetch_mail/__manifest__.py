# -*- coding: utf-8 -*-
{
    'name': "Fetch Mail",

    'summary': """
        Provide button for fetch incoming mail and show list fetched mail.""",

    'description': """
        Odoo module - Fetch Mails
        This module will provide some usefull actions for you:
        + create new model for mail alias
        + show all mails incoming through mail alias you created before
        + show button for fetch mail manually
        You must add 
        """,

    'author': "Mars",
    'website': "http://career.magestore.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'VIP',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'fetchmail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'qweb': [
        'static/src/xml/fetch_mail.xml',
    ],
    'application': True,
    'installable': True,
    # 'auto_install': True,
}
