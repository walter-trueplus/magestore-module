# -*- coding: utf-8 -*-
{
    'name': "Blog feature",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Magestore.com",
    'website': "Magestore.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','website_blog'],

    'data': [
        'views/templates.xml',
        'views/website_blog_view.xml',
    ],
    'application': True,
}