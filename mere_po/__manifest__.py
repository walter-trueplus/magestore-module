# -*- coding: utf-8 -*-
{
    'name': "mere_po",


    'summary': """
        this module allow user Merge (some) purchase_order from same vendor to 1 stock_picking record""",

    'description': """
       
    """,

    'author': "Magestore",
    'website': "http://www.magestore.vn",


    'category': 'tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/merge_po.xml",
    ],
    'application': True,
}