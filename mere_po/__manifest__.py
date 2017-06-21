# -*- coding: utf-8 -*-
{
    'name': "mere_po",


    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
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