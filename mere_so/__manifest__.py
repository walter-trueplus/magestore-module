# -*- coding: utf-8 -*-
{
    'name': "merge_so",

    'summary': """
        this module allow user Merge (some) sale_order from same partner to 1 stock_picking record""",

    'description': """
    
    """,

    'author': "Magestore",
    'website': "http://www.magestore.vn",


    'category': 'tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/merge_so.xml",
    ],
    'application': True,
}